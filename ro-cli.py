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


class Parser:
    site = 'https://www.random.org/'

    def __init__(self, url, cls_data=False):
        self.url = self.site + url
        self.cls_data = cls_data

    def parse(self, tag):
        try:
            req = requests.get(self.url)
            ro = BeautifulSoup(req.text, 'html.parser')
            if not self.cls_data:
                return ro.find(tag).string
            else:
                result = ''
                for li in ro.select(tag):
                    result += li.get_text()
                return result
        except requests.ConnectionError as e:
            print(f'No internet connection!\n\n{e}')
            exit()


def rand_int(types, a, b, c, d, e):
    url = f'{types}/?num={a}&min={b}&max={c}&col={d}&base={e}&format=html&rnd=new'
    result = Parser(url).parse('pre')
    return result


def rand_seq(types, a, b, c):
    url = f'{types}/?min={a}&max={b}&col={c}&format=html&rnd=new'
    result = Parser(url).parse('pre')
    return result


def rand_sets(types, a, b, c, d):
    url = f'{types}/?sets={a}&num={b}&min={c}&max={d}&seqnos=on&sort=on&order=index&format=html&rnd=new'
    result = Parser(url, True).parse('ul.data')
    return result


def usr_in(string):
    usr = int(input(string))
    return usr


def write_settings():
    default = [TYPE[0], 1, 1, 100, 1, 10]
    with open('settings.txt', mode='w', encoding='utf-8') as file:
        try:
            types = usr_in('Type: ')
            if types == 0:
                prompts = [
                'Count: ', 'Min: ', 'Max: ',
                'Column: ', 'Base (2 8 10 16): '
                ]
                params = [TYPE[types]]
                for i in prompts:
                    params.append(usr_in(i))
                file.writelines(f'{i}\n' for i in params)
            elif types == 1:
                prompts = ['Min: ', 'Max: ','Column: ']
                params = [TYPE[types]]
                for i in prompts:
                    params.append(usr_in(i))
                file.writelines(f'{i}\n' for i in params)
            elif types == 2:
                prompts = [
                'Count: ', 'Length: ',
                'Min: ', 'Max: '
                ]
                params = [TYPE[types]]
                for i in prompts:
                    params.append(usr_in(i))
                file.writelines(f'{i}\n' for i in params)
            else:
                file.writelines(f'{i}\n' for i in default)
        except Exception as e:
            file.writelines(f'{i}\n' for i in default)
            clear_terminal()
            print(f'Invalid character!\nError: {e}')
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


def start(params):
    p = params
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
        print('Some error occured! Try different settings...\n', e)
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
        get_random = start(rs)
        print(f'\nResult:\n\n{get_random}')
    else:
        print('Unknown command!')
        help()
