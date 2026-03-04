# queue_pipeline.py
from __future__ import annotations
from typing import List, Tuple, Optional
from collections import deque

# 1) CSV 읽기
def read_csv(path: str = 'sensor_events.csv') -> str:
    """CSV 원문을 읽어 문자열로 반환한다."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except (FileNotFoundError, PermissionError, IsADirectoryError, OSError):
        print('File open error.')
        return ''
    except UnicodeDecodeError:
        print('Decoding error.')
        return ''

# 2) 직접 구현 큐
class SensorQueue:
    def __init__(self) -> None:
        self._dq: deque = deque()

    def push(self, item) -> None:
        self._dq.append(item)

    def pop(self) -> Optional[tuple]:
        return self._dq.popleft() if self._dq else None

    def peek(self) -> Optional[tuple]:
        return self._dq[0] if self._dq else None

    def __len__(self) -> int:
        return len(self._dq)

    def is_empty(self) -> bool:
        return not self._dq

# 3) 파이프라인 함수
def parse_events(raw: str) -> List[Tuple[int, str, str]]:
    lines = [ln for ln in raw.splitlines() if ln.strip() != '']
    if not lines:
        raise ValueError('Invalid data format (empty).')
    header, *rows = lines
    if header.strip() != 'id,source,payload':
        raise ValueError('Invalid data format (header).')

    out: List[Tuple[int, str, str]] = []
    for ln in rows:
        parts = ln.split(',', 2)  # payload 콤마 보존
        if len(parts) != 3:
            raise ValueError('Invalid data format (columns).')
        sid, src, payload = parts
        try:
            i = int(sid)
        except ValueError as e:
            raise ValueError('Invalid data format (id).') from e
        out.append((i, src, payload))
    # id 오름차순 정렬
    out.sort(key=lambda t: t[0])
    return out

def enqueue_all(events: List[Tuple[int, str, str]], q: SensorQueue) -> None:
    for it in events:
        q.push(it)

def consume_k(q: SensorQueue, k: int) -> List[Tuple[int, str, str]]:
    n = max(0, k)
    out: List[Tuple[int, str, str]] = []
    for _ in range(n):
        item = q.pop()
        if item is None:
            break
        out.append(item)
    return out

def drain_all(q: SensorQueue) -> List[Tuple[int, str, str]]:
    out: List[Tuple[int, str, str]] = []
    while not q.is_empty():
        out.append(q.pop())
    return out

# 4) 엔트리포인트: 4회 print
def main() -> None:
    raw = read_csv()
    if not raw:
        return
    try:
        # ① 원문
        print(raw)
        # ② 파싱 리스트
        events = parse_events(raw)
        print(events)
        # ③ 앞 3개 소비
        q = SensorQueue()
        enqueue_all(events, q)
        first3 = consume_k(q, 3)
        print(first3)
        # ④ 나머지 전부 소비
        rest = drain_all(q)
        print(rest)
    except ValueError:
        print('Invalid data format.')
        return
    except Exception:
        print('Processing error.')
        return

if __name__ == '__main__':
    main()

