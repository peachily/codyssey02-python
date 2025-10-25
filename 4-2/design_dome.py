import math

# 전역 저장 (마지막 계산 결과)
LAST_DOME_RESULT = {}

# 재질 밀도 (g/cm^3)
MATERIAL_DENSITIES = {
    'glass': 2.4,
    'aluminum': 2.7,
    'carbon_steel': 7.85,
}

MARS_GRAVITY_FACTOR = 0.38  # 지구 대비


def sphere_area(diameter_m, material, thickness_cm=1.0):
    '반구체 돔의 곡면적(2πr^2)과 무게(화성 중력 반영)를 계산하여 딕셔너리로 반환'
    # 입력 검증 (보너스)
    if not isinstance(diameter_m, (int, float)):
        raise TypeError('diameter는 숫자여야 합니다.')
    if diameter_m <= 0:
        raise ValueError('diameter는 0보다 커야 합니다.')
    if not isinstance(thickness_cm, (int, float)):
        raise TypeError('thickness는 숫자여야 합니다.')
    if thickness_cm <= 0:
        raise ValueError('thickness는 0보다 커야 합니다.')
    mat_key = str(material).lower()
    if mat_key not in MATERIAL_DENSITIES:
        raise ValueError(f'지원되지 않는 재질입니다: {material}. 사용 가능: {list(MATERIAL_DENSITIES.keys())}')

    # 반지름 (m)
    r_m = diameter_m / 2.0
    # 반구 곡면적 (m^2) : 2 * pi * r^2
    area_m2 = 2.0 * math.pi * (r_m ** 2)

    # 질량 계산: area(cm^2) * thickness(cm) * density(g/cm^3)
    # 단위 변환: 1 m = 100 cm -> area_m2 -> area_cm2
    area_cm2 = area_m2 * 100.0 * 100.0
    density = MATERIAL_DENSITIES[mat_key]  # g/cm^3
    mass_g = area_cm2 * thickness_cm * density
    mass_kg = mass_g / 1000.0

    # 화성 중력 반영: 문제 요구에 따라 '무게'를 mass_kg * 0.38로 표기
    weight_on_mars_kg_equivalent = mass_kg * MARS_GRAVITY_FACTOR

    result = {
        'material': mat_key,
        'diameter_m': diameter_m,
        'thickness_cm': thickness_cm,
        'area_m2': area_m2,
        'mass_kg': mass_kg,
        'weight_on_mars_kg': weight_on_mars_kg_equivalent,
    }
    # 반환용 answer 변수 포함(요청사항 준수)
    answer = result
    return answer


def format_and_store_result(res):
    '전역 변수에 저장하고 요구 형식으로 출력'
    global LAST_DOME_RESULT
    LAST_DOME_RESULT = res.copy()
    # 출력 형식 예: 재질 ⇒ 유리, 지름 ⇒ 10, 두께 ⇒ 1, 면적 ⇒ 314.159, 무게 ⇒ 500.987 kg
    # 재질 표기는 원문(한글) 요청이 있었으므로 간단 맵핑 제공
    material_map = {
        'glass': '유리',
        'aluminum': '알루미늄',
        'carbon_steel': '탄소강',
    }
    mat_display = material_map.get(res['material'], res['material'])
    diameter_disp = res['diameter_m']
    thickness_disp = res['thickness_cm']
    area_disp = f'{res["area_m2"]:.3f}'
    weight_disp = f'{res["weight_on_mars_kg"]:.3f}'

    print(
        f'재질 ⇒ {mat_display}, 지름 ⇒ {diameter_disp}, 두께 ⇒ {thickness_disp}, '
        f'면적 ⇒ {area_disp}, 무게 ⇒ {weight_disp} kg'
    )


def input_with_exit(prompt):
    '사용자 입력 함수: 사용자가 exit 입력 시 예외로 탈출'
    val = input(prompt).strip()
    if val.lower() in ('exit', 'quit', '종료'):
        raise KeyboardInterrupt('사용자 종료')
    return val


def main_loop():
    '반복 실행: 사용자가 원할 때까지 계속. exit/quit로 종료.'
    print('=== Mars 돔 설계 프로그램 ===')
    print('종료하려면 "exit" 또는 "quit"을 입력하세요.')
    while True:
        try:
            raw_diameter = input_with_exit('지름을 입력하세요 (m, 예: 10): ')
            try:
                diameter = float(raw_diameter)
            except ValueError:
                print('올바른 숫자를 입력하세요.')
                continue

            raw_material = input_with_exit('재질을 입력하세요 (glass/aluminum/carbon_steel): ')
            material = raw_material.strip().lower()

            raw_thickness = input_with_exit('두께를 입력하세요 (cm, 기본 1 - 비워두면 1): ')
            if raw_thickness == '':
                thickness = 1.0
            else:
                try:
                    thickness = float(raw_thickness)
                except ValueError:
                    print('두께는 숫자여야 합니다.')
                    continue

            try:
                res = sphere_area(diameter, material, thickness)
            except Exception as e:
                print('입력 오류:', e)
                continue

            format_and_store_result(res)

        except KeyboardInterrupt:
            print('\n프로그램을 종료합니다.')
            break
        except Exception as e:
            print('예상치 못한 오류:', e)
            break


if __name__ == '__main__':
    main_loop()
