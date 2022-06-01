import sys

sys.path.append('D:\\代码\\编译原理')
sys.path.append('D:\\代码')
from termcolor import *
import pandas as pd
from 语法分析.LL1 import left_dg, get_first, get_follow, back_date
import os
import ply
# 预测分析
from 词法分析 import auto_analyse
from graphviz import Digraph
import graphviz

global temp_name
temp_name = 0
global sz
sz = []


def C_mid_code(start_wf, wf_code, value_code):
    print(start_wf, wf_code, value_code)


def predict_analyse(df, dot, express, line_list, value_list, first):
    stack = ['#', 'S']
    express = [r for r in express if r != '' and r != '\n']
    express.append('#')
    action = []
    temp_stack = []
    temp_express = []
    temp_locate = {'S': ['Start 0']}
    add_nodes = []
    paren_nodes = {}  # 用于记录所有节点的父节点
    i = 0
    j = 0

    start_wf = ''  # 临时存储初始文法
    wf_code = []  # 临时存储中间代码
    value_code = []  # 临时存储文法的值
    creat_mid = False  # 是否确认创建中间代码
    cr_cnt = 0
    while True:
        if express[i] in ['\n', '', ' ']:
            if i + 1 < len(express):
                i += 1
            continue
        else:

            a = express[i]
            temp_stack.append(stack.copy())
            temp_express.append(express[i:])

        if len(stack) == 0:
            action.append('异常退出，请仔细检查代码后执行')
            break
        fl = stack[-1]
        X = stack.pop()

        # Vt终结符 ，Vn是非终结符
        # 如果在终结符里
        # 如果有多个同名的匹配项目，temlocate={‘S’:[]},par_nodes={‘S’:[]},这种!每次取最后一个值，作为地址
        if X in list(df.columns) and X != '#':
            if X == express[i]:
                action.append(f'匹配成功 : {X}')
                # print(X, '匹配成功')
                if creat_mid:
                    wf_code.append(X)
                    value_code.append(value_list[i])
                if creat_mid and X in [';', '}'] and start_wf in ['define_stmt', 'expression']:
                    C_mid_code(start_wf, wf_code, value_code)
                    creat_mid = False
                    wf_code = []
                    value_code = []
                elif creat_mid and X in ['}'] and start_wf in ['iteration_stmt', 'branch_stmt']:
                    C_mid_code(start_wf, wf_code, value_code)
                    creat_mid = False
                    wf_code = []
                    value_code = []

                if X != value_list[i]:
                    dot.node(temp_locate[X][-1], label=f'{X}', color='black')
                    dot.node(f'{value_list[i]} {j + 1}', label=value_list[i], shape='doublecircle', color='red')
                    dot.edge(temp_locate[X][-1], f'{value_list[i]} {j + 1}')
                    j += 1
                    dot.attr('node', shape='circle', color='black')

                else:

                    dot.node(temp_locate[X][-1], label=X, shape='doublecircle', color='red')
                    dot.attr('node', shape='circle', color='black')

                i += 1

            else:

                print(colored(f'行号{line_list[i]} 符号 {value_list[i]}  token {express[i]}  匹配失败. gameover,终结符匹配不成功,'
                              f'请仔细检查语法,将跳过此语句', 'red'))
                action.append(f'行号{line_list[i]} 符号 {value_list[i]}  token {express[i]}  匹配失败. gameover,终结符匹配不成功,'
                              f'请仔细检查语法,将跳过此语句')
                while True:
                    i += 1
                    if express[i] == ';' or express[i] == '{' or express[i] == '}':
                        i += 1
                        break
        elif X == '#':
            if X == '#' and X == express[i] and i == len(express) - 1:

                action.append('结束')
                break
            else:

                print('存在不能识别的终结符，请仔细检查语法')
                action.append('存在不能识别的终结符，请仔细检查语法')

                i = i + 1

        else:
            if isinstance(df.loc[X, express[i]], list):
                action.append('替代')

                if X in ['define_stmt', 'expression', 'iteration_stmt', 'branch_stmt'] and not creat_mid:
                    start_wf = X
                    mid_code = []
                    value_code = []
                    creat_mid = True
                t = df.loc[X, express[i]]
                t = t[0].split(' ')
                t = [r for r in t if r != '']
                tf = False
                for k in t:
                    paren_nodes[f'{k} {j + 1}'] = temp_locate[X][-1]
                    if k not in temp_locate.keys():
                        temp_locate[k] = [f'{k} {j + 1}']
                    else:
                        temp_locate[k].append(f'{k} {j + 1}')

                    if temp_locate[X][-1] != temp_locate[k][-1]:
                        dot.node(temp_locate[k][-1], label=f'{k}')
                        dot.edge(temp_locate[X][-1], temp_locate[k][-1])
                        add_nodes.append(temp_locate[k][-1])
                    else:
                        tf = True
                        dot.node(temp_locate[k][-1], label=f'{k}')
                        dot.edge(temp_locate[X][-2], temp_locate[k][-1])
                        add_nodes.append(temp_locate[k][-1])

                    j = j + 1
                if tf:
                    p = temp_locate[X].pop(-2)

                else:
                    p = temp_locate[X].pop()

                if len(t) > 0:
                    j += 1
                t = t[::-1]
                for k in t:
                    stack.append(k)


            elif '$' in first[X]['first']:
                j += 1
                if temp_locate[X][-1] in add_nodes:
                    # dot.node(temp_locate[X][-1], label=f'{X}', color='black')
                    dot.node(f'$ {j + 1}', label=f'$', shape='doublecircle', color='blue')
                    dot.edge(temp_locate[X][-1], f'$ {j + 1}')
                    add_nodes.append(temp_locate[X][-1])
                    p = temp_locate[X].pop()

                j += 1
                action.append('可替代为空')


            else:
                if express[i] not in first[X]['first'] and express[i] not in [';', '}', '#', '(', ')', '(']:
                    print('出错了，请检查语法', '符号', express[i], '不在', X, '的 first集合里')
                    action.append(f'出错了，请检查语法 。符号 {express[i]} 不在 {X},的 first集合里')

                else:
                    action.append('退出')

                i = i + 1

    return temp_stack, temp_express, action, dot


