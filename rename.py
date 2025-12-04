"""Rename"""
def read_file(filename: str) -> dict:
    """Function return dict
    >>> list(read_file("renamed_locations_24.txt").keys())[13]
    'с.Грабівці'
    """
    dictionary = {}
    lines =[]
    district, region, rada, before, after = "", "", "", "", ""
    with open(filename, 'r', encoding='utf-8') as file:
        line = file.readline()
        while '1.' not in line:
            line = file.readline()
        while '2.' not in line:
            line = file.readline().strip()
            line = line.replace("село", "с.")
            line = line.replace("місто", "м.")
            line = line.replace("селище", "с-ще ")
            line = line.replace("селище міського типу", "смт ")
            lines.append(line.split())

        i = 1
        for row in lines:
            for el in row:
                el.replace("кого", "кий")
                el.replace("ої", "а")
                row[-1] = row[-1].replace('.', '')
                if el.startswith(f"{i})"):
                    region = row[2].replace("ій", "а") + " " + \
                    row[3].replace("і", "ь").replace(":", "")
                    i += 1
                if el == "району":
                    district = el.replace("у", "") + " " + \
                        "".join(row[row.index(el) - 1])
                    before = " ".join(row[:row.index(el) - 1])
                if el == "ради":
                    rada = "".join(row[row.index(el) - 2]) + " " + \
                    "".join(row[row.index(el) - 1]) + " " + el.replace("и", "а")
                if el == "на":
                    if row[row.index(el)+1] == "смт" or row[row.index(el)+1] == "с-ще":
                        after = row[row.index(el)+1] + " " + \
                            " ".join(row[row.index(el) + 2:]).rstrip(';')
                    else:
                        after = row[row.index(el)+1] + " ".join(row[row.index(el) + 2:]).rstrip(';')
            if row == lines[0]:
                continue
            if ("району" not in row) and ("ради" not in row):
                dictionary.setdefault((region, "" ,before), after)
            elif ("району" not in row) and ("ради" in row):
                dictionary.setdefault((region, rada, before), after)
            elif ("району" in row) and ("ради" in row):
                dictionary.setdefault((region, district, before, rada), after)
            elif ("району" in row) and ("ради" not in row):
                dictionary.setdefault((region, district, before, rada), after)
            # del dictionary[list(dictionary.keys())[0]]


    return dictionary

def write_csv_file(info: dict, filename: str):
    """Function writes to file

    >>> import tempfile
    >>> data = {
    ...     ('Вінницька область', 'Барський район', 'с.Червоне'): 'с.Грабівці',
    ... }
    >>> with tempfile.NamedTemporaryFile(mode='w+', suffix=".txt", delete=False) as temp_input:
    ...     temp_name = temp_input.name
    >>> write_csv_file(data, temp_name)
    >>> with open(temp_name[:-4] + '.csv', 'r', encoding='utf-8') as f:
    ...     lines = f.readlines()
    >>> lines[0].strip()
    'regionname,areaname,oldname,newname'
    >>> print(lines[1].strip())
    Вінницька область,Барський район,с.Червоне,с.Грабівці
    """
    filename = filename.replace(".txt", ".csv")
    with open(filename, 'w', encoding='utf-8') as file:
        file.write('regionname,areaname,oldname,newname\n')
        for el, renamed in info.items():
            file.write(f'{el[0]},{el[1]},{el[2]},{renamed}\n')


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
