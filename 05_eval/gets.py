#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by devel on 2018/11/04.

_input = "123 456"
pos = 0

def gets_set_src(string):
    global _input
    _input = string


def gets ():
    global pos
    if len(_input) <= pos:
        return ''
    ch = _input[pos]
    pos += 1
    return ch