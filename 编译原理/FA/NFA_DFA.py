import sys

sys.path.append('D:\\代码\\编译原理')
sys.path.append('D:\\代码')
import networkx as nx
from networkx.drawing.nx_pydot import write_dot
from IPython.core.interactiveshell import InteractiveShell

InteractiveShell.ast_node_interactivity = "all"
from graphviz import Digraph
from networkx import DiGraph

import graphviz


def plot(dot, name):
    write_dot(dot, "D:\代码\编译原理\pic\grid.dot")
    with open("D:\代码\编译原理\pic\grid.dot") as f:
        dot_graph = f.read()
    dot_graph = dot_graph.replace('name', 'label')
    dot2 = graphviz.Source(dot_graph)
    dot2.render(f'D:\代码\编译原理\pic\pic//{name}.pdf', view=True)
    return dot2


class Subgraph():
    def __init__(self, dot):

        self.label = ''
        self.head = ''
        self.tail = ''
        self.index = 0
        self.nodes = []
        self.copy_num = 0

    def add_edge(self, a, b, label='xx'):
        if type(a) != str:
            a = a.tail
        if type(b) != str:
            b = b.head
        self.nodes.append([a, b, label])
        dot.add_edge(a, b, name=label)

    def add_node(self, name, shape='circle', color='black'):
        dot.add_node(name, shape=shape, color=color)


def subcopy(sg, dot, start):
    d_temp = Subgraph(dot)
    d_temp.head = f'{start}' + f'cop{sg.copy_num}' + sg.head
    for n in sg.nodes:
        d_temp.add_edge(f'{start}' + f'cop{sg.copy_num}' + n[0], f'{start}' + f'cop{sg.copy_num}' + n[1], n[2])
        start += 1
    d_temp.tail = f'{start - 1}' + f'cop{sg.copy_num}' + sg.tail
    sg.copy_num += 1

    d_temp.label = sg.label

    return d_temp, start


def deal_or(s, stack_sign, dot, start):
    if s == '|':
        a = stack_sign.pop(-1)
        b = stack_sign.pop(-1)
        d = Subgraph(dot)
        d.add_edge(str(start), str(start + 1), label='sgm')
        d.add_edge(str(start), str(start + 2), label='sgm')
        d.add_edge(str(start + 1), b, b.label)
        d.add_edge(str(start + 2), a, a.label)
        d.add_edge(b, str(start + 3), label='sgm')
        d.add_edge(a, str(start + 3), label='sgm')
        d.head = str(start)
        d.tail = str(start + 3)
        d.label = 'sgm'
        start += 4
        stack_sign.append(d)
        return stack_sign, start


def deal_attach(s, stack_sign, dot, start):
    if s == '·':
        d = Subgraph(dot)
        b = stack_sign.pop(-1)
        a = stack_sign.pop(-1)
        if a.label == 'start':
            d.add_edge(f'{start}', b, label=b.label)
            d.add_edge(a, f'{start}', label='sgm')
            d.head = str(a.head)
            d.tail = str(b.tail)
            d.label = a.label
            print('起始', start)
        else:

            d.add_edge(a, b, label=b.label)
            d.head = str(a.head)
            d.tail = str(b.tail)
            d.label = a.label

        start += 1
        stack_sign.append(d)
        return stack_sign, start


def deal_dian(s, stack_sign, dot, start):
    if s == '.':
        d = Subgraph(dot)
        a = stack_sign.pop(-1)
        d.add_edge(a, f'{start}', label='!=\  n')
        d.head = str(a.head)
        d.tail = f'{start}'
        d.label = a.label
        start += 1
        stack_sign.append(d)
        return stack_sign, start