# 创建预测分析表
def create_predf(first, follow):
    col = []
    for r in follow.values():
        col.extend(r)
    col = list(set(col))
    index = list(set(follow.keys()))

    df = pd.DataFrame()
    for c in col:
        df[c] = ['error'] * len(index)
    df.index = index
    for i in index:
        for s, k in first[i]['pre'].items():
            k = list(set(k))
            df.loc[i, s] = [k]

        for s in follow[i]:
            if 'ε' in first[i]['first']:
                df.loc[i, s] = 'ε'
    df.fillna('error', inplace=True)
    return df


def get_tree(code, open_pdf):
    with open('D:/代码/编译原理/语法分析/static/C 文法2.txt') as f:
        wf_source = f.read()
    wf = wf_source.split('\n')
    # # 消除二义性  暂时没用了
    # wf = left_dg(wf)
    # wf = back_date(wf)
    first = get_first(wf, True)
    follow = get_follow(wf, first)

    follow = {f: g['follow'] for f, g in follow.items()}
    df = create_predf(first, follow)
    temp = auto_analyse.get_lex(code)
    temp = list(temp)[0]
    value_list = [t[0] for t in temp if len(t) > 0]
    token_list = [t[1] for t in temp if len(t) > 0]
    line_list = [t[2] for t in temp if len(t) > 0]
    # 开始预测分析
    dota = Digraph()
    temp_stack, temp_express, action, dot = predict_analyse(df, dota, express=token_list, line_list=line_list,
                                                            value_list=value_list, first=first)
    if open_pdf:
        df2 = pd.DataFrame()
        df2['stack'] = temp_stack
        df2['express'] = temp_express
        df2['action'] = action
        # dot.view()
        df2.to_csv('D:/代码/编译原理/语法分析/static/预测分析过程.csv', encoding='gbk')
        dot.view()
    return dot

# ε
# wf = ['E-> T G', 'G-> + T G', 'G-> ε ', 'T-> F H', 'H-> * F H', 'H-> ε', 'F-> ( E )', 'F-> i']
# wf = ['S-> a A S | b', 'A-> b A | ε']
# wf = ['E-> T | A', 'T-> F B', 'F-> i | ( E )','A-> + T A | ε','B-> * F B | ε']
# wf=['P-> b T d','T-> S F','F-> ; S F | ε','S-> N I C','N-> a','C-> I D','D-> e S | ε','I-> Z N','Z-> i c t']
# 测试
# code = '''
# int main ( ) {
# int a = 10 ;
# while ( a < 20 ) {
# a = a + 1 ;
# }
# }
# '''
#
# get_tree(code, True)
