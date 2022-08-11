#!/usr/bin/env python3
import requests
import yaml
from pathlib import Path
from bs4 import BeautifulSoup
from os import system, name
from rich.console import Console
from rich.panel import Panel


TYPE = ['integers', 'sequences', 'integer-sets']
CONSOLE = Console()
DIR = Path(__file__)


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
    err2 = 'Some error occured!\nTry different configuration \
            or use valid base number [2|8|10|16].\n'
    defaults = (f'{error}\nPress H for help...\n\n'
                'Default configuration will be used:\n')
    if msg == 0:
        return Panel.fit(help_msg, title='HELP', style='#F4A460', padding=2)
    elif msg == 1:
        return Panel.fit(f'{err2} {error}', title='ERROR!', padding=2)
    elif msg == 2:
        defaults += yaml.dump(default, sort_keys=False)
        return Panel.fit(defaults, title='Default Settings', padding=2)
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
            CONSOLE.print(Panel.fit(
                f'[bold red]No internet connection!\n\n{e}',
                title='CONNECTION ERROR!'))
            exit()


def rand_int(types, a, b, c, d, e):
    url = f'{types}/?num={a}&min={b}&max={c}' \
            f'&col={d}&base={e}&format=html&rnd=new'
    result = Parser(url).parse('pre')
    return result


def rand_seq(types, a, b, c):
    url = f'{types}/?min={a}&max={b}&col={c}&format=html&rnd=new'
    result = Parser(url).parse('pre')
    return result


def rand_sets(types, a, b, c, d):
    url = f'{types}/?sets={a}&num={b}&min={c}&max={d}' \
            '&seqnos=on&sort=on&order=index&format=html&rnd=new'
    result = Parser(url, True).parse('ul.data')
    return result


def usr_in(string, digit=True):
    try:
        if not digit:
            usr = input(string)
            clear_terminal()
            if usr.upper() == "S":
                write_settings()
            elif usr.upper() == "H":
                CONSOLE.print(message(0))
            elif usr.upper() == "Q":
                exit()
            elif usr == "":
                with CONSOLE.status(
                        '[bold #FFC0CB]Getting data from random.org',
                        spinner='dots2', speed=3.0):
                    get_random = generate_random()
                    CONSOLE.print(f'[bold cyan]RESULT:\n[yellow]{get_random}')
            else:
                CONSOLE.print(message(3), style='red')
                CONSOLE.print(message(0), style='#F4A460')
        else:
            usr = int(input(f'{string}: '))
            return usr
    except KeyboardInterrupt:
        exit()


def write_settings():
    default = {
            'Config': {
                'Type': TYPE[0],
                'Count': 1,
                'Min': 1,
                'Max': 100,
                'Column': 1,
                'Base': 10
                }
            }
    with open(DIR.parent / 'config.yaml', 'w') as file:
        try:
            types = usr_in('Type')
            params = {'Config': {'Type': TYPE[types]}}
            if types == 0:
                prompts = ['Count', 'Min', 'Max', 'Column', 'Base']
                for i in prompts:
                    params['Config'][i] = usr_in(i)
                yaml.dump(params, file, sort_keys=False)
            elif types == 1:
                prompts = ['Min', 'Max', 'Column']
                for i in prompts:
                    params['Config'][i] = usr_in(i)
                yaml.dump(params, file, sort_keys=False)
            elif types == 2:
                prompts = ['Count', 'Length', 'Min', 'Max']
                for i in prompts:
                    params['Config'][i] = usr_in(i)
                yaml.dump(params, file, sort_keys=False)
            else:
                yaml.dump(default, file, sort_keys=False)
                CONSOLE.print('[bold red]Type out of range!\n', message(0))
        except Exception as e:
            yaml.dump(default, file, sort_keys=False)
            clear_terminal()
            CONSOLE.print(message(2, e, default), style='#FFE900')


def read_settings():
    try:
        with open(DIR.parent / 'config.yaml') as file:
            data = yaml.safe_load(file)
            return list(data['Config'].values())
    except (FileNotFoundError, KeyError, yaml.error.YAMLError):
        write_settings()


def generate_random():
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
        exit()


while __name__ == '__main__':
    read_settings()
    rs = read_settings()
    CONSOLE.print(f'\n[b cyan]RANDOM[/] [b yellow]{rs[0].upper()}', end='')
    usr_in(': ', False)