def deal_bb(s, stack_sign, dot, start):
    if s == '*':
        d = Subgraph(dot)
        a = stack_sign.pop(-1)
        d.add_edge(str(start), a, label='sgm')
        d.add_edge(a, a, label=a.label)
        d.add_edge(a, str(start + 1), label='sgm')
        d.add_edge(str(start), str(start + 1), label='sgm')
        d.head = str(start)
        d.tail = str(start + 1)
        d.label = 'sgm'
        start += 2
        stack_sign.append(d)
    return stack_sign, start


def deal_zbb(s, stack_sign, dot, start):
    if s == '+':
        d = Subgraph(dot)
        a = stack_sign.pop(-1)
        d.add_edge(str(start), a, label=a.label)
        d.add_edge(a, a, label=a.label)
        d.add_edge(a, str(start + 1), label='sgm')
        d.head = str(start)
        d.tail = str(start + 1)
        d.label = 'sgm'
        start += 2
        stack_sign.append(d)
    return stack_sign, start


# 花括号
def deal_hkh(s, stack_sign, dot, start):
    if s == '}':
        d = Subgraph(dot)
        c = stack_sign.pop(-1)
        dot.remove_node(c.head)
        m = int(c.label) - 1
        a = stack_sign.pop(-1)

        cop = ''
        last = a
        for i in range(m):
            cop, start = subcopy(a, dot, start)
            d.add_edge(last, cop, label=cop.label)
            last = cop
        d.head = a.head
        d.tail = last.tail
        d.label = a.label
        stack_sign.append(d)
        return stack_sign, start


# 方括号
def deal_fkh(st):
    Li = 0
    remain = []
    for c in range(0, len(st)):
        p = st[c]
        if c == 0:
            if st[c + 1] != '-':
                remain.append(st[c])
                continue
        if c == len(st) - 1:
            if st[c - 1] != '-':
                remain.append(st[c])
                continue
        if st[c - 1] != '-' and st[c + 1] != '-' and st[c] != '-':
            remain.append(st[c])
    result = ''
    while True:
        try:
            i = st.index('-', Li)
        except:
            break
        if st[i - 1].isalpha() and st[i + 1].isalpha():
            chars = []
            L1 = ord(st[i - 1])
            L2 = ord(st[i + 1])
            if L1 > L2:
                L1, L2 = L2, L1
            for k in range(L1, L2 + 1):
                chars.append(str(chr(k)))
            if len(result) > 1:
                result += '|'
            result += '|'.join(chars)

        if st[i - 1].isdigit() and st[i + 1].isdigit():
            ints = []
            L1 = int(st[i - 1])
            L2 = int(st[i + 1])
            if L1 > L2:
                L1, L2 = L2, L1
            for k in range(L1, L2 + 1):
                ints.append(str(k))
            if len(result) > 1:
                result += '|'
            result += '|'.join(ints)

        Li = i + 1
    if len(result) > 1:
        result += '|'
        result += '|'.join(remain)

    return '(' + result + ')'


def deal(s, stack_sign, dot, start):
    #  ^ .还没有写
    if s == '·':
        return deal_attach(s, stack_sign, dot, start)
    elif s == '}':
        return deal_hkh(s, stack_sign, dot, start)
    elif s == '|':
        return deal_or(s, stack_sign, dot, start)
    elif s == '+':
        return deal_zbb(s, stack_sign, dot, start)
    elif s == '*':
        return deal_bb(s, stack_sign, dot, start)
    elif s == '.':
        return deal_dian(s, stack_sign, dot, start)


def get_st(zz, index, stack_cal):
    if index + 1 < len(zz) and zz[index + 1].isalpha():
        stack_cal.append('·')
    elif index + 1 < len(zz) and zz[index + 1] == '(':
        stack_cal.append('·')
    return stack_cal


