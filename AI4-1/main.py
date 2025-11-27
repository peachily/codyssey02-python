"""
Spaceship Titanic 데이터 분석 스크립트

Kaggle Spaceship Titanic 데이터를 분석하여 Transported 여부와의 관계를 파악합니다.
"""

import csv
import os
from collections import defaultdict
from typing import Dict, List, Tuple, Optional


def read_csv_file(file_path: str) -> Tuple[List[str], List[Dict[str, str]]]:
    """
    CSV 파일을 읽어서 헤더와 데이터를 반환합니다.
    
    Args:
        file_path: 읽을 CSV 파일의 경로
        
    Returns:
        (헤더 리스트, 데이터 딕셔너리 리스트) 튜플
    """
    headers = []
    data = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames
        
        for row in reader:
            data.append(row)
    
    return headers, data


def merge_data(train_data: List[Dict[str, str]], 
               test_data: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    train 데이터와 test 데이터를 병합합니다.
    
    Args:
        train_data: train 데이터 리스트
        test_data: test 데이터 리스트
        
    Returns:
        병합된 데이터 리스트
    """
    merged_data = train_data.copy()
    
    # test 데이터에 Transported 컬럼 추가 (None으로 설정)
    for row in test_data:
        row['Transported'] = ''
    
    merged_data.extend(test_data)
    return merged_data


def get_total_count(data: List[Dict[str, str]]) -> int:
    """
    전체 데이터의 수량을 반환합니다.
    
    Args:
        data: 데이터 리스트
        
    Returns:
        전체 데이터 수량
    """
    return len(data)


def convert_to_float(value: str) -> Optional[float]:
    """
    문자열을 float로 변환합니다. 변환 불가능하면 None을 반환합니다.
    
    Args:
        value: 변환할 문자열
        
    Returns:
        float 값 또는 None
    """
    if value == '' or value is None:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def convert_to_bool(value: str) -> Optional[bool]:
    """
    문자열을 bool로 변환합니다.
    
    Args:
        value: 변환할 문자열
        
    Returns:
        bool 값 또는 None
    """
    if value == '' or value is None:
        return None
    if value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False
    return None


def calculate_correlation(data: List[Dict[str, str]], 
                         column_name: str) -> float:
    """
    Transported와 특정 컬럼 간의 상관관계를 계산합니다.
    
    Args:
        data: 데이터 리스트
        column_name: 분석할 컬럼 이름
        
    Returns:
        상관관계 값 (0~1 사이)
    """
    transported_true = []
    transported_false = []
    
    for row in data:
        transported = convert_to_bool(row.get('Transported', ''))
        if transported is None:
            continue
        
        value = row.get(column_name, '')
        if value == '' or value is None:
            continue
        
        if transported:
            transported_true.append(value)
        else:
            transported_false.append(value)
    
    if not transported_true or not transported_false:
        return 0.0
    
    # 수치형 데이터인 경우 평균 차이로 상관관계 계산
    try:
        true_values = [convert_to_float(v) for v in transported_true]
        false_values = [convert_to_float(v) for v in transported_false]
        true_values = [v for v in true_values if v is not None]
        false_values = [v for v in false_values if v is not None]
        
        if true_values and false_values:
            true_avg = sum(true_values) / len(true_values)
            false_avg = sum(false_values) / len(false_values)
            diff = abs(true_avg - false_avg)
            max_val = max(max(true_values), max(false_values))
            min_val = min(min(true_values), min(false_values))
            if max_val - min_val > 0:
                return diff / (max_val - min_val)
    except (ValueError, TypeError):
        pass
    
    # 범주형 데이터인 경우 카이제곱 유사도 계산
    true_counts = defaultdict(int)
    false_counts = defaultdict(int)
    
    for v in transported_true:
        true_counts[v] += 1
    for v in transported_false:
        false_counts[v] += 1
    
    all_values = set(list(true_counts.keys()) + list(false_counts.keys()))
    if not all_values:
        return 0.0
    
    total_true = sum(true_counts.values())
    total_false = sum(false_counts.values())
    total = total_true + total_false
    
    if total == 0:
        return 0.0
    
    correlation = 0.0
    for val in all_values:
        true_ratio = true_counts[val] / total_true if total_true > 0 else 0
        false_ratio = false_counts[val] / total_false if total_false > 0 else 0
        correlation += abs(true_ratio - false_ratio)
    
    return correlation / len(all_values) if all_values else 0.0


def find_most_correlated_column(data: List[Dict[str, str]], 
                                headers: List[str]) -> Tuple[str, float]:
    """
    Transported와 가장 관련성이 높은 컬럼을 찾습니다.
    
    Args:
        data: 데이터 리스트
        headers: 컬럼 이름 리스트
        
    Returns:
        (컬럼 이름, 상관관계 값) 튜플
    """
    excluded_columns = {'PassengerId', 'Name', 'Transported', 'Cabin'}
    target_columns = [h for h in headers if h not in excluded_columns]
    
    correlations = {}
    for column in target_columns:
        corr = calculate_correlation(data, column)
        correlations[column] = corr
    
    if not correlations:
        return ('', 0.0)
    
    most_correlated = max(correlations.items(), key=lambda x: x[1])
    return most_correlated


def get_age_group(age: Optional[float]) -> Optional[str]:
    """
    나이를 연령대 그룹으로 변환합니다.
    
    Args:
        age: 나이 값
        
    Returns:
        연령대 문자열 (10대, 20대, ...) 또는 None
    """
    if age is None:
        return None
    
    age_int = int(age)
    if age_int < 10:
        return '10대 미만'
    elif age_int < 20:
        return '10대'
    elif age_int < 30:
        return '20대'
    elif age_int < 40:
        return '30대'
    elif age_int < 50:
        return '40대'
    elif age_int < 60:
        return '50대'
    elif age_int < 70:
        return '60대'
    elif age_int < 80:
        return '70대'
    else:
        return '70대 이상'


def get_age_group_data(data: List[Dict[str, str]]) -> Dict[str, Dict[str, int]]:
    """
    연령대별 Transported 여부 데이터를 수집합니다.
    
    Args:
        data: 데이터 리스트
        
    Returns:
        연령대별 Transported 통계 딕셔너리
    """
    age_group_data = defaultdict(lambda: {'True': 0, 'False': 0})
    
    for row in data:
        transported = convert_to_bool(row.get('Transported', ''))
        if transported is None:
            continue
        
        age = convert_to_float(row.get('Age', ''))
        age_group = get_age_group(age)
        
        if age_group:
            if transported:
                age_group_data[age_group]['True'] += 1
            else:
                age_group_data[age_group]['False'] += 1
    
    return dict(age_group_data)


def get_destination_age_distribution(data: List[Dict[str, str]]) -> Dict[str, Dict[str, int]]:
    """
    Destination별 연령대 분포를 수집합니다.
    
    Args:
        data: 데이터 리스트
        
    Returns:
        Destination별 연령대 분포 딕셔너리
    """
    destination_age_data = defaultdict(lambda: defaultdict(int))
    
    for row in data:
        destination = row.get('Destination', '')
        if destination == '':
            continue
        
        age = convert_to_float(row.get('Age', ''))
        age_group = get_age_group(age)
        
        if age_group:
            destination_age_data[destination][age_group] += 1
    
    return {dest: dict(ages) for dest, ages in destination_age_data.items()}


def main():
    """메인 함수"""
    # 파일 경로 설정
    base_dir = os.path.dirname(os.path.abspath(__file__))
    train_path = os.path.join(base_dir, 'spaceship-titanic', 'train.csv')
    test_path = os.path.join(base_dir, 'spaceship-titanic', 'test.csv')
    
    # 1. CSV 파일 읽기
    print('CSV 파일 읽는 중...')
    train_headers, train_data = read_csv_file(train_path)
    test_headers, test_data = read_csv_file(test_path)
    print(f'Train 데이터: {len(train_data)}개')
    print(f'Test 데이터: {len(test_data)}개')
    
    # 2. 데이터 병합
    print('\n데이터 병합 중...')
    merged_data = merge_data(train_data, test_data)
    
    # 3. 전체 데이터 수량 파악
    total_count = get_total_count(merged_data)
    print(f'\n전체 데이터 수량: {total_count}개')
    
    # 4. Transported와 가장 관련성이 높은 항목 찾기
    print('\nTransported와 가장 관련성이 높은 항목 분석 중...')
    most_correlated_column, correlation_value = find_most_correlated_column(
        train_data, train_headers)
    print(f'가장 관련성이 높은 항목: {most_correlated_column} '
          f'(상관관계: {correlation_value:.4f})')
    
    # 5. 연령대별 Transported 여부 데이터 수집
    print('\n연령대별 Transported 여부 데이터 수집 중...')
    age_group_data = get_age_group_data(train_data)
    
    # 6. 그래프 출력을 위한 데이터 준비 및 출력
    print('\n연령대별 Transported 여부 그래프 생성 중...')
    try:
        import pandas as pd
        import matplotlib.pyplot as plt
        
        # 한글 폰트 설정 (macOS)
        try:
            plt.rcParams['font.family'] = 'AppleGothic'
            plt.rcParams['axes.unicode_minus'] = False
        except:
            pass
        
        # 데이터프레임 생성
        age_groups = []
        transported_counts = []
        not_transported_counts = []
        
        age_order = ['10대 미만', '10대', '20대', '30대', '40대', '50대', 
                     '60대', '70대', '70대 이상']
        
        for age_group in age_order:
            if age_group in age_group_data:
                age_groups.append(age_group)
                transported_counts.append(age_group_data[age_group]['True'])
                not_transported_counts.append(age_group_data[age_group]['False'])
        
        df_age = pd.DataFrame({
            '연령대': age_groups,
            'Transported (True)': transported_counts,
            'Transported (False)': not_transported_counts
        })
        
        # 그래프 생성
        fig, ax = plt.subplots(figsize=(12, 6))
        x = range(len(age_groups))
        width = 0.35
        
        ax.bar([i - width/2 for i in x], transported_counts, width, 
               label='Transported (True)', color='skyblue')
        ax.bar([i + width/2 for i in x], not_transported_counts, width, 
               label='Transported (False)', color='lightcoral')
        
        ax.set_xlabel('연령대', fontsize=12)
        ax.set_ylabel('인원 수', fontsize=12)
        ax.set_title('연령대별 Transported 여부', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(age_groups, rotation=45, ha='right')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        output_path = os.path.join(base_dir, 'age_group_transported.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f'그래프 저장 완료: {output_path}')
        plt.close()
        
    except ImportError:
        print('Pandas 또는 Matplotlib이 설치되지 않아 그래프를 생성할 수 없습니다.')
        print('연령대별 데이터:')
        for age_group, counts in sorted(age_group_data.items()):
            print(f'  {age_group}: Transported=True {counts["True"]}명, '
                  f'Transported=False {counts["False"]}명')
    
    # 7. 보너스: Destination별 연령대 분포 시각화
    print('\nDestination별 연령대 분포 분석 중...')
    destination_age_data = get_destination_age_distribution(merged_data)
    
    try:
        import pandas as pd
        import matplotlib.pyplot as plt
        
        # 한글 폰트 설정 (macOS)
        try:
            plt.rcParams['font.family'] = 'AppleGothic'
            plt.rcParams['axes.unicode_minus'] = False
        except:
            pass
        
        # 데이터 준비
        destinations = list(destination_age_data.keys())
        age_order = ['10대 미만', '10대', '20대', '30대', '40대', '50대', 
                     '60대', '70대', '70대 이상']
        
        # 각 Destination별 연령대별 인원 수 수집
        plot_data = []
        for dest in destinations:
            for age_group in age_order:
                count = destination_age_data[dest].get(age_group, 0)
                if count > 0:
                    plot_data.append({
                        'Destination': dest,
                        '연령대': age_group,
                        '인원 수': count
                    })
        
        if plot_data:
            df_dest = pd.DataFrame(plot_data)
            
            # 그래프 생성
            fig, ax = plt.subplots(figsize=(14, 8))
            
            # 각 Destination별로 막대 그래프 생성
            dest_counts = {}
            for dest in destinations:
                counts = [destination_age_data[dest].get(age, 0) 
                         for age in age_order]
                dest_counts[dest] = counts
            
            x = range(len(age_order))
            width = 0.8 / len(destinations)
            
            for i, dest in enumerate(destinations):
                counts = dest_counts[dest]
                offset = (i - len(destinations)/2 + 0.5) * width
                ax.bar([xi + offset for xi in x], counts, width, 
                      label=dest, alpha=0.8)
            
            ax.set_xlabel('연령대', fontsize=12)
            ax.set_ylabel('인원 수', fontsize=12)
            ax.set_title('Destination별 연령대 분포', fontsize=14, fontweight='bold')
            ax.set_xticks(x)
            ax.set_xticklabels(age_order, rotation=45, ha='right')
            ax.legend()
            ax.grid(axis='y', alpha=0.3)
            
            plt.tight_layout()
            output_path = os.path.join(base_dir, 'destination_age_distribution.png')
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f'그래프 저장 완료: {output_path}')
            plt.close()
        else:
            print('시각화할 데이터가 없습니다.')
            
    except ImportError:
        print('Pandas 또는 Matplotlib이 설치되지 않아 그래프를 생성할 수 없습니다.')
        print('Destination별 연령대 분포:')
        for dest, ages in destination_age_data.items():
            print(f'  {dest}:')
            for age_group, count in sorted(ages.items()):
                print(f'    {age_group}: {count}명')
    
    print('\n작업 완료!')


if __name__ == '__main__':
    main()

