try:
  with open('mission_computer_main.log', 'r', encoding = 'utf-8') as f:
    log = f.read()
    log_lines = log.splitlines()
    log_comma = [line.split(',') for line in log_lines]
  print(log_comma)

except FileNotFoundError:
  print()
except UnicodeDecodeError:
  print()
except Exception as e:
  print('오류 내용: ', e)