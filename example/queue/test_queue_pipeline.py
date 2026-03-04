# test_queue_pipeline.py
import io
import builtins
import pytest
import queue_pipeline as stu

CSV_CONTENT = """id,source,payload
0,Parm-1,temp=23,ok
1,Parm-2,light=7421
2,Parm-3,humi=58,warning,check
3,Parm-4,temp=24
4,Parm-5,light=8100
5,Parm-1,humi=61
"""

def _expected_events():
    lines = CSV_CONTENT.strip().splitlines()
    _, *rows = lines
    out = []
    for ln in rows:
        i, src, payload = ln.split(',', 2)
        out.append((int(i), src, payload))
    # id 오름차순
    out.sort(key=lambda t: t[0])
    return out

def test_pipeline_success(monkeypatch):
    printed = []

    # fake open
    real_open = builtins.open
    def fake_open(file, mode='r', *args, **kwargs):
        if file == 'sensor_events.csv' and 'r' in mode:
            return io.StringIO(CSV_CONTENT)
        return real_open(file, mode, *args, **kwargs)
    monkeypatch.setattr(builtins, 'open', fake_open)

    # capture print
    real_print = builtins.print
    def fake_print(*args, **kwargs):
        printed.append((args, kwargs))
    monkeypatch.setattr(builtins, 'print', fake_print)

    # run student's main
    stu.main()

    assert len(printed) >= 4

    # 1) 원문
    raw = printed[0][0][0]
    assert isinstance(raw, str)
    assert raw.startswith('id,source,payload')
    assert 'humi=58,warning,check' in raw

    # 2) 파싱 리스트
    parsed = printed[1][0][0]
    exp = _expected_events()
    assert parsed == exp

    # 3) 앞 3개
    first3 = printed[2][0][0]
    assert first3 == exp[:3]

    # 4) 나머지
    rest = printed[3][0][0]
    assert rest == exp[3:]

def test_queue_behaviors():
    q = stu.SensorQueue()
    assert q.is_empty()
    assert len(q) == 0
    q.push((1,'a','x'))
    q.push((2,'b','y'))
    assert len(q) == 2
    assert q.peek() == (1,'a','x')
    assert q.pop() == (1,'a','x')
    assert q.pop() == (2,'b','y')
    assert q.pop() is None

def test_file_open_error(monkeypatch, capsys):
    def boom(*a, **k): raise FileNotFoundError()
    monkeypatch.setattr(builtins, 'open', boom)
    stu.main()
    out = capsys.readouterr().out
    assert 'File open error.' in out

def test_decoding_error(monkeypatch, capsys):
    class BadFile(io.StringIO):
        def read(self, *a, **k):
            raise UnicodeDecodeError('utf-8', b'\x80', 0, 1, 'bad')
    def fake_open(file, mode='r', *a, **k):
        if file == 'sensor_events.csv' and 'r' in mode:
            return BadFile('')
        return builtins.open(file, mode, *a, **k)
    monkeypatch.setattr(builtins, 'open', fake_open)
    stu.main()
    out = capsys.readouterr().out
    assert 'Decoding error.' in out

def test_invalid_header(monkeypatch, capsys):
    bad = "bad,header,here\n0,Parm-1,temp=23\n"
    def fake_open(file, mode='r', *a, **k):
        if file == 'sensor_events.csv' and 'r' in mode:
            return io.StringIO(bad)
        return builtins.open(file, mode, *a, **k)
    monkeypatch.setattr(builtins, 'open', fake_open)
    stu.main()
    out = capsys.readouterr().out
    assert 'Invalid data format.' in out

def test_invalid_id(monkeypatch, capsys):
    bad = "id,source,payload\na,Parm-1,temp=23\n"
    def fake_open(file, mode='r', *a, **k):
        if file == 'sensor_events.csv' and 'r' in mode:
            return io.StringIO(bad)
        return builtins.open(file, mode, *a, **k)
    monkeypatch.setattr(builtins, 'open', fake_open)
    stu.main()
    out = capsys.readouterr().out
    assert 'Invalid data format.' in out