def start_NFA(zz):
    # '·'表示连接运算符
    level = {

        '+': 3, '\\': 5, '|': 1, '*': 4, '.': 2, '?': 3, '{': 3, '}': 3.5, '(': 4, ')': 4.5, '[': 4, ']': 4.5, '^': 2,
        '$': 2,
        '·': 2,
    }

    # 实例化一个Digraph对象(有向图)，name:生成的图片的图片名，format:生成的图片格式
    global dot
    dot = nx.DiGraph(splines=True)
    index = 0
    cnt = 1
    d = Subgraph(dot=dot)
    d.add_node(name=str(0) + 'start', color='red')
    d.head = str(0) + 'start'
    d.tail = str(0) + 'start'
    d.label = 'start'

    # 存储运算符
    stack_cal = ['#', '·']
    # 存储非运算符 sgm表示空字符
    stack_sign = [d]

    zm = []
    while True:
        s = zz[index]

        print('当前stack_cal', stack_cal, s)
        print('剩余', len(stack_sign))
        print('当前尾节点', stack_sign[-1].tail, '当前头节点', stack_sign[-1].head, '当前节点label', stack_sign[-1].label)

        if s in ['+', '\\', '|', '*', '.', '?', '{', '}', '(', ')', '[', ']']:
            if level[stack_cal[-1]] < level[s]:
                if s == '}':
                    stack_sign, cnt = deal(s, stack_sign, dot, cnt)
                    while stack_cal[-1] != '{':
                        stack_sign, cnt = deal_hkh(s, stack_sign, dot, cnt)

                elif s == ')':
                    stack_sign, cnt = deal(stack_cal.pop(), stack_sign, dot, cnt)
                    while stack_cal[-1] != '(':
                        stack_sign, cnt = deal(stack_cal.pop(), stack_sign, dot, cnt)
                    stack_cal.pop()

                elif s == ']':
                    st = ''
                    while stack_cal[-1] != '[':
                        st += stack_sign.pop(-1).label
                        stack_cal.pop(-1)
                    st = deal_fkh(st)
                    if st[-2] == '|':
                        st = st[:-2] + ')'

                    for m in st:
                        if m not in level.keys():
                            d = Subgraph(dot)
                            d.add_node(name=f'{cnt}' + f' {m}')
                            d.head = str(cnt) + f' {m}'
                            d.tail = str(cnt) + f' {m}'
                            d.label = m
                            stack_sign.append(d)
                            cnt += 1
                        elif m != ')':
                            stack_cal.append(m)

                        elif m == ')':
                            stack_sign, cnt = deal(stack_cal.pop(), stack_sign, dot, cnt)
                            while stack_cal[-1] != '(':
                                stack_sign, cnt = deal(stack_cal.pop(), stack_sign, dot, cnt)
                            stack_cal.pop()

                    stack_cal.pop()


                elif s in ['(', '[', '{']:
                    stack_cal.append(s)

                else:
                    stack_cal.append(s)
                    stack_sign, cnt = deal(stack_cal.pop(), stack_sign, dot, cnt)

            elif level[stack_cal[-1]] == level[s]:
                if stack_cal[-1] == s and s == '(':
                    stack_cal.append(s)
                elif stack_cal[-1] != s:
                    stack_cal.append(s)
                    stack_sign, cnt = deal(stack_cal.pop(), stack_sign, dot, cnt)

                else:
                    stack_cal.pop()
            else:
                stack_cal.append(s)
            #             右符号的连接
            if s in [')', ']', '}', '*', '+', '.']:
                stack_cal = get_st(zz, index, stack_cal)

        else:
            stack_cal = get_st(zz, index, stack_cal)
            zm.append(s)
            d = Subgraph(dot)
            d.add_node(name=f'{cnt}')
            d.head = str(cnt)
            d.tail = str(cnt)
            d.label = s
            stack_sign.append(d)
            cnt += 1

        index += 1
        if index >= len(zz):
            break

    while len(stack_cal) != 1:
        stack_sign, cnt = deal(stack_cal[-1], stack_sign, dot, cnt)
        stack_cal.pop()

    z_node = []
    for n in dot.nodes:
        if dot.out_degree(n) == 0 and n != '0start':
            z_node.append(n)
            continue
    zt_n = z_node[0]

    d.add_node(name='end', shape='doublecircle')
    dot.add_edge(z_node[0], 'end', name='sgm')

    plot(dot, 'NFA')
    dot.remove_node('end')
    import gc
    gc.collect()

    # 第二步 NFA->DFA

    def get_closure(nn, la, res, dot, gy):
        f = False
        r = dict(dot[nn].items())
        for m, n in zip(r.keys(), r.values()):
            if n['name'] == la and m != nn and m not in gy:
                f = True
                if m not in gy:
                    gy.append(m)
                res = get_closure(nn=m, la=la, res=res, dot=dot, gy=gy)

        res.append(nn)
        return res

    def get_I(nn, la, res, dot):
        f = False
        r = dict(dot[nn].items())
        for m, n in zip(r.keys(), r.values()):
            if n['name'] == la:
                f = True
                res.append(m)
        return res

    dr = {}
    for n in dot.nodes:
        k = get_closure(n, res=[], la='sgm', dot=dot, gy=[])
        dr[n] = list(set(k))
    start = list(dict(dot['0start'].items()).keys())[0]

    import pandas as pd
    import numpy as np

    zm = list(set(zm))
    df = pd.DataFrame()
    df = pd.DataFrame(np.zeros(len(zm) + 1))
    df = df.T
    df.columns = ['sgmlist'] + zm
    df.iloc[0, 0] = '[' + ','.join(dr[start]) + ']'

    n_index = 0
    new_ = 1
    while True:
        change = False
        for z in zm:
            move = []
            for m in eval(df.iloc[n_index, 0]):
                t = list(set(get_I(str(m), res=[], la=z, dot=dot)))
                move += t
            move = list(set(move))

            res = []
            for m in move:
                res += dr[m]
            df.loc[n_index, z] = '[' + ','.join(res) + ']'

            if df.loc[n_index, z] not in df.iloc[:, 0].unique():
                change = True
                df.loc[new_, 'sgmlist'] = '[' + ','.join(res) + ']'
                new_ += 1
        if not change and len(df[df[zm[0]].isna()]) == 0:
            break
        n_index += 1

    zt_p = df.loc[:, 'sgmlist'].apply(lambda x: zt_n in x)
    ct_p = df.loc[:, 'sgmlist'].apply(lambda x: start in x)

    pre_sgm = df['sgmlist']

    from sklearn.preprocessing import LabelEncoder

    La = LabelEncoder()

    for i in range(len(df.columns)):
        df.iloc[:, i] = df.iloc[:, i].astype(str)
        if i == 0:
            df.iloc[:, i] = La.fit_transform(df.iloc[:, i])
        else:
            df.iloc[:, i] = La.transform(df.iloc[:, i])

    if '[]' in list(pre_sgm):
        kong = La.transform(['[]'])[0]
    else:
        kong = ''

    # 连接点是否不全为空点
    def add(i, kong):
        for j in range(1, len(i)):
            if j != kong:
                return True
        return False

    def hasIntersection(a, b):
        return not set(a).isdisjoint(b)

    dot2 = nx.DiGraph(splines=True)
    cnt = 0
    # 确定终态和初态
    zt_nodes = []
    ct_nodes = []
    zm_new = []
    for i in df.values:
        if i[0] != kong:
            if zt_p[cnt]:
                if add(i, kong):
                    dot2.add_node(str(i[0]), shape='doublecircle')
                    zt_nodes.append(str(i[0]))
            #         elif ct_p[cnt]:
            #             if add(i,kong):
            #                 dot2.add_node(str(i[0]),color='red')
            #                 ct_nodes.append(str(i[0]))

            cnt += 1
            for j in range(1, len(i)):
                if i[j] != kong and i[0] != kong:
                    if dot2.has_edge(str(i[0]), str(i[j])) and not hasIntersection(zm[j - 1],
                                                                                   dot2[str(i[0])][str(i[j])]['name']):
                        zm[j - 1] += ' or ' + dot2[str(i[0])][str(i[j])]['name']
                    if zm[j - 1] not in zm_new:
                        zm_new.append(zm[j - 1])
                    dot2.add_edge(str(i[0]), str(i[j]), name=zm[j - 1])

    plot(dot2, 'DFA')

    # DFA的最小化
    def reverse_dict(dic):
        v = dic.values()
        nd = {}
        for (a, s) in dic.items():
            if s in nd.keys():
                nd[s].append(a)
            else:
                nd[s] = [a]
        return nd

    fzt_node = []
    zm = zm_new
    for n in dot2.nodes:
        if n not in zt_nodes:
            fzt_node.append(n)

    if len(fzt_node) >= 1:
        zj = [fzt_node, zt_nodes]
    else:
        zj = [zt_nodes]
    print(zj)

    import statistics as stats

    def get_fizj(zj, dot2):
        while True:
            change_cnt = len(zj)
            for z in zm:
                zj2 = zj.copy()
                for m in zj.copy():
                    print('当前子集', m)
                    dt = {}
                    rea_change = []
                    for k in m:
                        e = get_I(str(k), la=z, res=[], dot=dot2)
                        if len(e) == 0:
                            dt[f'{k}'] = 'kong'
                        else:
                            dt[f'{k}'] = f'{e[0]}'
                            rea_change.append(f'{e[0]}')
                    #         如果存在其后接子集与另一个子集的差集等于该后接子集，则该子集无法区分

                    print('后接子集', rea_change, '字母', z)
                    change = True
                    cc = []
                    res = []
                    for r in zj.copy():
                        r = set(r)
                        if list(set(rea_change) & r) == list(set(rea_change)):
                            print('存在完全相等集合', r, rea_change, '集合不可区分')
                            change = False
                            break
                        else:
                            temp2 = set(rea_change) & r
                            if len(temp2) != 0:
                                res.append(list(temp2))

                    dt_verse = reverse_dict(dt)

                    if change:
                        print('改变了', '映射是', dt)
                        zj2.remove(m)

                        for f in res:
                            ttt = []
                            for q in f:
                                ttt.extend(dt_verse[q])
                            zj2.append(ttt)
                        print('翻转映射', dt_verse, '新子集：', zj2)
                    else:
                        print('\n\n')
                        continue
                    print('\n\n')
            zj = zj2
            print('子集变成了', zj)
            if change_cnt == len(zj):
                return zj2

            # 最终子集

    zj_final = get_fizj(zj, dot2)
    zj_final

    t_dic = {}
    for j in zj_final:
        if len(j) > 1:
            for l in j:
                t_dic[l] = j[0]
        elif len(j) == 1:
            t_dic[j[0]] = j[0]

    dot_f = nx.DiGraph()

    kk = []

    dr = {}
    dy = {}
    for z in zm:
        for n in dot2.nodes:
            k = get_I(n, res=[], la=z, dot=dot2)
            if len(k) > 0:
                #             if n in t_dic.keys():
                k = list(set(k))[0]
                kk.append(f'{t_dic[n]}_{t_dic[k]}_{z}')

    kk = list(set(kk))

    for n in ct_nodes:
        if n in list(t_dic.values()):
            dot_f.add_node(n, color='red')
    for n in zt_nodes:
        if n in list(t_dic.values()):
            dot_f.add_node(n, shape='doublecircle')

    for k in kk:
        k = k.split('_')
        if k[0] == k[1]:
            if dot_f.has_edge(k[0], k[1]):
                k[2] += ' or ' + dot_f[k[0]][k[1]]['name']
        dot_f.add_edge(k[0], k[1], name=k[2])

    # z_node=[]
    # for n in dot_f.nodes:
    #     if dot.in_degree(n)==0 :
    #         dot_f.add_edge('start',n,)

    plot(dot_f, 'min_dfa')
