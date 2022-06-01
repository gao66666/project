import sys
sys.path.append('D:\\代码\\编译原理')
sys.path.append('D:\\代码')
sys.path.append('D:\\代码\\编译原理\\语法分析')
from turtle import clear
from LL1 import get_first, get_follow, left_dg, back_date
import networkx as nx
from networkx.drawing.nx_pydot import write_dot
from graphviz import Digraph
import graphviz


def plot(dot):
    write_dot(dot, "grid.dot")
    with open("grid.dot") as f:
        dot_graph = f.read()
    dot_graph = dot_graph.replace('name', 'label')
    dot2 = graphviz.Source(dot_graph)
    dot2.view('递归语法分析.pdf')
    return dot2


def match(s):
    if W.token[W.index] == s:
        W.getNext()
        return
    else:
        print('出错')
    return


# 这是一个简单的加减乘除赋值的递归程序，若不够请自行添加
def E(dot, cnt,pa):
    if W.index >= len(W.token):
        return

    dot.edge(pa, 'T{}'.format(cnt))
    pa='T{}'.format(cnt)
    T(dot, cnt + 1,pa)
    dot.edge(pa, 'E_{}'.format(cnt))
    pa='E_{}'.format(cnt)
    E_(dot, cnt + 1,pa)


def E_(dot, cnt,pa):
    if W.index >= len(W.token):
        return
    if W.token[W.index] == '+':
        match('+')
        dot.node('+    op{}'.format(cnt), label='+', color='red')
        dot.edge(pa, '+    op{}'.format(cnt))
        dot.edge(pa, 'T{}'.format(cnt))
        T(dot, cnt + 1,pa)
        dot.edge(pa, 'E{}'.format(cnt))
        E(dot, cnt + 1,pa)
    elif W.token[W.index] == '-':
        dot.node( '-    op{}'.format(cnt), label='-', color='red')
        dot.edge(pa, '-    op{}'.format(cnt))
        match('-')
        dot.edge(pa, 'T{}'.format(cnt))
        T(dot, cnt + 1,pa)
        dot.edge(pa, 'E{}'.format(cnt))
        E(dot, cnt + 1,pa)


def T(dot, cnt,pa):
    if W.index >= len(W.token):
        return

    dot.edge(pa, 'F{}'.format(cnt))
    pa = 'F{}'.format(cnt)
    F(dot, cnt + 1,pa)
    dot.edge(pa, 'T_{}'.format(cnt))
    pa = 'T_{}'.format(cnt)
    T_(dot, cnt + 1,pa)


def F(dot, cnt,pa):
    if W.index >= len(W.token):
        return
    if W.token[W.index] == '(':
        dot.node('(    link_sign{}'.format(cnt),label='(',color='red')
        dot.edge(pa, '(    link_sign{}'.format(cnt))
        match('(')

        E(dot, cnt + 1,pa)
        if W.token[W.index] == ')':
            dot.node(')    link_sign{}'.format(cnt), label=')', color='red')
            dot.edge(pa, ')    link_sign{}'.format(cnt))
            match(')')
    elif W.token[W.index].isdigit():

        dot.edge(pa, 'I{}'.format(cnt))
        pa='I{}'.format(cnt)
        I(dot, cnt + 1,pa)

    else:
        print('error')


def I(dot, cnt,pa):
    if W.index >= len(W.token):
        return

    if W.token[W.index].isdigit():
        if '.' not in W.token[W.index]:
            dig = int(W.token[W.index])
        else:
            dig = float(W.token[W.index])
        dot.edge(pa, f'{dig}    num{cnt}')
        match(str(dig))


def T_(dot, cnt,pa):
    if W.index >= len(W.token):
        return
    if W.token[W.index] == '*':
        dot.node('*  op{}'.format(cnt), label='*', color='red')
        dot.edge(pa, '*  op{}'.format(cnt))
        match('*')
        F(dot, cnt + 1,pa)
        T_(dot, cnt + 1,pa)
    elif W.token[W.index] == '/':
        dot.node('/   op{}'.format(cnt), label='/', color='red')
        dot.edge(pa, '/   op{}'.format(cnt))
        match('/')
        F(dot, cnt + 1,pa)
        T_(dot, cnt + 1,pa)
    elif W.token[W.index] == '=':
        dot.node('=         op{}'.format(cnt), label='=', color='red')
        dot.edge(pa, '=         op{}'.format(cnt))
        match('=')
        dot.edge(pa, 'E{}'.format(cnt))
        E(dot, cnt + 1,pa)
        dot.edge(pa, 'T_{}'.format(cnt))
        T_(dot, cnt + 1,pa)


class WF:
    def __init__(self, wf, token):
        wf = left_dg(wf)
        wf = list(set(wf))
        wf = back_date(wf)
        wf = list(set(wf))
        print('更正后的文法是', wf)
        first = get_first(wf, False)
        print(first)
        follow = get_follow(wf, first)
        follow = {f: g['follow'] for f, g in follow.items()}
        print(follow)
        self.wf = wf
        self.fz = [w.split('->')[0] for w in wf]
        self.first = first
        self.follow = follow
        self.token = [r for r in token.split(' ') if r != '']
        self.index = 0

    def getNext(self):
        t = self.token[self.index]
        self.index += 1
        return t


# wf_source = ['E-> T E_'
#     , 'E_-> + T E_ | ε'
#     , 'T-> F T_'
#     , 'T_-> * F T_ | ε'
#     , 'F-> ( E ) | i']
def Digui_ana(text):
    wf_source = ['E-> E + T | T', 'E-> E - T | T', 'T-> T * F | F', 'T-> T / F | F', 'T-> T = E', 'F-> i | ( E )',
                 'i-> 1 | 2 | 3 | 4 | '
                 '5 | 6 | 7 | 8 | 9']
    global W
    W = WF(wf_source, text)
    dot = Digraph()
    dot.node('E0')
    cnt = 0
    E(dot, cnt + 1,pa='E0')
    dot.view()
