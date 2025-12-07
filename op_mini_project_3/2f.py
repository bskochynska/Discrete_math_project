import os
import re
def read_file(match: str, pattern: str, folder: str, show_lines=None, only_show_counts=None):

    if not all(isinstance(el, str) for el in (match, pattern, folder)):
        return 'Введіть правильні аргументи'
    result = {}
    lst = []
    files = [f for f in os.listdir(folder) if os.path.isfile((os.path.join(folder, f)))]
    needed_files = [el for el in files if pattern in el]

    for elem in needed_files:
        lst.append(elem)
        try:
            with open(folder + '/' + elem, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                for i, line in enumerate(lines):
                    if re.search(match, line):
                        if show_lines:
                            result.setdefault(elem, []).append(f'{i}: {line.rstrip()}')
                        else:
                            result.setdefault(elem, []).append(line.rstrip())
        except FileNotFoundError:
            return 'Введіть коректний шлях до папки'
    a = sum(len(el) for el in result.values())
    if only_show_counts:
        return a
    return result

print(read_file('I', 'file', 'folder', only_show_counts=1))
