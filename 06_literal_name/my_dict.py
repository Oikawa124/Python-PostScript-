#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by devel on 2018/11/08.

from collections import namedtuple

KeyValue = namedtuple("KeyValue", ("key", "value"))

class MyDict:
    def __init__(self):
        self.dict = []

    def put(self, keyvalue):
        Exist, index = self._find_index(keyvalue.key)
        if Exist:
            self.dict[index] = keyvalue
        else:
            self.dict.append(keyvalue)

    def get(self, key):
        Exist, index = self._find_index(key)
        if Exist:
            return self.dict[index].value
        else:
            return False

    def print_all(self):
        for kv in self.dict:
            print(kv)

    def _find_index(self, key):
        for index in range(len(self.dict)):
            if self.dict[index].key == key:
                return True, index
        return False, None


def main():
    mydict = MyDict()
    mydict.put(KeyValue(1, "add"))
    print(mydict.get(1))
    mydict.print_all()


if __name__ == '__main__':
    main()
