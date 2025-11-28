"""
인구 데이터 분석 스크립트

2015년 이후 인구 데이터를 분석하여 일반가구원 통계를 파악합니다.
"""

import csv
import os
from typing import Dict, List, Tuple, Optional


def read_csv_to_dataframe(file_path: str):
    """
    CSV 파일을 읽어서 pandas DataFrame으로 반환합니다.
    
    Args:
        file_path: 읽을 CSV 파일의 경로
        
    Returns:
        pandas DataFrame 객체
    """
    try:
        import pandas as pd
        
        # CSV 파일 읽기
        df = pd.read_csv(file_path, encoding='utf-8')
        return df
    except ImportError:
        print('Pandas가 설치되지 않았습니다.')
        return None


def remove_columns_except_general_population(df):
    """
    일반가구원 컬럼을 제외한 나머지 컬럼들을 삭제합니다.
    
    Args:
        df: pandas DataFrame
        
    Returns:
        일반가구원 컬럼만 남긴 DataFrame
    """
    if df is None:
        return None
    
    # 일반가구원 컬럼과 필요한 식별 컬럼들만 유지
    columns_to_keep = ['시점', '행정구역별(시군구)', '성별', '연령별', '일반가구원']
    existing_columns = [col for col in columns_to_keep if col in df.columns]
    
    df_filtered = df[existing_columns].copy()
    return df_filtered


def filter_data_from_2015(df):
    """
    2015년 이후 데이터만 필터링합니다.
    
    Args:
        df: pandas DataFrame
        
    Returns:
        2015년 이후 데이터만 포함한 DataFrame
    """
    if df is None:
        return None
    
    # 시점 컬럼을 숫자로 변환
    df['시점'] = df['시점'].astype(str).str.replace('"', '').astype(int)
    
    # 2015년 이후 데이터만 필터링
    df_filtered = df[df['시점'] >= 2015].copy()
    return df_filtered


def get_year_range(df):
    """
    데이터에 포함된 연도 범위를 반환합니다.
    
    Args:
        df: pandas DataFrame
        
    Returns:
        (최소 연도, 최대 연도) 튜플
    """
    if df is None or df.empty:
        return (None, None)
    
    min_year = int(df['시점'].min())
    max_year = int(df['시점'].max())
    return (min_year, max_year)


def convert_general_population_to_numeric(value):
    """
    일반가구원 값을 숫자로 변환합니다.
    
    Args:
        value: 변환할 값
        
    Returns:
        숫자 값 또는 None
    """
    if value is None or value == '' or value == 'X' or value == '-':
        return None
    
    try:
        # pandas의 NaN 체크
        try:
            import pandas as pd
            if pd.isna(value):
                return None
        except (ImportError, AttributeError):
            pass
        
        # 문자열인 경우 따옴표 제거
        if isinstance(value, str):
            value = value.replace('"', '').replace(',', '')
        return int(float(value))
    except (ValueError, TypeError):
        return None


def get_gender_year_statistics(df):
    """
    2015년 이후 남자 및 여자의 연도별 일반가구원 데이터 통계를 계산합니다.
    
    Args:
        df: pandas DataFrame
        
    Returns:
        연도별 성별 통계 DataFrame
    """
    if df is None:
        return None
    
    try:
        import pandas as pd
        
        # 일반가구원을 숫자로 변환
        df['일반가구원'] = df['일반가구원'].apply(convert_general_population_to_numeric)
        
        # 남자와 여자 데이터만 필터링 (합계 제외)
        gender_df = df[df['성별'].isin(['남자', '여자'])].copy()
        
        # 연도별, 성별별로 그룹화하여 합계 계산
        # 합계 행 제외 (연령별이 '합계'인 행 제외)
        gender_df = gender_df[gender_df['연령별'] != '합계']
        
        statistics = gender_df.groupby(['시점', '성별'])['일반가구원'].sum().reset_index()
        statistics_pivot = statistics.pivot(index='시점', columns='성별', values='일반가구원')
        
        return statistics_pivot
    except Exception as e:
        print(f'통계 계산 중 오류 발생: {e}')
        return None


