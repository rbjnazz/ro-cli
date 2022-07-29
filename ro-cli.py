#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
from os import system, name
from rich.console import Console


TYPE = ['integers', 'sequences', 'integer-sets']
CONSOLE = Console()


def clear_terminal():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


def message(msg=None, error=None, default=None):
    help_msg = '''
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
    err1 = 'Invalid character!\n'
    err2 = 'Some error occured! Try different settings...\n'
    defaults = ['Type: 0 ', 'Count: ', 'Min: ',
    'Max:', 'Col: ', 'Base: ']
    def_msg = f'{err1}{error}\n\nDefault settings will be used:\n'
    if msg == 0:
        return help_msg
    elif msg == 1:
        return f'{err2} {error}'
    elif msg == 2:
        for d, i in zip(default, range(0,6)):
            def_msg += f'{defaults[i]}{default[i]}\n'
        return def_msg
    else:
        return err1


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
            CONSOLE.print(f'No internet connection!\n\n{e}', style='#ED0800')
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


def usr_in(string, digit=True):
    if not digit:
        usr = input(string)
        clear_terminal()
        if usr.upper() == "S":
            write_settings()
        elif usr.upper() == "H":
            CONSOLE.print(message(0), style='#F4A460')
        elif usr.upper() == "Q":
            print('Quit!')
            exit()
        elif usr == "":
            with CONSOLE.status('[bold #FFC0CB]Getting data from random.org', spinner='material') as status:
                get_random = start()
                CONSOLE.print(f'[bold blue]\nResult:[/]\n\n[green]{get_random}')
        else:
            CONSOLE.print(f'[bold #ED0800]{message(3)}[/]', message(0), style='#F4A460')
    else:
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
                CONSOLE.print('[bold #ED0800]Type out of range![/]\n', message(0), style='#F4A460')
        except Exception as e:
            file.writelines(f'{i}\n' for i in default)
            clear_terminal()
            CONSOLE.print(message(2, e, default), style='#FFE900')


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


def start():
    p = read_settings()
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
        CONSOLE.print(message(1, e), style='red')
        write_settings()
        return 'please hit enter again'


while __name__ == '__main__':
    read_settings()
    rs = read_settings()
    usr_in(f'\nRANDOM-ORG-CLI {rs[0]} >>> ', False)

