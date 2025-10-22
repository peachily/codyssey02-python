def read_log(path: str = 'mission_computer_main.log') -> str:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError: raise
    except UnicodeDecodeError: raise
    except Exception: raise

def log_to_tuple(log):
    raw = log.strip().split('\n')
    if raw[0] != 'timestamp,event,message': raise ValueError
    pairs = []
    for line in raw[1:]:
        if line.strip():
            p = line.split(',', 2)
            if len(p) != 3 or len(p[0]) != 19: raise ValueError
            pairs.append((p[0], p[2]))
    return pairs

def sort_log(t): return sorted(t, key=lambda x: x[0], reverse=True)
def log_to_dict(t): return {k: v for k, v in t}

def main():
    try:
        log = read_log(); print(log)
        t = log_to_tuple(log); print(t)
        st = sort_log(t); print(st)
        d = log_to_dict(st); print(d)
    except FileNotFoundError: print('File open error.'); return
    except UnicodeDecodeError: print('Decoding error.'); return
    except ValueError: print('Invalid log format.'); return
    except Exception: print('Processing error.'); return

if __name__ == '__main__': main()
