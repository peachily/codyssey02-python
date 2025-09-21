import json

try:
  with open('mission_computer_main.log', 'r', encoding = 'utf-8') as f:
    log = f.read()
    log_lines = log.splitlines()
    log_comma = [line.split(',') for line in log_lines]
    header = log_comma[0]
    log_data = log_comma[1:]
    log_data.sort(key= lambda x: x[0], reverse=True)
    mission_computer = [dict(zip(header, data)) for data in log_data]

  with open ('mission_computer_main.json', 'w', encoding='utf-8') as f:
    json.dump(mission_computer, f, ensure_ascii=False, indent=4)

except FileNotFoundError:
  print('파일을 찾을 수 없습니다')
except UnicodeDecodeError:
  print('파일 인코딩 문제 발생')
except Exception as e:
  print('오류 내용: ', e)