import json

try:
  with open('mission_computer_main.log', 'r', encoding = 'utf-8') as f:
    log = f.read()
    log_lines = log.splitlines()
    log_comma = [line.split(',') for line in log_lines]
    header = log_comma[0]
    log_data = log_comma[1:]

    print('=== 원본 로그 리스트 ===')
    for item in log_data:
      print(item)

    print('\n=== 로그 정렬 방식 선택 ===')
    print('1. 최신 로그부터 보기')
    print('2. 오래된 로그부터 보기')
    option = input('번호를 입력하세요 (1 또는 2): ')
    order = True if option == "1" else False
    log_data.sort(key= lambda x: x[0], reverse=order)

    print('\n=== 정렬된 로그 리스트 ===')
    for item in log_data:
      print(item)

    mission_computer = [dict(zip(header, data)) for data in log_data]

  with open ('mission_computer_main.json', 'w', encoding='utf-8') as f:
    json.dump(mission_computer, f, ensure_ascii=False, indent=4)
  
  keywords = ['unstable', 'explosion', 'leak', 'high temperature', 'Oxygen']

  danger_logs = []

  for data in log_data:
    for keyword in keywords:
      if keyword in data[2]:
        danger_logs.append(data)
        break
      
  print('\n=== 위험 로그 리스트 ===')
  if danger_logs:
    for danger in danger_logs:
      print(danger)

    danger_log_dicts = [dict(zip(header, data)) for data in danger_logs]
    with open('danger_logs.json', 'w', encoding='utf-8') as f:
      json.dump(danger_log_dicts, f, ensure_ascii=False, indent=4)

  else:
    print('위험 키워드가 포함된 로그는 없습니다.')

  with open ('log_analysis.md', 'w', encoding='utf-8') as f:
    f.write('# Mission Computer Log Analysis Report\n\n')
    f.write('## 1. 로그 개요\n')
    f.write('- 분석 대상 파일: mission_computer_main.log\n')
    f.write(f'- 총 로그 개수: {len(log_data)}개\n')
    f.write('- 분석 기준: 시간 순서 및 위험 키워드(폭발, 누출, 고온, Oxygen 등)\n\n')
    f.write('## 2. 주요 위험 로그\n')
    if danger_logs:
      for danger in danger_logs:
        f.write(f'- {danger[0]} → {danger[2]}\n')
    else:
      f.write('- 위험 로그가 없습니다.\n')
    f.write('\n## 3. 사고 원인 추론\n')
    f.write('- 발사 및 궤도 진입 과정은 정상적으로 수행되었음.\n')
    f.write('- 그러나 임무 종료 직후 산소 탱크에서 불안정 현상이 보고됨.\n')
    f.write('- 불안정 상태가 해결되지 못하고 폭발로 이어짐.\n')
    f.write('- 이는 산소 공급 장치의 구조적 결함 또는 재진입 후 과열 문제일 가능성이 있음.\n\n')

    f.write('## 4. 결론\n')
    f.write('본 사고의 근본 원인은 **산소 탱크 불안정 → 산소 폭발**로 이어진 것으로 추정된다.\n')
    f.write('임무 자체는 위성 배치까지 성공했으나, 산소 공급 시스템의 취약점으로 인해 안전성이 크게 저해되었음.\n')
    f.write('향후 동일한 사고 방지를 위해 **산소 탱크 설계 개선 및 재진입 환경에서의 안정성 검증 강화**가 필요하다.\n')

  print('\n=== 로그 검색 ===')
  search = input('\n검색어를 입력하세요: ')
  if search:
    result = []
    for log in log_data:
      if search.lower() in log[2].lower():
        result.append(log)
    
    print('\n-- 검색 결과 --')
    if result:
      print(f'총 {len(result)}개의 로그가 검색되었습니다.')
      for log in result:
        print(log)
    else:
      print('해당 검색어가 포함된 로그는 없습니다.')
  else:
    print('검색어가 입력되지 않았습니다.')

except FileNotFoundError:
  print('파일을 찾을 수 없습니다')
except UnicodeDecodeError:
  print('파일 인코딩 문제 발생')
except Exception as e:
  print('오류 내용: ', e)