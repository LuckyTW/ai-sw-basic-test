# abalone_encode.py
from __future__ import annotations
from typing import List, Tuple, Dict, Any, Optional
import io
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import inspect

# ---------- 파일 유틸 ----------
def _read_text(path: str) -> Optional[str]:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except (FileNotFoundError, PermissionError, IsADirectoryError, OSError):
        print('File open error.')
        return None
    except UnicodeDecodeError:
        print('Decoding error.')
        return None

def load_attributes(path: str = 'abalone_attributes.txt') -> Optional[List[str]]:
    raw = _read_text(path)
    if raw is None:
        return None
    cols = [ln.strip() for ln in raw.splitlines() if ln.strip() != '']
    return cols

def load_data(columns: List[str], path: str = 'abalone.txt') -> Optional[pd.DataFrame]:
    raw = _read_text(path)
    if raw is None:
        return None
    try:
        df = pd.read_csv(io.StringIO(raw), header=None, names=columns)
        if df.shape[1] != len(columns):
            raise ValueError('column count mismatch')
        return df
    except Exception:
        print('Processing error.')
        return None

# ---------- 전처리 ----------
def impute_missing(df: pd.DataFrame) -> pd.DataFrame:
    """수치형은 중앙값, 범주형/문자형은 최빈값으로 결측 대치."""
    out = df.copy()
    num_cols = out.select_dtypes(include='number').columns
    obj_cols = out.select_dtypes(exclude='number').columns

    if len(num_cols) > 0:
        med = out[num_cols].median()
        out[num_cols] = out[num_cols].fillna(med)

    for col in obj_cols:
        mode_series = out[col].mode(dropna=True)
        fill = mode_series.iloc[0] if not mode_series.empty else ''
        out[col] = out[col].fillna(fill)

    return out

def denoise(df: pd.DataFrame, lower_q: float = 0.01, upper_q: float = 0.99) -> Tuple[pd.DataFrame, Dict[str, Tuple[float, float]]]:
    """수치형 열에 대해 분위수 기반 클리핑. 경계값 사전도 함께 반환."""
    out = df.copy()
    num_cols = out.select_dtypes(include='number').columns.tolist()
    bounds: Dict[str, Tuple[float, float]] = {}
    for col in num_cols:
        lower = float(out[col].quantile(lower_q))
        upper = float(out[col].quantile(upper_q))
        bounds[col] = (round(lower, 6), round(upper, 6))
        out[col] = out[col].clip(lower=lower, upper=upper)
    return out, bounds

def handle_outliers_iqr(df: pd.DataFrame, k: float = 1.5) -> Tuple[pd.DataFrame, Dict[str, int]]:
    """수치형 열에 대해 IQR 클리핑을 적용하고, 열별 변경된 개수 집계도 반환."""
    out = df.copy()
    num_cols = out.select_dtypes(include='number').columns.tolist()
    changed_counts: Dict[str, int] = {}
    for col in num_cols:
        q1 = float(out[col].quantile(0.25))
        q3 = float(out[col].quantile(0.75))
        iqr = q3 - q1
        lower = q1 - k * iqr
        upper = q3 + k * iqr
        ser = out[col]
        clipped = ser.clip(lower=lower, upper=upper)
        changed_counts[col] = int((ser != clipped).sum())
        out[col] = clipped
    return out, changed_counts

# ---------- 호환성 유틸 (OneHotEncoder) ----------
def _make_ohe(categories) -> OneHotEncoder:
    """
    sklearn 1.2+: sparse_output
    sklearn <=1.4: sparse (deprecated), 일부 버전에서는 sparse 제거됨
    """
    sig = inspect.signature(OneHotEncoder.__init__)
    if 'sparse_output' in sig.parameters:
        # 최신
        return OneHotEncoder(
            categories=[categories],
            drop=None,
            sparse_output=False,
            dtype=int,
            handle_unknown='ignore',
        )
    else:
        # 구버전 호환
        return OneHotEncoder(
            categories=[categories],
            drop=None,
            sparse=False,
            dtype=int,
            handle_unknown='ignore',
        )

# ---------- 메인 파이프라인 ----------
def main() -> None:
    try:
        cols = load_attributes()
        if cols is None:
            return

        df = load_data(cols)
        if df is None:
            return

        # 라벨 분리
        if 'Sex' not in df.columns:
            print('Processing error.')
            return
        df['label'] = df['Sex']
        df = df.drop(columns=['Sex'])

        # (1) 원본 모양
        print(df.shape)

        # (2) 라벨 분포
        label_counts = df['label'].value_counts().to_dict()
        print(label_counts)

        # (3) 라벨 인코딩 매핑
        le = LabelEncoder()
        _ = le.fit_transform(df['label'])
        mapping = {cls: int(i) for i, cls in enumerate(le.classes_)}
        print(mapping)

        # (4) 원핫 합계 검증 (버전 호환 OHE)
        ohe = _make_ohe(le.classes_)
        onehot_arr = ohe.fit_transform(df[['label']])
        onehot_cols = [f'label_{c}' for c in ohe.categories_[0]]
        onehot = pd.DataFrame(onehot_arr, columns=onehot_cols, index=df.index)
        print(onehot.sum().to_dict())

        # (5) 결측 대치 결과
        missing_before = int(df.isna().sum().sum())
        df_imp = impute_missing(df)
        missing_after = int(df_imp.isna().sum().sum())
        print((missing_before, missing_after))

        # (6) 노이즈 클리핑 경계 (분위수)
        df_denoised, qbounds = denoise(df_imp, lower_q=0.01, upper_q=0.99)
        print(qbounds)

        # (7) IQR 클리핑 건수
        df_iqr, changed = handle_outliers_iqr(df_denoised, k=1.5)
        print(changed)

    except ValueError:
        print('Processing error.')
    except Exception:
        print('Processing error.')

if __name__ == '__main__':
    main()