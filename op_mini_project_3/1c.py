def read_file(filename, n, decrypt=None, inplace=None):

    uppercase_letters = ["А", "Б", "В", "Г", "Ґ", "Д", "Е", "Є", "Ж", "З", "И", \
"І", "Ї", "Й", "К", "Л", "М", "Н", "О", "П", "Р", "С", \
"Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ь", "Ю", "Я"]

    lowercase_letters = ["а", "б", "в", "г", "ґ", "д", "е", "є", "ж", "з", "и", \
"і", "ї", "й", "к", "л", "м", "н", "о", "п", "р", "с", \
"т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ь", "ю", "я"]

    if not isinstance(filename, str):
        return 'Введіть коректний шлях до файлу'
    if not isinstance(n, int):
        return 'Введіть коректне число зміщення'

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            line = file.read()
            result = ''
            if decrypt:
                n = -n
            for i in line:
                if 65 <= ord(i) <= 90:
                    result += chr(((ord(i)-65) + n)%26 + 65)
                elif 97 <= ord(i) <= 122:
                    result += chr(((ord(i)-97) + n)%26 + 97)
                elif i in uppercase_letters:
                    result += uppercase_letters[(uppercase_letters.index(i) + n)%33]
                elif i in lowercase_letters:
                    result += lowercase_letters[(lowercase_letters.index(i) + n)%33]
                else:
                    result += i
    except FileNotFoundError:
        return 'Message had been writen to file'

    if inplace:
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(result)
        except FileNotFoundError:
            return 'Message had been writen to file'

        return result

print(read_file('code', 4, decrypt=1, inplace=1))
