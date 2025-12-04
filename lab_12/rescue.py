"""Rescue"""
def read_file(file_path):
    """Function reads file and returns dictionary
    >>> read_file('smart_people.txt')
    {'Marilyn vos Savant': 186, 'Judith Polgar': 170, \
'Elon Musk': 165, 'Quentin Tarantino': 163, 'Bill Gates': 160, \
"Conan O'Brien": 160, 'Will Smith': 157, 'Mark Zuckerberg': 152, \
'Barack Obama': 137, 'Emma Watson': 132}
    """
    d = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        file.readline()
        for line in file:
            name, iq = line.split(',')
            d[name] = int(iq.strip())
    return dict(sorted(d.items(), key = lambda x: (-x[1], x[0])))
def rescue_people(smarties, limit_iq):
    """Function returns the count of travel and who we need to transfer
    >>> rescue_people({"Steve Jobs": 160, "Albert Einstein": 160, \
"Sir Isaac Newton": 195, "Nikola Tesla": 189}, 500)
    (2, [['Sir Isaac Newton', 'Nikola Tesla'], ['Albert Einstein', 'Steve Jobs']])
    """
    stack = []
    queue = []
    limit = limit_iq

    smarties = sorted(smarties.items(), key = lambda x: (-x[1], x[0]))

    while smarties:
        queue = []
        limit = limit_iq
        left = []
        for el in smarties:
            if el[1] <= limit:
                queue.append(el[0])
                limit -= el[1]
            else:
                left.append(el)
        stack.append(queue)
        smarties = left

    return (len(stack), stack)

if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
