import sys

sys.path.append('D:\\代码\\编译原理')
sys.path.append('D:\\代码')
import pandas as pd
from 语法分析 import LL1
from 语法分析.predict_analyse import get_tree
from 词法分析 import auto_analyse
import networkx as nx
from networkx.drawing.nx_pydot import read_dot
from 语法分析.LL1 import left_dg, get_first, get_follow, back_date
from graphviz import Digraph


def get_split(co):
    i = 0
    j = 0
    re = []
    while j <= len(co) - 1:
        if co[j] == ' ':
            if i == j:
                re.append(' ')
                i += 1
                j += 1
            else:
                re.append(co[i:j])
                re.append(' ')
                j += 1
                i = j
        else:
            j += 1
    re.append(co[i:])
    return re


def dic_type(wf, name):
    di = []
    for w in wf:
        w_ = w.split('->')[0]
        f = w.split('->')[1]
        f = get_split(f)
        if w_ == name:
            # f2是因为中间有空格
            if f[2] in fz and f[0] == '.' and f[2] != w_:
                di.append(w)
                di.extend(dic_type(wf, f[2]))
            elif f[0] == '.' and f[2] != w_:
                di.append(w)

    return di


def get_xm(wf1):
    wf = []
    for w in wf1:
        f = w.split('->')[0]
        r1 = w.split('->')[1]
        r = get_split(r1)
        r.append(' ')
        c = r.count(' ')
        index = 0

        while c != 0 or index <= len(r) - 1:
            if r[index] == ' ':
                te = r.copy()
                te[index] = '.'
                if index != len(r) - 1:
                    te.pop()
                te = [m for m in te if m != ' ']
                te = f + '->' + ' '.join(te)
                wf.append(te)
                c -= 1
            index += 1

    return wf


def get_Closure(edges, pa, now, list_zu, dot, has_nodes):
    if now[-1] == '.':
        if [now] not in list_zu:
            list_zu.append([now])

        if pa != ' ':
            X = now.split('->')[1].split(' ')
            ind = X.index('.')
            ll = X[ind - 1]
            dot.node(f'{now}', label='\n'.join([now]), shape='box')
            edges.append([pa.replace('\n', ' '), f'{now}', ll])
            dot.edge(pa, f'{now}', ll)
        print('从', now, '返回')
        return edges, list_zu, dot, has_nodes

    p = now.split('->')[1].split(' ')
    index = p.index('.')
    di = ''
    if p[index + 1] in fz:
        di = dic_type(xm, p[index + 1])

    cu = [now]
    cu.extend(di)

    if len(list_zu) != 0 and cu in list_zu:
        X = now.split('->')[1].split(' ')
        ind = X.index('.')
        ll = X[ind - 1]
        pa = pa.replace('\n', ' ')
        if pa == ' '.join(cu):
            edges.append([pa, pa, ll])
            dot.edge(pa, pa, ll)
            print('相同', now, '返回')
            return edges, list_zu, dot, has_nodes
    else:
        list_zu.append(cu)

    if pa != ' ':
        X = cu[0].split('->')[1].split(' ')
        ind = X.index('.')
        ll = X[ind - 1]
        edges.append([pa.replace('\n', ' '), ' '.join(cu), ll])
        dot.node('\n'.join(cu), label='\n'.join(cu))
        dot.edge(pa, '\n'.join(cu), ll)

    for c in cu[::-1]:
        r = get_split(c.split('->')[1])
        # r = list(c.split('->')[1])
        index = r.index('.')
        r[index], r[index + 2] = r[index + 2], r[index]
        r = c.split('->')[0] + '->' + ''.join(r)
        if r not in list(has_nodes.keys()):
            has_nodes[r] = []
            print('进入', r)
            edges, list_zu, dot, has_nodes = get_Closure(edges, '\n'.join(cu), r, list_zu, dot, has_nodes)
        else:
            for n in has_nodes[r]:
                X = cu[0].split('->')[1].split(' ')
                ind = X.index('.')
                ll = X[ind - 1]
                edges.append([pa.replace('\n', ' '), ' '.join(cu), ll])
                dot.node('\n'.join(cu), label='\n'.join(cu))
                dot.edge(pa, '\n'.join(cu), ll)

    return edges, list_zu, dot, has_nodes


