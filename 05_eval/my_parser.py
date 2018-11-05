#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by devel on 2018/11/04.
from enum import IntEnum, auto

from gets import gets, gets_set_src


class Ltype(IntEnum):
    EOF = -1
    NUMBER = auto()
    SPACE = auto()
    EXECUTABLE_NAME = auto()
    LITERAL_NAME = auto()
    OPEN_CURLY = auto()
    CLOSE_CURLY = auto()
    END_OF_FILE = auto()
    UNKNOWN = auto()


class Token:
    def __init__(self, ltype=None, value=None):
        self._ltype = ltype
        self._value = value

    def get_ltype(self):
        return self._ltype

    def set_ltype(self, ltype):
        self._ltype = ltype

    def get_value(self):
        return self._value

    def set_value(self, value):
        self._value = value

    ltype = property(get_ltype, set_ltype)
    value = property(get_value, set_value)




def parse_one(prev_ch):
    ch = gets() if prev_ch == '' else prev_ch
    if not ch: return '', Token(ltype=Ltype.END_OF_FILE)

    if ch.isdigit():
        num = 0
        while ch.isdigit():
            num = num*10 + int(ch)
            ch = gets()
        return ch, Token(ltype=Ltype.NUMBER, value=num)

    elif ch.isalpha():
        word = ""
        while ch.isalpha() or ch.isalnum():
            word += ch
            ch = gets()
        return ch, Token(ltype=Ltype.EXECUTABLE_NAME, value=word)

    elif ch == '/':
        word = ch
        ch = gets()
        while ch.isalpha() or ch.isdigit():
            word += ch
            ch = gets()
        return ch, Token(ltype=Ltype.LITERAL_NAME, value=word)

    elif ch.isspace():
        while ch.isspace(): ch = gets()
        return ch, Token(ltype=Ltype.SPACE)

    elif ch == "{":
        ch = gets()
        return ch, Token(ltype=Ltype.OPEN_CURLY)

    elif ch == "}":
        ch = gets()
        return ch, Token(ltype=Ltype.CLOSE_CURLY)

    elif not ch:
        return ch, Token(ltype=Ltype.END_OF_FILE)

    else:
        return ch, Token(ltype=Ltype.UNKNOWN)


def parser_print_all():
    ch = ""
    while True:
        ch, token = parse_one(ch)

        if token.ltype == Ltype.END_OF_FILE:
            break

        if token.ltype == Ltype.NUMBER:
            print(f"num: {token.value}")
        elif token.ltype == Ltype.SPACE:
            print("space")
        elif token.ltype == Ltype.OPEN_CURLY:
            print("open curly brace")
        elif token.ltype == Ltype.CLOSE_CURLY:
            print("close curly brace")
        elif token.ltype == Ltype.EXECUTABLE_NAME:
            print(f"executable name: {token.value}")
        elif token.Ltype == Ltype.LITERAL_NAME:
            print(f"literal name {token.value}")
        else:
            print(f"Unknown type : {token.ltype}")



def main():
    input = "1 1 add"
    gets_set_src(input)
    parser_print_all()


if __name__ == '__main__':
    main()