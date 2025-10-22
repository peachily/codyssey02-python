CIPHER_TEXT = 'erkekr, DDrker ereeiic efkef'

def caesar_cipher_decode(target_text: str) -> list[str]:
    if not isinstance(target_text, str):
        raise ValueError
    if target_text == '':
        raise ValueError
    results = []
    for i in range(26):
        decoded = []
        for ch in target_text:
            if 'a' <= ch <= 'z':
                code = ord(ch) - i
                if code < ord('a'):
                    code += 26
                decoded.append(chr(code))
            else:
                decoded.append(ch)
        results.append(''.join(decoded))
    return results

def main() -> None:
    try:
        decode_passwords = caesar_cipher_decode(CIPHER_TEXT)
        for m, password in enumerate(decode_passwords):
            print(f"{m}: {password}")
        raw = input()
        if not isinstance(raw, str):
            raise ValueError
        s = raw.strip()
        if s == '':
            raise ValueError
        if not s.isdigit():
            raise ValueError
        idx = int(s)
        if not 0 <= idx <= 25:
            raise ValueError
        print(f"Result: {decode_passwords[idx]}")
    except ValueError:
        print('Invalid input.')
        return
    except Exception:
        print('Processing error.')
        return

if __name__ == "__main__":
    main()
