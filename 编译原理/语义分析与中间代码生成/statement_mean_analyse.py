import sys

sys.path.append('D:\\代码\\编译原理')
sys.path.append('D:\\代码')
import pandas as pd
from 语法分析 import LL1
from 语法分析.predict_analyse import get_tree
from 词法分析 import auto_analyse
import networkx as nx
from networkx.drawing.nx_pydot import read_dot

def crea_mcode(code):
    import sys
    sys.path.append('D:\\代码\\编译原理')
    sys.path.append('D:\\代码')

    import pandas as pd
    import networkx as nx
    from networkx.drawing.nx_pydot import read_dot
    d = read_dot('D:/代码/编译原理/语义分析与中间代码生成/static/source.dot')
    table = []

    fz = ['S', 'funcs', 'func', 'type', 'args', 'arg', 'func_body', 'block', 'define_stmts', 'define_stmt', 'init',
          'vars', 'stmts', 'stmt', 'assign_stmt', 'jump_stmt', 'iteration_stmt', 'branch_stmt', 'result',
          'logical_expression', 'bool_expression', 'lop', 'case_stmts', 'case_stmt', 'default_stmt', 'block_stmt',
          'isnull_expr1', 'isnull_expr2', 'IDN_NUM', 'isnull_expr', 'expression', 'operation', 'compare_op', 'equal_op',
          'value', 'value_', 'item', 'item_', 'factor', 'call_func', 'es', 'isnull_es', 'const', 'num_const']

    def get_zj(d, start, value):
        key = list(dict(d[start]).keys())
        if len(key) == 0:
            value.append(start.split(' ')[0])
            return value
        else:
            for k in key:
                if k[0] != '$':
                    value = get_zj(d, k, value)

        return value

    def link_jia(sy, ck, qd, zd):
        for q in qd:

            for m, n in enumerate(sy[q]):
                print(m, n)
            if n[-1] == 'sentence_unknow':
                sy[q][m][-1] = zd
            else:
                print('有问题', qd, zd, print(sy[q]))
        print(sy)
        return sy

    def copy_mid(sy, snum, target_sum):
        jck = []
        for s in sy[target_sum]:
            if s[-1] == target_sum:
                jck.append(snum)
            sy[f'sentence{snum}'] = s
            snum += 1

        return sy, snum, jck

    def get_allsy(sy, first, final):
        temp = []
        for i in range(first, final):
            temp.append(sy[f'sentence{i}'])
        return temp

    def deal_bool_expression(code, num, snum, sy, ck):
        ja = []
        first = snum
        jck = []
        symbol = ['>', '<', '==', '!=', '>=', '<=']
        idn_stack = []
        com_stack = []
        last_z = ''
        last_j = ''
        if_index = code.index('if')
        hual_index = code.index('{')
        huar_index = code.index('}')
        bool_expression = code[if_index + 2:hual_index - 1]
        real_z = code[hual_index + 1:huar_index]
        if 'else' in code:
            else_index = code.index('else')
            else_rindex = else_index
            while code[else_rindex] != '}':
                else_rindex += 1

            real_j = code[else_index + 2:else_rindex]

        elif huar_index < len(code) - 1:
            real_j = code[huar_index + 1]
        else:
            real_j = 'sentence_unknow'

        for s in bool_expression:
            if s.isalpha() or s.isdigit() or s.isidentifier():
                idn_stack.append(s)
            elif s in symbol:
                com_stack.append(s)

        compare = com_stack.pop()
        b = idn_stack.pop()
        a = idn_stack.pop()

        if 'else' not in code:
            sy[f'sentence{snum}'] = [f'j{compare}', a, b, f'sentence{snum + 2}']
            snum += 1
            sy[f'sentence{snum}'] = ['j', ' ', ' ', 'sentence_unknow']
            jck = [f'sentence{snum}']
            snum += 1
            for r in real_z:
                if 'sentence' in r:
                    print(r, snum)
                    sy, snum, ja = copy_mid(sy, snum, r)
            if len(ja) != 0:
                for j in ja:
                    sy[f'sentence{j}'] = ['j', ' ', ' ', 'sentence_unknow']
                    jck.append(f'sentence{j}')
            else:
                sy[f'sentence{snum}'] = ['j', ' ', ' ', 'sentence_unknow']
                jck.append(f'sentence{snum}')
                snum += 1



        else:
            sy[f'sentence{snum}'] = [f'j{compare}', a, b, f'sentence{snum + 2}']

            L = 0
            for r in real_z:
                if 'sentence' in r:
                    L += len(sy[r])
            else_in = snum + L

            snum += 1
            sy[f'sentence{snum}'] = ['j', ' ', ' ', f'sentence{else_in + 1+2}']
            snum += 1
            for r in real_z:
                if 'sentence' in r:
                    print(r, snum)
                    sy, snum, ja = copy_mid(sy, snum, r)

            if len(ja) != 0:
                for j in ja:
                    sy[f'sentence{j}'] = ['j', ' ', ' ', 'sentence_unknow']
                    jck.append(f'sentence{j}')
            else:
                sy[f'sentence{snum}'] = ['j', ' ', ' ', 'sentence_unknow']
                jck.append(f'sentence{snum}')
                snum += 1

            print('现在snum', snum)
            snum = else_in + 3
            print('else snum', snum)
            for r in real_j:
                if 'sentence' in r:
                    print(r, snum)
                    sy, snum, ja = copy_mid(sy, snum, r)

            if len(ja) != 0:
                for j in ja:
                    sy[f'sentence{j}'] = ['j', ' ', ' ', 'sentence_unknow']
                    jck.append(f'sentence{j}')
            else:
                sy[f'sentence{snum}'] = ['j', ' ', ' ', 'sentence_unknow']
                jck.append(f'sentence{snum}')
                snum += 1

        sy[f'sentence{snum}'] = get_allsy(sy, first, snum)

        for c in jck:
            sy[c].pop()
            sy[c].append(f'sentence{snum}')
        snum += 1
        return num, snum, sy, ck

    def cal(right, num, snum, sy, ck):
        if len(right) <= 1:
            return num, snum, sy, ck
        level = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2, ')': 3, '(': 0, '<': 0.5, '>': 0.5, '<=': 0.5, '>=': 0.5,
                 '==': 0.5, '!=': 0.5}

        cal_op = []
        num_op = []
        for r in right:
            if r.isalpha() or r.isdigit():
                num_op.append(r)
            else:
                if r == ')':
                    while True:
                        top = cal_op.pop()
                        if top == '(':
                            break
                        b = num_op.pop()
                        a = num_op.pop()
                        sy[f'sentence{snum}'] = [top, a, b, f't{num}']
                        num_op.append(f't{num}')
                        snum += 1
                        num += 1

                elif r == '(':
                    cal_op.append(r)
                elif len(cal_op) == 0 or level[r] >= level[cal_op[-1]]:
                    cal_op.append(r)

                elif level[r] < level[cal_op[-1]]:

                    top = cal_op.pop()
                    b = num_op.pop()
                    a = num_op.pop()
                    sy[f'sentence{snum}'] = [top, a, b, f't{num}']
                    num_op.append(f't{num}')
                    snum += 1
                    num += 1
                    cal_op.append(r)

        while len(cal_op) != 0:
            top = cal_op.pop()
            b = num_op.pop()
            a = num_op.pop()
            sy[f'sentence{snum}'] = [top, a, b, f't{num}']
            num_op.append(f't{num}')
            num += 1
            snum += 1
        return num, snum, sy, ck

    def deal_expression(code, num, snum, sy, ck):
        '''
        算术表达式应该是没有假出口的
        '''
        first = snum
        level = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2, ')': 3, '(': 0, '<': 0.5, '>': 0.5, '<=': 0.5, '>=': 0.5,
                 '==': 0.5, '!=': 0.5}

        if '=' in code:

            ind = code.index('=')
            name = code[ind]
            right = code[ind + 1:]
            left = code[:ind]

            if len(right) == 1:

                sy[f'sentence{snum}'] = ['=', right[0], ' ', left[0]]
                snum += 1

            else:
                num, snum, sy, ck = cal(right, num, snum, sy, ck)
                sy[f'sentence{snum}'] = ['=', f't{num - 1}', ' ', left[0]]
                num += 1
                snum += 1
        else:
            sy = []

        sy[f'sentence{snum}'] = get_allsy(sy, first, snum)
        snum += 1

        return num, snum, sy, ck

    def deal_com(expr, sy, num, snum, ck):
        level = ['<', '>', '<=', '>=', '==', '!=']
        comp_ind = 0
        for c, d in enumerate(expr):
            print(c, d)
            if d in level:
                comp_ind = c
                break

        left = expr[:comp_ind]
        right = expr[comp_ind + 1:]

        num2, snum, sy, ck = cal(left, num, snum, sy, ck)
        print(num2, snum)
        if num2 != num:
            left = sy[snum - 1][-1]
            num = num2
        else:
            left = left[0]

        num2, snum, sy, ck = cal(right, num, snum, sy, ck)
        print(num2, snum, sy)
        if num2 != num:
            right = sy[f'sentence{snum - 1}'][-1]
            num = num2
        else:
            right = right[0]
        return left, expr[comp_ind], right, sy, num, snum, ck

    def deal_iteration(code, num, snum, sy, ck):
        ja = []
        first = snum
        khl = code.index('(')
        khr = code.index(')')
        expression = code[khl + 1:khr]
        expr = []
        temp = []
        fi_r = khr
        while code[fi_r] != '}':
            fi_r += 1

        real_z = code[khr + 2:fi_r]

        if 'for' in code:
            expression.insert(1, ';')
            print('expression', expression)
            for e in expression:
                if e != ';':
                    temp.append(e)

                else:
                    expr.append(temp)
                    temp = []
            expr.append(temp)
            for r in expr[0]:
                if 'sentence' in r:
                    sy, snum, ja = copy_mid(sy, snum, r)

            pa = f'sentence{snum}'
            left, comp, right, sy, num, snum, ck = deal_com(expr[1], sy, num, snum, ck)
            print('left right', left, right)
            sy[f'sentence{snum}'] = [f'j{comp}', left, right, f'sentence_daiding']
            expc = f'sentence{snum}'

            snum += 1
            sy[f'sentence{snum}'] = ['j', ' ', ' ', 'sentence_unknow']
            jck = [f'sentence{snum}']
            snum += 1

            #     这里要接上expr2
            pa2 = f'sentence{snum}'
            for r in expr[2]:
                if 'sentence' in r:
                    print(r, snum)
                    sy, snum, ja = copy_mid(sy, snum, r)

            sy[f'sentence{snum}'] = ['j', ' ', ' ', pa]
            snum += 1

            sy[expc][-1] = f'sentence{snum}'
            for r in real_z:
                if 'sentence' in r:
                    sy, snum, ja = copy_mid(sy, snum, r)

            if len(ja) != 0:
                for j in ja:
                    sy[f'sentence{j}'] = ['j', ' ', ' ', pa2]
            else:
                sy[f'sentence{snum}'] = ['j', ' ', ' ', pa2]
                snum += 1

            sy[f'sentence{snum}'] = get_allsy(sy, first, snum)
        elif 'while' in code:
            pa = f'sentence{snum}'
            left, comp, right, sy, num, snum, ck = deal_com(expression, sy, num, snum, ck)
            sy[f'sentence{snum}'] = [f'j{comp}', left, right, f'sentence_daiding']
            expc = f'sentence{snum}'
            snum += 1
            sy[f'sentence{snum}'] = ['j', ' ', ' ', 'sentence_unknow']
            jck = [f'sentence{snum}']
            snum += 1
            sy[expc][-1] = f'sentence{snum}'
            for r in real_z:
                if 'sentence' in r:
                    sy, snum, ja = copy_mid(sy, snum, r)
            if len(ja) != 0:
                for j in ja:
                    sy[f'sentence{j}'] = ['j', ' ', ' ', pa]
            else:
                sy[f'sentence{snum}'] = ['j', ' ', ' ', pa]
                snum += 1

            sy[f'sentence{snum}'] = get_allsy(sy, first, snum)

        for c in jck:
            sy[c].pop()
            sy[c].append(f'sentence{snum}')
        snum += 1
        return num, snum, sy, ck

    def mid_code(d, start, fz, num, snum, sy, ck):
        value = []
        name = start.split(' ')[0]
        key = list(dict(d[start]).keys())
        if len(key) == 0:
            value.append(name)
            return value, num, snum, sy, ck
        else:
            for k in key:
                if k[0] != '$':
                    va, num, snum, sy, ck = mid_code(d, k, fz, num, snum, sy, ck)
                    value.extend(va)

        if name in ['expression', 'isnull_expr3']:
            print('遇到', name, value)
            if '=' in value:
                num, snum, sy, ck = deal_expression(value, num, snum, sy, ck)
                value = [f'sentence{snum - 1}']
                print('中间代码如下', sy[value[0]])

        elif name == 'isnull_expr1':
            print('遇到', name, value)
            if '=' in value:
                if value[0] in ['int', 'char']:
                    num, snum, sy, ck = deal_expression(value[1:-1], num, snum, sy, ck)
                    value = [f'sentence{snum - 1}']
                    print('中间代码如下', sy[value[0]])
                else:
                    num, snum, sy, ck = deal_expression(value[:-1], num, snum, sy, ck)
                    value = [f'sentence{snum - 1}']
                    print('中间代码如下', sy[value[0]])

        elif name == 'define_stmt':
            print('遇到', name, value)
            ind = value.index(';')
            if '+' in value or '*' in value or '-' in value or '/' in value:
                num, snum, sy, ck = deal_expression(value[1:ind], num, snum, sy, ck)
                if 'define' not in sy:
                    sy['define'] = value
                else:
                    sy['define'].extend(value)

                value = [f'sentence{snum - 1}']


        elif name == 'branch_stmt':
            print('遇到', name, value)
            num, snum, sy, ck = deal_bool_expression(value, num, snum, sy, ck)
            value = [f'sentence{snum - 1}']
            print('中间代码如下', sy[value[0]])

        elif name == 'iteration_stmt':
            print('遇到', name, value)
            num, snum, sy, ck = deal_iteration(value, num, snum, sy, ck)
            value = [f'sentence{snum - 1}']
            print('中间代码如下', f'sentence{snum - 1}', '->', sy[value[0]])

        return value, num, snum, sy, ck

    f = mid_code(d, 'Start 0', fz, 0, 0, {}, {})

    midcode = []
    define_code = []
    fin=''
    for c in f[0]:
        if 'sentence' in c:
            midcode.extend(f[-2][c])
            fin=c
        else:
            define_code.append(c)

    mid = []

    final_index = int(fin[8:])
    print('final', final_index)
    midcode.append(['sys', '', '', ''])

    for m in midcode:
        print(m[-1])
        if m[0] == 'sys':
            mid.append(m)
        elif m[0] == 'main':
            mid.append(m)
        elif 'sentence' in m[-1]:
            r = int(m[-1][8:])
            if r >= final_index:
                ind = midcode.index(['sys', '', '', ''])
                m[-1]=ind+2
                mid.append(m)

            else:
                ind = midcode.index(f[-2][m[-1]])
                m[-1] = ind+2
                mid.append(m)
        else:
            mid.append(m)
    mid.insert(0, ['main', '', '', ''])
    print('中间代码如下',mid)
    import re
    if 'define' in list(f[-2].keys()):
        define_code = ' '.join(define_code) + ' '.join(f[-2]['define'])
    else:
        define_code = ' '.join(define_code)
    define_code = re.split('(;|{|})', define_code)
    define_code = [d.strip() for d in define_code]

    def creat_tabel(define_code):
        type1 = ['int', 'char', 'double', 'float']
        table = []
        func_area = 0
        for d in define_code:
            d = d.split(' ')
            if d[0] == '{' or d[0] == '(':
                func_area = func_area + 1

            if d[0] in type1 and d[-1] == ')':
                if d[-2] == ')':
                    table.append(['无参数函数', d[0], d[1], 'null', func_area])
                else:
                    table.append(['无参数函数', d[0], d[1], 'null', func_area])
            elif d[0] in ['int', 'float', 'double']:
                if d[-1].isdigit():
                    table.append(['数值', d[0], d[1], d[-1], func_area])
                elif d[0] == 'int':
                    table.append(['数值', d[0], d[1], 0, func_area])
                elif d[0] == 'float':
                    table.append(['浮点数', d[0], d[1], 0.0, func_area])
                elif d[0] == 'double':
                    table.append(['双字节浮点数', d[0], d[1], 0.0, func_area])
            elif d[0] in ['char', 'string']:
                if d[-1].isalpha():
                    table.append(['字符', d[0], d[1], d[-1], func_area])
                elif d[0] == 'char':
                    table.append(['字符', d[0], d[1], '', func_area])
        return table

    table = creat_tabel(define_code)
    symbol = pd.DataFrame(table, columns=['类型', '类型token', '标识符', '值', '作用域'])
    symbol.to_csv('D:/代码/编译原理/语义分析与中间代码生成/static/语义分析符号的表.csv',encoding='gbk')
    sy=symbol.iloc[1:, :][['标识符', '值']].values.tolist()

    return mid,sy

def write_dot2(dot):
    with open('D:/代码/编译原理/语义分析与中间代码生成/static/source.dot', 'w', encoding='utf-8', ) as f:
        f.write(dot.source)


def Creat_SignTable(code):
    dot = get_tree(code, False)
    write_dot2(dot)
    d = read_dot('D:/代码/编译原理/语义分析与中间代码生成/static/source.dot')
    return  crea_mcode(code)

    # df = pd.DataFrame()


