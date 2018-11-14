#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by devel on 2018/11/05.
import operator as op
from functools import partial

from element import to_elems, Element, Etype
from my_dict import Hashtable
from stack import Stack
from continuation import *


def to_char_gen(input_): return (x for x in input_)


class Evaluator:
    def __init__(self):
        self.stack = Stack()
        self.dict_ = Hashtable()
        register_primitives(self.stack, self.dict_, self)
        self.co_stack = CoStack()

    def eval(self, elems):
        for elem in elems:
            if elem.etype in {Etype.NUMBER, Etype.LITERAL_NAME, Etype.EXECUTABLE_ARRAY}:
                self.stack.push(elem)
            elif elem.etype == Etype.EXECUTABLE_NAME:
                if elem.value == "exec":
                    self.eval_exec_array(self.stack.pop().value)
                else:
                    is_exist, dict_value = self.dict_.get(elem)
                    if is_exist:
                        if dict_value.etype == Etype.FUNCTION:
                            dict_value.value()
                        elif dict_value.etype == Etype.EXECUTABLE_ARRAY:
                            self.eval_exec_array(dict_value.value)
                        else:
                            self.stack.push(dict_value)
                    else:
                        self.stack.push(elem)
            elif elem.etype == Etype.OPEN_CURLY:
                ex_arr = self.compile_exec_array(elems)
                if ex_arr:
                    self.stack.push(
                        Element(
                            etype=Etype.EXECUTABLE_ARRAY,
                            value=ex_arr
                        )
                    )
                else:
                    raise Exception("NO ELEMENT IN EXECUTABLE_ARRAY")
            else:
                raise Exception("NOT COME HERE")

    def compile_exec_array(self, elems):
        ex_arr = []
        for elem in elems:
            if elem.etype in {Etype.NUMBER, Etype.EXECUTABLE_NAME, Etype.LITERAL_NAME}:
                ex_arr.append(elem)
            elif elem.etype == Etype.OPEN_CURLY:
                rec_ex_arr = self.compile_exec_array(elems)
                if rec_ex_arr:
                    ex_arr.append(Element(
                            etype=Etype.EXECUTABLE_ARRAY,
                            value=rec_ex_arr)
                    )
                else:
                    raise Exception("NO ELEMENT IN EXECUTABLE_ARRAY")
            elif elem.etype == Etype.CLOSE_CURLY:
                break
            else:
                raise Exception("NOT COME HERE")
        return ex_arr

    def eval_exec_array(self, ex_arr):
        self.co_stack.push((ex_arr, 0))

        while not self.co_stack.is_empty():
            exec_array, pc = self.co_stack.pop()

            for i in range(pc, len(exec_array)):
                if exec_array[i].etype in {Etype.NUMBER, Etype.LITERAL_NAME, Etype.EXECUTABLE_ARRAY}:
                    self.stack.push(exec_array[i])
                elif exec_array[i].etype == Etype.EXECUTABLE_NAME:
                    if exec_array[i].value == "exec":
                        self.co_stack.push((exec_array, i+1))
                        self.co_stack.push((self.stack.pop().value, 0))
                        break
                    elif exec_array[i].value == "jmp":
                        pass
                    elif exec_array[i].value == "jmp_not_if":
                        pass
                    # jmp jmp_not_ifを実装する。
                    else:
                        is_exist, dict_value = self.dict_.get(exec_array[i])
                        if is_exist:
                            if dict_value.etype == Etype.FUNCTION:
                                dict_value.value()
                            elif dict_value.etype == Etype.EXECUTABLE_ARRAY:
                                self.co_stack.push((exec_array, i+1))
                                break
                            else:
                                self.stack.push(dict_value)
                        else:
                            self.stack.push(exec_array[i])
                else:
                    raise Exception("NOT COME HERE")


def register_primitives(stack, mydict, evaluator):
    def _pop_two_elems():
        num1 = stack.pop()
        num2 = stack.pop()
        return num1, num2

    def _binary_op(binop):
        elem1, elem2 = _pop_two_elems()

        ans = binop(elem2.value, elem1.value)

        ans = ans if type(ans) != bool else int(ans)

        stack.push(Element(etype=Etype.NUMBER, value=ans))

    add_ = partial(_binary_op, op.add)
    sub_ = partial(_binary_op, op.sub)
    mul_ = partial(_binary_op, op.mul)
    div_ = partial(_binary_op, op.floordiv)
    eq_  = partial(_binary_op, op.eq)
    neq_ = partial(_binary_op, op.ne)
    gt_  = partial(_binary_op, op.gt)
    ge_  = partial(_binary_op, op.ge)
    lt_  = partial(_binary_op, op.lt)
    le_  = partial(_binary_op, op.le)

    def def_op():
        val, key = _pop_two_elems()
        mydict.insert(key, val)

    def pop_op(): stack.pop()

    def exch_op():
        val1, val2 = _pop_two_elems()
        stack.push(val1)
        stack.push(val2)

    def dup_op():
        val = stack.pop()
        stack.push(val)
        stack.push(val)

    def index_op():
        val = stack.pop()
        index = val.value
        stack.push(stack.seek(index))

    # def exec_op():
    #     proc = stack.pop()
    #     evaluator.request_execute(proc)

    # def if_op():
    #     proc, bool_ = _pop_two_elems()
    #     if bool_.value:
    #         evaluator.eval(proc.value)
    #
    # def ifelse_op():
    #     proc2, proc1 = _pop_two_elems()
    #     bool_ = stack.pop()
    #
    #     if bool_.value:
    #         evaluator.eval(proc1.value)
    #     else:
    #         evaluator.eval(proc2.value)
    #
    # def repeat_op():
    #     proc, n = _pop_two_elems()
    #     cnt = n.value
    #
    #     for _ in range(cnt):
    #         evaluator.eval(proc.value)
    #
    # def while_op():
    #     body, cond = _pop_two_elems()
    #
    #     evaluator.eval(cond.value)
    #
    #     val = stack.pop()
    #
    #     while val.value:
    #         evaluator.eval(body.value)
    #         evaluator.eval(cond.value)
    #         val = stack.pop()
    #
    # func_list = [def_op, pop_op, exch_op, dup_op, index_op,
    #              exec_op, if_op, ifelse_op, repeat_op, while_op]
    func_list = [def_op]
    for func in func_list:
        mydict.insert(
            key=Element(etype=Etype.EXECUTABLE_NAME, value=f"{func.__name__[:-3]}"),
            value=Element(etype=Etype.FUNCTION, value=func)
        )

    func_list_partial = [v for v in locals().keys() if v.endswith("_")]

    for func in func_list_partial:
        mydict.insert(
            key=Element(etype=Etype.EXECUTABLE_NAME, value=f"{func[:-1]}"),
            value=Element(etype=Etype.FUNCTION, value=eval(func))
        )


def main():
    evaluator = Evaluator()
    elems = to_elems(to_char_gen("{{1 {1} exec} exec 1 1} exec"))
    evaluator.eval(elems)

    evaluator.stack.debug_print()
    #print(evaluator.dict_)


if __name__ == '__main__':
    main()