def prepare_analyse(wf1):
    # 默认LL1文法
    # with open('D:/代码/编译原理/语法分析/static/C 文法3.txt') as f:
    #     wf_source = f.read()
    # wf1 = wf_source.split('\n')
    # wf1 = ['S_-> S', 'S-> ( L )', 'L-> i']

    # wf1 = ['S-> a A','S-> b B','A-> c d','A-> e','B-> f g','B-> h',]

    global fz
    wf1.insert(0, 'S_-> S')
    fz = [w.split('->')[0] for w in wf1]
    fz = list(set(fz))
    zj = []
    for w in wf1:
        w = w.split('->')[1]
        w = w.split(' ')
        for k in w:
            if k != ' ' and k != '' and k not in fz:
                zj.append(k)
    zj = list(set(zj))
    zj.insert(0, '#')
    global xm
    xm = get_xm(wf1)
    dot = Digraph()

    edges, z, dot, has_nodes = get_Closure([], ' ', 'S_->. S', [], dot, {})
    # dot.view()
    all_nodes = []
    z = [' '.join(m) for m in z]
    df = pd.DataFrame()
    fz.remove('S_')
    col = zj + fz
    df['name'] = z
    for c in col:
        df[c] = ['null'] * len(z)
    df.loc[df.name == 'S_->S .', '#'] = 'acc'
    label_dic = {}
    cn = 0
    for f in z:
        label_dic[f] = cn
        cn += 1

    for e in edges:
        df.loc[df.name == e[0], e[2]] = label_dic[e[1]]

    for l in z:
        if l[-1] == '.' and l != 'S_->S .':
            ori = l
            l = l[:-2]
            left = l.split('->')[0]
            right = l.split('->')[1]
            l = left + '-> ' + right
            id = wf1.index(l)
            df.loc[df.name == ori, zj] = f'r{id}'
    dot.view()
    df.to_csv('语法分析/static/lr0分析表')
    return df, wf1


def start_analyse(code, df, wf):
    # temp = auto_analyse.get_lex(code)
    # temp = list(temp)[0]
    # value_list = [t[0] for t in temp if len(t) > 0]
    # remain = [t[1] for t in temp if len(t) > 0]
    remain=code.split(' ')
    remain.append('#')

    state = [0]
    symbol = ['#']
    i = 0
    L = len(remain) - 1
    gc = []
    action = []

    while True:
        sta = state[-1]
        temp = remain[0]
        ac = str(df.loc[sta, temp])

        if 'r' in ac:
            # 归约

            num = ac[1:]
            num = int(num)
            right = wf[num].split('->')[1]
            right = get_split(right)
            right = [r for r in right if r != ' ' and r != '']
            left = wf[num].split('->')[0]
            j = -1
            sym_copy = symbol.copy()
            L=len(symbol)-1
            while j >= -1 * len(right) and right[j] == sym_copy[j]:
                symbol.pop()
                j -= 1
                L-=1
            symbol.append(left)
            state.pop()
            pp=symbol[1:L+1]
            pp=' '.join(pp)
            sta=0
            for m,n in enumerate(df['name']):
                k=pp+left+'.'
                k=''.join(k.split(' '))
                h=n.split('->')[1]
                h = ''.join(h.split(' '))
                if h==k:
                    sta=m
                    break
            new_sta = sta
            state.append(new_sta)
            i += 1
            action.append('归约' + f'{wf[num]}')
        elif ac != 'null':
            # 移进
            if ac=='acc':
                print('匹配完成退出Lr0分析')
                return gc
            state.append(int(ac))
            symbol.append(temp)
            action.append('移进')
            remain.pop(0)
            i += 1
        else:
            if str(df.loc[sta, '$']) != 'null':
                ac = str(df.loc[sta, '$'])
                # 移进
                print('可替代为空')
                remain.insert(0, '$')
            else:
                print('报错，请更改', sta, temp)
                break;
        print(state.copy(), symbol.copy(), remain.copy(), sta, temp, action[-1])
        gc.append([state.copy(), symbol.copy(), remain.copy(), sta, temp, action[-1]])
        # if temp == '#':


def Lr0(wf,code):
    if len(wf)==0:
        wf = ['S-> a A','S-> b B','A-> c d','A-> e','B-> f g','B-> h',]
    df, wf1 = prepare_analyse(wf)
    print('lr表生成如下')
    print(df)
    gc=start_analyse(code, df, wf1)

    g = pd.DataFrame(gc, columns=['状态栈', '符号栈', '待输入符号', '当前状态', '当前字符', '执行'])
    g.to_csv('语法分析/static/lr分析过程.csv')
    return gc

