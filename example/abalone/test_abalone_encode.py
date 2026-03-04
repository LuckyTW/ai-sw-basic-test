# test_abalone_encode.py
import io
import builtins
import inspect
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import abalone_encode as stu

ATTR_TXT = """Sex
Length
Diameter
Height
Whole weight
Shucked weight
Viscera weight
Shell weight
Rings
"""

DATA_TXT = """M,0.455,0.365,0.095,0.5140,0.2245,0.1010,0.150,15
M,0.350,0.265,0.090,0.2255,0.0995,0.0485,0.070,7
F,0.530,0.420,0.135,0.6770,0.2565,0.1415,0.210,9
I,0.440,0.365,0.125,0.5160,0.2155,0.1140,0.155,10
I,0.330,0.255,0.080,0.2050,0.0895,0.0395,0.055,7
F,0.425,0.300,0.095,0.3515,0.1410,0.0775,0.120,8
"""

def _fake_open_router(file, mode='r', *args, **kwargs):
    if file == 'abalone_attributes.txt' and 'r' in mode:
        return io.StringIO(ATTR_TXT)
    if file == 'abalone.txt' and 'r' in mode:
        return io.StringIO(DATA_TXT)
    return builtins.open(file, mode, *args, **kwargs)

def _make_ohe_for_test(classes):
    sig = inspect.signature(OneHotEncoder.__init__)
    if 'sparse_output' in sig.parameters:
        return OneHotEncoder(categories=[classes], drop=None, sparse_output=False, dtype=int, handle_unknown='ignore')
    else:
        return OneHotEncoder(categories=[classes], drop=None, sparse=False, dtype=int, handle_unknown='ignore')

def _build_reference_df():
    cols = [ln.strip() for ln in ATTR_TXT.splitlines() if ln.strip()]
    df = pd.read_csv(io.StringIO(DATA_TXT), header=None, names=cols)
    df['label'] = df['Sex']
    df = df.drop(columns=['Sex'])
    return df

def test_full_pipeline_outputs(monkeypatch):
    printed = []
    monkeypatch.setattr(builtins, 'open', _fake_open_router)

    def fake_print(*args, **kwargs):
        printed.append((args, kwargs))
    monkeypatch.setattr(builtins, 'print', fake_print)

    stu.main()

    assert len(printed) >= 7

    df_ref = _build_reference_df()
    num_cols = df_ref.select_dtypes(include='number').columns.tolist()

    # 1) shape
    assert printed[0][0][0] == (6, 9)

    # 2) label 분포
    labels = printed[1][0][0]
    assert labels == {'M': 2, 'F': 2, 'I': 2}

    # 3) 라벨 매핑
    mapping = printed[2][0][0]
    le = LabelEncoder().fit(df_ref['label'])
    expected_mapping = {cls: int(i) for i, cls in enumerate(le.classes_)}
    assert mapping == expected_mapping

    # 4) 원핫 합계
    onehot_sum = printed[3][0][0]
    ohe = _make_ohe_for_test(le.classes_)
    arr = ohe.fit_transform(df_ref[['label']])
    cols = [f'label_{c}' for c in ohe.categories_[0]]
    expected_sum = dict(zip(cols, arr.sum(axis=0).astype(int).tolist()))
    assert onehot_sum == expected_sum

    # 5) 결측 대치 전/후 (샘플 데이터는 결측 없음)
    missing_before, missing_after = printed[4][0][0]
    assert missing_before == 0 and missing_after == 0

    # 6) 노이즈 경계
    bounds = printed[5][0][0]
    expected_bounds = {}
    for col in num_cols:
        l = float(df_ref[col].quantile(0.01))
        u = float(df_ref[col].quantile(0.99))
        expected_bounds[col] = (round(l, 6), round(u, 6))
    assert bounds == expected_bounds

    # 7) IQR 변경 건수
    changed = printed[6][0][0]
    # denoise 적용을 반영해서 동일 계산
    df_denoised = df_ref.copy()
    for col in num_cols:
        l = float(df_ref[col].quantile(0.01))
        u = float(df_ref[col].quantile(0.99))
        df_denoised[col] = df_denoised[col].clip(lower=l, upper=u)
    expected_changed = {}
    for col in num_cols:
        q1 = float(df_denoised[col].quantile(0.25))
        q3 = float(df_denoised[col].quantile(0.75))
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        ser = df_denoised[col]
        clipped = ser.clip(lower=lower, upper=upper)
        expected_changed[col] = int((ser != clipped).sum())
    assert changed == expected_changed