def get_age_statistics(df):
    """
    2015년 이후 연령별 일반가구원 데이터 통계를 계산합니다.
    
    Args:
        df: pandas DataFrame
        
    Returns:
        연령별 통계 DataFrame
    """
    if df is None:
        return None
    
    try:
        import pandas as pd
        
        # 일반가구원을 숫자로 변환
        df['일반가구원'] = df['일반가구원'].apply(convert_general_population_to_numeric)
        
        # 계(전체) 데이터만 사용
        total_df = df[df['성별'] == '계'].copy()
        
        # 합계 행 제외
        total_df = total_df[total_df['연령별'] != '합계']
        
        # 연도별, 연령별로 그룹화하여 합계 계산
        statistics = total_df.groupby(['시점', '연령별'])['일반가구원'].sum().reset_index()
        statistics_pivot = statistics.pivot(index='시점', columns='연령별', values='일반가구원')
        
        return statistics_pivot
    except Exception as e:
        print(f'통계 계산 중 오류 발생: {e}')
        return None


def get_gender_age_statistics(df):
    """
    2015년 이후 남자 및 여자의 연령별 일반가구원 데이터를 계산합니다.
    
    Args:
        df: pandas DataFrame
        
    Returns:
        성별, 연령별 통계 DataFrame
    """
    if df is None:
        return None
    
    try:
        import pandas as pd
        
        # 일반가구원을 숫자로 변환
        df['일반가구원'] = df['일반가구원'].apply(convert_general_population_to_numeric)
        
        # 남자와 여자 데이터만 필터링
        gender_df = df[df['성별'].isin(['남자', '여자'])].copy()
        
        # 합계 행 제외
        gender_df = gender_df[gender_df['연령별'] != '합계']
        
        # 연도별, 성별, 연령별로 그룹화
        statistics = gender_df.groupby(['시점', '성별', '연령별'])['일반가구원'].sum().reset_index()
        
        return statistics
    except Exception as e:
        print(f'통계 계산 중 오류 발생: {e}')
        return None


def create_gender_age_line_chart(statistics_df):
    """
    남자 및 여자의 연령별 일반가구원 데이터를 꺽은선 그래프로 표현합니다.
    
    Args:
        statistics_df: 성별, 연령별 통계 DataFrame
    """
    if statistics_df is None or statistics_df.empty:
        print('그래프를 생성할 데이터가 없습니다.')
        return
    
    try:
        import pandas as pd
        import matplotlib.pyplot as plt
        
        # 한글 폰트 설정 (macOS)
        try:
            plt.rcParams['font.family'] = 'AppleGothic'
            plt.rcParams['axes.unicode_minus'] = False
        except:
            pass
        
        # 연령대 순서 정의
        age_order = ['15세미만', '15~19세', '20~24세', '25~29세', '30~34세', 
                     '35~39세', '40~44세', '45~49세', '50~54세', '55~59세',
                     '60~64세', '65~69세', '70~74세', '75~79세', '80~84세', '85세이상']
        
        # 연도별로 데이터 재구성
        years = sorted(statistics_df['시점'].unique())
        
        # 각 연령대별로 그래프 생성
        fig, axes = plt.subplots(4, 4, figsize=(20, 16))
        axes = axes.flatten()
        
        for idx, age_group in enumerate(age_order):
            if idx >= len(axes):
                break
            
            ax = axes[idx]
            
            # 남자 데이터
            male_data = statistics_df[
                (statistics_df['성별'] == '남자') & 
                (statistics_df['연령별'] == age_group)
            ].sort_values('시점')
            
            # 여자 데이터
            female_data = statistics_df[
                (statistics_df['성별'] == '여자') & 
                (statistics_df['연령별'] == age_group)
            ].sort_values('시점')
            
            if not male_data.empty and not female_data.empty:
                ax.plot(male_data['시점'], male_data['일반가구원'], 
                       marker='o', label='남자', linewidth=2)
                ax.plot(female_data['시점'], female_data['일반가구원'], 
                       marker='s', label='여자', linewidth=2)
            
            ax.set_title(f'{age_group}', fontsize=10, fontweight='bold')
            ax.set_xlabel('연도', fontsize=9)
            ax.set_ylabel('일반가구원 수', fontsize=9)
            ax.legend(fontsize=8)
            ax.grid(True, alpha=0.3)
            ax.tick_params(labelsize=8)
        
        plt.suptitle('2015년 이후 남자 및 여자의 연령별 일반가구원 변화', 
                     fontsize=14, fontweight='bold', y=0.995)
        plt.tight_layout()
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(base_dir, 'gender_age_line_chart.png')
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f'그래프 저장 완료: {output_path}')
        plt.close()
        
    except ImportError:
        print('Matplotlib이 설치되지 않아 그래프를 생성할 수 없습니다.')
    except Exception as e:
        print(f'그래프 생성 중 오류 발생: {e}')


