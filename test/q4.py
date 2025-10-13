# design_dome05.py
# 예외처리 우선순서 반영 + 계산식 try/except 추가
import math


def _normalize_material_kor(text: str) -> str:
    """앞뒤 + 중간 공백 제거"""
    if not isinstance(text, str):
        return ''
    return ''.join(text.strip().split())


def sphere_area(diameter: float, material: str, thickness: float = 1.0) -> tuple[float, float]:
    """반구체 돔의 표면적(π·d²)과 화성 중력 기준 무게 계산"""
    # === 간단 유효성 검사(타입체크 X, 값/허용치만 확인) ===
    if diameter <= 0:
        raise ValueError
    
    if thickness <= 0:
        raise ValueError

    material_kor = _normalize_material_kor(material)
    densities_g_per_cm3 = {'유리': 2.4, '알루미늄': 2.7, '탄소강': 7.85}
    if material_kor not in densities_g_per_cm3:
        raise ValueError

    # === 계산(문제식 그대로, 예외 발생 시 그대로 전파) ===
    try:
        area_m2 = math.pi * (diameter ** 2)               # π·d² (m²)
        volume_cm3 = (area_m2 * 10000.0) * thickness      # m²→cm² 후 두께(cm) 곱
        mass_kg = densities_g_per_cm3[material_kor] * volume_cm3 / 1000.0
        mars_weight_kg = mass_kg * 0.38
        return area_m2, mars_weight_kg
    except Exception:
        raise  ## check


def main() -> None:
    try:
        # 지름(m)
        d_raw = input('지름(m)을 입력하세요:').strip()
        if not d_raw:
            print('Invalid input.'); return  #ddd
        try:
            diameter_m = float(d_raw)
        except Exception:
            print('Invalid input.'); return
        if diameter_m <= 0:
            print('Invalid input.'); return

        # 재질(한글만 허용, 공백 정규화)
        material_in = input('재질(유리/알루미늄/탄소강)을 입력하세요:').strip()
        material_kor = _normalize_material_kor(material_in) #dd
        if material_kor not in ('유리', '알루미늄', '탄소강'):
            print('Invalid input.'); return

        # 두께(cm) — 빈 입력이면 1.0
        t_raw = input('두께(cm)를 입력하세요(기본값 1):').strip()
        if t_raw == '':
            thickness_cm = 1.0
        else:
            try:
                thickness_cm = float(t_raw)
            except Exception:
                print('Invalid input.'); return
            if thickness_cm <= 0:
                print('Invalid input.'); return

        # 계산
        try:
            area_m2, mars_weight_kg = sphere_area(diameter_m, material_kor, thickness_cm)
        except ValueError:
            print('Invalid input.'); return
        except Exception:
            print('Processing error.'); return

        # 정확히 한 줄 출력
        print(f'재질 : {material_kor}, 지름 : {diameter_m:g}, 두께 : {thickness_cm:g}, 면적 : {area_m2:.3f}, 무게 : {mars_weight_kg:.3f} kg')

    except Exception:
        print('Processing error.')


if __name__ == '__main__':
    main()