import argparse
import sys
def main():

    uppercase_letters = ["А", "Б", "В", "Г", "Ґ", "Д", "Е", "Є", "Ж", "З", "И", \
"І", "Ї", "Й", "К", "Л", "М", "Н", "О", "П", "Р", "С", \
"Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ь", "Ю", "Я"]

    lowercase_letters = ["а", "б", "в", "г", "ґ", "д", "е", "є", "ж", "з", "и", \
"і", "ї", "й", "к", "л", "м", "н", "о", "п", "р", "с", \
"т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ь", "ю", "я"]

    parser = argparse.ArgumentParser(
        description='Програма для шифрування/дешифрування файлів шифром Цезаря з підтримкою кирилиці та латиниці.')

    parser.add_argument(
        'file_path',
        help='Шлях до файлу, який необхідно обробити.')

    parser.add_argument(
        '--offset',
        type=int,
        default=13,
        help='Величина зсуву (ціле число). За замовчуванням: 13.')

    parser.add_argument(
        '--decrypt',
        action='store_true',
        help='Включає режим дешифрування.')

    parser.add_argument(
        '--inplace',
        action='store_true',
        help='Якщо присутній, перезаписує вихідний файл результатом.')

    args = parser.parse_args()
    shift = args.offset
    if args.decrypt:
        shift = -args.offset

    try:
        with open(args.file_path, 'r', encoding='utf-8') as file:
            lines = file.read()
            result = ''
            for el in lines:
                if 65 <= ord(el) <= 90:
                    result += chr(((ord(el)-65) + shift)%26 + 65)
                elif 97 <= ord(el) <= 122:
                    result += chr(((ord(el)-97) + shift)%26 + 97)
                elif el in uppercase_letters:
                    result += uppercase_letters[(uppercase_letters.index(el) + shift)%33]
                elif el in lowercase_letters:
                    result += lowercase_letters[(lowercase_letters.index(el) + shift)%33]
                else:
                    result += el
    except FileNotFoundError:
        print(f'Помилка: Файл "{args.file_path}" не знайдено.')
        sys.exit(1)
    except Exception as e:
        print(f'Помилка при читанні файлу: {e}')
        sys.exit(1)
    processed_text = "".join(result)
    if args.inplace:
        try:
            with open(args.file_path, 'w', encoding='utf-8') as f:
                f.write(processed_text)
            print(f"Операція '{'Дешифрування' if args.decrypt else 'Шифрування'}' успішно виконана на місці.")
        except Exception as e:
            print(f'Помилка при записі файлу: {e}')
            sys.exit(1)

    else:
        print(processed_text)

if __name__ == '__main__':
    main()