def create_trend_report(statistics_df, age_statistics_df):
    """
    연령별 그래프의 변화를 보고 인구의 변화 트렌드를 데이터를 기반으로 정리한 리포터를 작성합니다.
    
    Args:
        statistics_df: 성별, 연령별 통계 DataFrame
        age_statistics_df: 연령별 통계 DataFrame
    """
    if statistics_df is None or age_statistics_df is None:
        print('리포터를 작성할 데이터가 없습니다.')
        return
    
    try:
        import pandas as pd
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        report_path = os.path.join(base_dir, 'population_trend_report.txt')
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('=' * 80 + '\n')
            f.write('인구 변화 트렌드 분석 리포터\n')
            f.write('=' * 80 + '\n\n')
            
            # 데이터 기간
            years = sorted(statistics_df['시점'].unique())
            f.write(f'분석 기간: {years[0]}년 ~ {years[-1]}년 ({len(years)}년간)\n\n')
            
            # 전체 인구 변화
            f.write('1. 전체 인구 변화\n')
            f.write('-' * 80 + '\n')
            
            total_by_year = age_statistics_df.sum(axis=1)
            for year in years:
                if year in total_by_year.index:
                    f.write(f'{year}년: {int(total_by_year[year]):,}명\n')
            
            first_year_total = total_by_year[years[0]]
            last_year_total = total_by_year[years[-1]]
            change_rate = ((last_year_total - first_year_total) / first_year_total) * 100
            f.write(f'\n전체 변화율: {change_rate:.2f}% '
                   f'({int(first_year_total):,}명 → {int(last_year_total):,}명)\n\n')
            
            # 연령대별 변화
            f.write('2. 연령대별 인구 변화\n')
            f.write('-' * 80 + '\n')
            
            age_order = ['15세미만', '15~19세', '20~24세', '25~29세', '30~34세', 
                         '35~39세', '40~44세', '45~49세', '50~54세', '55~59세',
                         '60~64세', '65~69세', '70~74세', '75~79세', '80~84세', '85세이상']
            
            for age_group in age_order:
                if age_group in age_statistics_df.columns:
                    first_value = age_statistics_df[age_group].iloc[0]
                    last_value = age_statistics_df[age_group].iloc[-1]
                    
                    if pd.notna(first_value) and pd.notna(last_value):
                        change = last_value - first_value
                        change_rate = (change / first_value) * 100 if first_value > 0 else 0
                        f.write(f'{age_group}: {int(first_value):,}명 → {int(last_value):,}명 '
                               f'({change_rate:+.2f}%)\n')
            
            # 성별 변화
            f.write('\n3. 성별 인구 변화\n')
            f.write('-' * 80 + '\n')
            
            male_data = statistics_df[statistics_df['성별'] == '남자'].groupby('시점')['일반가구원'].sum()
            female_data = statistics_df[statistics_df['성별'] == '여자'].groupby('시점')['일반가구원'].sum()
            
            for year in years:
                if year in male_data.index and year in female_data.index:
                    male_count = int(male_data[year])
                    female_count = int(female_data[year])
                    total = male_count + female_count
                    male_ratio = (male_count / total) * 100 if total > 0 else 0
                    female_ratio = (female_count / total) * 100 if total > 0 else 0
                    f.write(f'{year}년: 남자 {male_count:,}명 ({male_ratio:.2f}%), '
                           f'여자 {female_count:,}명 ({female_ratio:.2f}%)\n')
            
            # 주요 트렌드 분석
            f.write('\n4. 주요 트렌드 분석\n')
            f.write('-' * 80 + '\n')
            
            # 고령화 추세
            old_ages = ['65~69세', '70~74세', '75~79세', '80~84세', '85세이상']
            old_pop_first = sum([age_statistics_df[age].iloc[0] 
                                for age in old_ages if age in age_statistics_df.columns 
                                and pd.notna(age_statistics_df[age].iloc[0])])
            old_pop_last = sum([age_statistics_df[age].iloc[-1] 
                               for age in old_ages if age in age_statistics_df.columns 
                               and pd.notna(age_statistics_df[age].iloc[-1])])
            
            if old_pop_first > 0:
                old_change_rate = ((old_pop_last - old_pop_first) / old_pop_first) * 100
                f.write(f'고령 인구(65세 이상) 변화: {int(old_pop_first):,}명 → {int(old_pop_last):,}명 '
                       f'({old_change_rate:+.2f}%)\n')
            
            # 청년층 추세
            young_ages = ['15~19세', '20~24세', '25~29세']
            young_pop_first = sum([age_statistics_df[age].iloc[0] 
                                  for age in young_ages if age in age_statistics_df.columns 
                                  and pd.notna(age_statistics_df[age].iloc[0])])
            young_pop_last = sum([age_statistics_df[age].iloc[-1] 
                                 for age in young_ages if age in age_statistics_df.columns 
                                 and pd.notna(age_statistics_df[age].iloc[-1])])
            
            if young_pop_first > 0:
                young_change_rate = ((young_pop_last - young_pop_first) / young_pop_first) * 100
                f.write(f'청년층(15~29세) 변화: {int(young_pop_first):,}명 → {int(young_pop_last):,}명 '
                       f'({young_change_rate:+.2f}%)\n')
            
            f.write('\n' + '=' * 80 + '\n')
            f.write('리포터 작성 완료\n')
            f.write('=' * 80 + '\n')
        
        print(f'리포터 저장 완료: {report_path}')
        
    except Exception as e:
        print(f'리포터 작성 중 오류 발생: {e}')


