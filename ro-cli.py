from bs4 import BeautifulSoup
import requests
from os import system, name


TYPE = ['integers', 'sequences', 'integer-sets']


def clear_terminal():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


def help():
    help_text = '''
    Type S for settings, H for help, Q to quit, hit ENTER to start:

    ABOUT SETTINGS:
    Type - 0 1 2
        0 Integers: makes random numbers in configurable intervals.
        1 Sequence: will randomize an integer sequence of your choice.
        2 Integer-sets: makes sets of non-repeating integers.

        The randomness comes from atmospheric noise,
        which for many purposes is better than the
        pseudo-random number algorithms typically used in computer programs.

    Count - Generate random integers (maximum 107,000).
    Length - How many unique random integer on each (Integer-sets).
    Min - Minimum value.
    Max - Maximum value.
    Column - Number of columns (output).
    Base - 2 Binary, 8 Octal, 10 Decimal, 16 Hexadecimal
    '''
    print(help_text)


def rand_int(types, a, b, c, d, e):
    url = f'https://www.random.org/{types}/?num={a}&min={b}&max={c}&col={d}&base={e}&format=html&rnd=new'
    try:
        req_result = requests.get(url)
        random_org = BeautifulSoup(req_result.text, 'html.parser')
        return random_org.find('pre').string
    except requests.ConnectionError as e:
        print(f'No internet connection!\n\n{e}')
        exit()


def rand_seq(types, a, b, c):
    url = f'https://www.random.org/{types}/?min={a}&max={b}&col={c}&format=html&rnd=new'
    try:
        req_result = requests.get(url)
        random_org = BeautifulSoup(req_result.text, 'html.parser')
        return random_org.find('pre').string
    except requests.ConnectionError as e:
        print(f'No internet connection!\n\n{e}')
        exit()


def rand_sets(types, a, b, c, d):
    url = f'https://www.random.org/{types}/?sets={a}&num={b}&min={c}&max={d}&seqnos=on&sort=on&order=index&format=html&rnd=new'
    try:
        req_result = requests.get(url)
        random_org = BeautifulSoup(req_result.text, 'html.parser')
        data = random_org.find(class_='data')
        result = ''
        for i in data.find_all('li'):
            result += i.string + '\n'
        return result
    except requests.ConnectionError as e:
        print(f'No internet connection!\n\n{e}')
        exit()


def write_settings():
    default = [TYPE[0], 1, 1, 100, 1, 10]
    with open('settings.txt', mode='w', encoding='utf-8') as file:
        try:
            types = int(input('Type: '))
            if types == 0:
                count = int(input('Count: '))
                min = int(input('Min: '))
                max = int(input('Max: '))
                col = int(input('Column: '))
                base = int(input('Base: '))
                params = [TYPE[types], count, min, max, col, base]
                for i in params:
                    file.writelines(f'{i}\n')
            elif types == 1:
                min = int(input('Min: '))
                max = int(input('Max: '))
                col = int(input('Column: '))
                params = [TYPE[types], min, max, col]
                for i in params:
                    file.writelines(f'{i}\n')
            elif types == 2:
                count = int(input('Count: '))
                length = int(input('Length: '))
                min = int(input('Min: '))
                max = int(input('Max: '))
                params = [TYPE[types], count, length, min, max]
                for i in params:
                    file.writelines(f'{i}\n')
            else:
                for i in default:
                    file.writelines(f'{i}\n')
        except Exception as e:
            for i in default:
                file.writelines(f'{i}\n')
            clear_terminal()
            print(f'Imvalid character!\nError: {e}')
            print(f'''
    Default settings will be used:
    Type: 0 {default[0]}
    Count: {default[1]}
    Min: {default[2]}
    Max: {default[3]}
    Col: {default[4]}
    Base: {default[5]}
    ''')


def read_settings():
    try:
        with open('settings.txt', mode='r', encoding='utf-8') as file:
            lines = file.readlines()
            ris = []
            for line in lines:
                ris.append(line.rstrip('\n'))
            if ris is None or len(ris) == 0:
                write_settings()
            elif ris[0] == '':
                write_settings()
            else:
                return ris
    except FileNotFoundError:
        write_settings()


def start(rsp):
    p = rsp
    try:
        if p[0] == 'integers':
            intr = rand_int(p[0], p[1], p[2], p[3], p[4], p[5])
            return intr
        elif p[0] == 'sequences':
            seqr = rand_seq(p[0], p[1], p[2], p[3])
            return seqr
        elif p[0] == 'integer-sets':
            setsr = rand_sets(p[0], p[1], p[2], p[3], p[4])
            return setsr
    except Exception as e:
        print('some error occured!\n', e)
        exit()


while __name__ == '__main__':
    read_settings()
    rs = read_settings()
    usr_input = input(f'\nRANDOM-ORG-CLI {rs[0]} >>> ')
    clear_terminal()
    if usr_input.upper() == "S":
        write_settings()
    elif usr_input.upper() == "H":
        help()
    elif usr_input.upper() == "Q":
        print('Quit!')
        exit()
    elif usr_input == "":
        x = start(rs)
        print(f'\nResult:\n\n{x}')
    else:
        print('Unknown command!')
        help()
