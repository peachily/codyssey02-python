import csv
import os
import pickle

INPUT_FILENAME = 'Mars_Base_Inventory_List.csv'
DANGER_FILENAME = 'Mars_Base_Inventory_danger.csv'
BINARY_FILENAME = 'Mars_Base_Inventory_List.bin'


def detect_dialect_and_read_rows(filename):
    '파일의 구분자(콤마/탭 등)를 자동 탐지하여 모든 행을 리스트로 반환'
    if not os.path.exists(filename):
        raise FileNotFoundError(f'파일을 찾을 수 없습니다: {filename}')
    with open(filename, 'r', encoding='utf-8') as f:
        sample = f.read(4096)
        f.seek(0)
        sniffer = csv.Sniffer()
        try:
            dialect = sniffer.sniff(sample)
        except csv.Error:
            # 기본으로 comma와 tab 중에 포함된 것으로 시도
            dialect = csv.get_dialect('excel')
        reader = csv.reader(f, dialect)
        rows = [row for row in reader if any(field.strip() for field in row)]
    return rows


def parse_inventory_rows(rows):
    '헤더를 제외한 라인들을 dict 리스트로 파싱, flammability는 float로 변환 시도'
    header = rows[0]
    items = []
    # 컬럼 인덱스 찾기 (대소문자 관계없이)
    h_lower = [h.strip().lower() for h in header]
    try:
        idx_name = h_lower.index('substance')
    except ValueError:
        idx_name = 0
    try:
        idx_flamm = h_lower.index('flammability')
    except ValueError:
        # 마지막 열로 추정
        idx_flamm = len(header) - 1

    for row in rows[1:]:
        # 행이 짧을 수 있으므로 안전하게 접근
        name = row[idx_name].strip() if idx_name < len(row) else ''
        raw_flamm = row[idx_flamm].strip() if idx_flamm < len(row) else ''
        # flammability float 변환 시도, 실패시 None으로
        flamm = None
        try:
            flamm = float(raw_flamm)
        except Exception:
            # 일부 항목에 'Various' 같은 문자열이 있음 -> None 처리
            flamm = None
        items.append({
            'substance': name,
            'flammability': flamm,
            'raw_row': row,
        })
    return items


def sort_by_flammability_desc(items):
    'flammability가 None인 항목은 가장 낮게 취급하여 내림차순 정렬'
    return sorted(items, key=lambda x: (x['flammability'] is None, -(x['flammability'] or 0.0)))


def filter_dangerous(items, threshold=0.7):
    'threshold 이상인 항목만 반환 (flammability가 None인 항목은 제외)'
    return [it for it in items if it['flammability'] is not None and it['flammability'] >= threshold]


def write_csv_from_items(items, out_filename, header_row):
    'raw_row 사용하여 CSV로 저장'
    try:
        with open(out_filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header_row)
            for it in items:
                writer.writerow(it['raw_row'])
    except Exception as e:
        raise IOError(f'CSV 쓰기 실패: {e}')


def save_binary(obj, filename):
    'pickle로 바이너리 저장'
    try:
        with open(filename, 'wb') as f:
            pickle.dump(obj, f)
    except Exception as e:
        raise IOError(f'바이너리 저장 실패: {e}')


def read_binary(filename):
    'pickle로 바이너리 읽기'
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        raise IOError(f'바이너리 읽기 실패: {e}')


def explain_text_vs_binary():
    '텍스트 파일과 바이너리 파일의 차이점 간단 출력'
    explanation = (
        '텍스트 파일:\n'
        '- 사람이 읽을 수 있음(편집기에서 열람/수정 가능).\n'
        '- 크로스플랫폼 호환성이 좋고 디버깅이 쉬움.\n'
        '- 숫자/구조를 저장할 때 추가 파싱이 필요할 수 있음.\n\n'
        '바이너리 파일:\n'
        '- 자료구조(예: 파이썬 객체)를 그대로 저장 가능(pickle 등).\n'
        '- 저장/로드가 빠르고 파일 크기가 작을 수 있음.\n'
        '- 사람이 읽기 어렵고, 포맷 종속적일 수 있어 안전/버전 관리 주의 필요.\n'
    )
    return explanation


def main():
    '전체 파이프라인 실행'
    try:
        rows = detect_dialect_and_read_rows(INPUT_FILENAME)
    except FileNotFoundError as e:
        print(e)
        return
    except Exception as e:
        print('파일 읽기 중 오류:', e)
        return

    items = parse_inventory_rows(rows)
    sorted_items = sort_by_flammability_desc(items)

    # 화면 출력(상위 20개 요약)
    print('\n=== 정렬된 인벤토리 상위 20개 (flammability 내림차순) ===')
    for i, it in enumerate(sorted_items[:20], 1):
        name = it['substance']
        fl = it['flammability']
        fl_text = f'{fl:.3f}' if fl is not None else 'N/A'
        print(f'{i:02d}. {name} - flammability: {fl_text}')

    # 필터링 및 저장
    dangerous = filter_dangerous(sorted_items, threshold=0.7)
    print(f'\n인화성 >= 0.7 항목 개수: {len(dangerous)}')
    try:
        write_csv_from_items(dangerous, DANGER_FILENAME, rows[0])
        print(f'위험 항목을 CSV로 저장했습니다: {DANGER_FILENAME}')
    except Exception as e:
        print(e)

    # 보너스: 바이너리 저장/읽기
    try:
        save_binary(sorted_items, BINARY_FILENAME)
        print(f'정렬된 배열을 바이너리로 저장했습니다: {BINARY_FILENAME}')
        loaded = read_binary(BINARY_FILENAME)
        print('\n=== 바이너리로부터 읽은 상위 10개 항목 확인 ===')
        for it in loaded[:10]:
            name = it['substance']
            fl = it['flammability']
            fl_text = f'{fl:.3f}' if fl is not None else 'N/A'
            print(f'- {name} : {fl_text}')
    except Exception as e:
        print('바이너리 저장/읽기 중 오류:', e)

    # 텍스트 vs 바이너리 설명 출력
    print('\n--- 텍스트 파일과 바이너리 파일의 차이 ---')
    print(explain_text_vs_binary())

    # 결과 반환(테스트/재사용을 위해)
    answer = {
        'total_items': len(items),
        'danger_count': len(dangerous),
        'danger_csv': DANGER_FILENAME,
        'binary_file': BINARY_FILENAME,
    }
    return answer


if __name__ == '__main__':
    main()
