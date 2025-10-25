import csv
import os
from typing import Dict, List, Tuple

import numpy as np

FILES = [
    'mars_base_main_parts-001.csv',
    'mars_base_main_parts-002.csv',
    'mars_base_main_parts-003.csv',
]
OUTPUT_FILENAME = 'parts_to_work_on.csv'
TRANSPOSED_FILENAME = 'parts_to_work_on_transposed.csv'


def read_parts_file_numpy(filename):
    'numpy.genfromtxt를 사용하여 파일을 읽음(문자열+숫자 혼합 -> csv.reader로 안전하게 읽음)'
    if not os.path.exists(filename):
        raise FileNotFoundError(f'파일을 찾을 수 없습니다: {filename}')
    parts = []
    strengths = []
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if not row or len(row) < 2:
                continue
            part = row[0].strip()
            try:
                value = float(row[1])
            except Exception:
                # 비정상 값이면 건너뜀
                continue
            parts.append(part)
            strengths.append(value)
    arr = np.array(list(zip(parts, strengths)), dtype=object)
    return arr


def merge_and_average(arrays: List[np.ndarray]) -> List[Tuple[str, float]]:
    '부품명을 키로 강도값들을 모아서 평균을 계산'
    data: Dict[str, List[float]] = {}
    for arr in arrays:
        for name, val in arr:
            data.setdefault(str(name), []).append(float(val))
    result = []
    for name, vals in data.items():
        avg = sum(vals) / len(vals)
        result.append((name, avg))
    # parts는 ndarray 형태로 만들되, 여기서는 리스트로 반환
    return result


def save_parts_to_csv(parts_list, filename):
    'parts_list: list of (name, avg)'
    try:
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['parts', 'average_strength'])
            for name, avg in parts_list:
                writer.writerow([name, f'{avg:.3f}'])
    except Exception as e:
        raise IOError(f'CSV 저장 실패: {e}')


def main():
    arrays = []
    for fname in FILES:
        try:
            arr = read_parts_file_numpy(fname)
            arrays.append(arr)
            print(f'읽음: {fname} ({arr.shape[0]} 행)')
        except FileNotFoundError as e:
            print(e)
        except Exception as e:
            print(f'읽기 중 오류({fname}):', e)

    if not arrays:
        print('읽을 파일이 없습니다. 종료합니다.')
        return

    merged = merge_and_average(arrays)
    # numpy ndarray로 변환 (parts x 2)
    parts = np.array(merged, dtype=object)

    # 평균값이 50보다 작은 항목 필터
    to_work_on = [p for p in merged if p[1] < 50.0]
    print(f'평균값 < 50인 항목 개수: {len(to_work_on)}')

    try:
        save_parts_to_csv(to_work_on, OUTPUT_FILENAME)
        print(f'저장 완료: {OUTPUT_FILENAME}')
    except Exception as e:
        print(e)

    # 보너스: 파일 다시 읽기 -> 전치행렬 -> 저장 및 출력
    try:
        # parts2: numpy 로드 (문자열, 숫자)
        loaded = np.genfromtxt(OUTPUT_FILENAME, delimiter=',', dtype=None, encoding='utf-8', names=True)
        # genfromtxt with names=True returns structured array; 변환하여 2D array로 만듦
        if loaded.size == 0:
            print('parts_to_work_on.csv에 데이터가 없습니다.')
            return
        # 표준화: 2D object array
        parts2 = np.column_stack((loaded['parts'], loaded['average_strength'])).astype(object)
        parts3 = parts2.T  # 전치

        # 저장: 전치된 것을 CSV로
        # 전치 결과는 (2, N) 형태 -> 행 0: parts 명, 행1: 평균값
        with open(TRANSPOSED_FILENAME, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            for row in parts3:
                writer.writerow(row)
        print(f'전치행렬 저장: {TRANSPOSED_FILENAME}')
        print('전치행렬 샘플 출력(첫 5열):')
        # 간단 출력
        cols_to_show = min(parts3.shape[1], 5)
        for r in range(parts3.shape[0]):
            row_display = ', '.join(str(x) for x in parts3[r, :cols_to_show])
            print(f'row {r}: {row_display}')
    except Exception as e:
        print('전치 또는 재저장 중 오류:', e)

    # 반환용 answer
    answer = {
        'total_parts_distinct': len(parts),
        'to_work_on_count': len(to_work_on),
        'output_csv': OUTPUT_FILENAME,
        'transposed_csv': TRANSPOSED_FILENAME,
    }
    return answer


if __name__ == '__main__':
    main()