def main():
    """메인 함수"""
    # 파일 경로 설정
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, 'population.csv')
    
    # 1. CSV 파일을 DataFrame으로 읽기
    print('CSV 파일 읽는 중...')
    df = read_csv_to_dataframe(csv_path)
    
    if df is None:
        print('데이터를 읽을 수 없습니다.')
        return
    
    print(f'원본 데이터: {len(df)}행')
    
    # 2. 일반가구원을 제외한 나머지 컬럼 삭제
    print('\n일반가구원 컬럼만 남기고 나머지 삭제 중...')
    df_filtered = remove_columns_except_general_population(df)
    print(f'필터링된 데이터: {len(df_filtered)}행')
    print(f'컬럼: {list(df_filtered.columns)}')
    
    # 3. 2015년 이후 데이터 필터링
    print('\n2015년 이후 데이터 필터링 중...')
    df_2015 = filter_data_from_2015(df_filtered)
    min_year, max_year = get_year_range(df_2015)
    print(f'데이터 기간: {min_year}년 ~ {max_year}년')
    print(f'필터링된 데이터: {len(df_2015)}행')
    
    # 4. 남자 및 여자의 연도별 일반가구원 데이터 통계 출력
    print('\n남자 및 여자의 연도별 일반가구원 데이터 통계 계산 중...')
    gender_year_stats = get_gender_year_statistics(df_2015)
    
    if gender_year_stats is not None:
        print('\n[남자 및 여자 연도별 일반가구원 통계]')
        print(gender_year_stats)
        print()
    
    # 5. 연령별 일반가구원 데이터 통계 출력
    print('\n연령별 일반가구원 데이터 통계 계산 중...')
    age_stats = get_age_statistics(df_2015)
    
    if age_stats is not None:
        print('\n[연령별 일반가구원 통계]')
        print(age_stats)
        print()
    
    # 6. 남자 및 여자의 연령별 일반가구원 데이터를 꺽은선 그래프로 표현
    print('\n남자 및 여자의 연령별 일반가구원 꺽은선 그래프 생성 중...')
    gender_age_stats = get_gender_age_statistics(df_2015)
    
    if gender_age_stats is not None:
        create_gender_age_line_chart(gender_age_stats)
    
    # 7. 보너스: 인구 변화 트렌드 리포터 작성
    print('\n인구 변화 트렌드 리포터 작성 중...')
    if gender_age_stats is not None and age_stats is not None:
        create_trend_report(gender_age_stats, age_stats)
    
    print('\n작업 완료!')


if __name__ == '__main__':
    main()

