import pandas as pd
import sys
sys.path.append('D:\\代码\\编译原理')
sys.path.append('D:\\代码')
df=pd.read_csv('词法分析/type_code.csv')
keyword_sign =df[df['类型']=='关键词'][['字符','种别码']].set_index('字符').to_dict()['种别码']
word_sign=df[df['类型']=='特殊符'][['字符','种别码']].set_index('字符').to_dict()['种别码']
cal_sign = df[df['类型']=='运算与逻辑符'][['字符','种别码']].set_index('字符').to_dict()['种别码']
jie_sign =df[df['类型']=='界符'][['字符','种别码']].set_index('字符').to_dict()['种别码']
num_sign= df[df['类型']=='数值符号'][['字符','种别码']].set_index('字符').to_dict()['种别码']


# 错误 state=66
# 分辨标识符

def distinguish_symbol(str_code, index_start, state):
    start = index_start

    while True:

        index_start += 1
        s = str_code[index_start]

        if state == 3:
            if s.isalpha() or s == '_' or s.isdigit():
                state = 3
            else:
                state = 9
        if state == 9:

            if str_code[start:index_start] in keyword_sign.keys():
                state = 11
                type_code = keyword_sign[str_code[start:index_start]]
                return index_start - 1, [str_code[start:index_start], type_code]
            elif s == ' ' or s == '=' or s in cal_sign.keys() or s in jie_sign.keys() or s == '\n':
                state = 10
                type_code = word_sign['identifier']
                return index_start - 1, [str_code[start:index_start], type_code]
            else:
                state = 66
                type_code = word_sign['error']
                bc = ' 出现未知标识符'
                return index_start, [str_code[start:index_start + 1]  ,bc, type_code]


# 分辨数值
def distinguish_number(str_code, index_start, state):
    start = index_start
    while True:

        s = str_code[index_start]

        if state == 4:
            if s == '0':
                state = 37
            else:
                state = 29
        elif state == 29:
            if s.isdigit():
                state = 29
            elif s == '.':
                state = 30
            elif s == 'E' or s == 'e':
                state = 32
            elif s in cal_sign.keys() or s in jie_sign.keys() or s == ' ' or s == '\n':
                state = 41
                type_code = num_sign['整数']
                return index_start - 1, [str_code[start:index_start], type_code]
            else:
                state = 66
                type_code = word_sign['error']
                bc = ' 数字识别错误'
                return index_start, [str_code[start:index_start + 1] ,bc, type_code]
        elif state == 30:
            if s.isdigit():
                state = 31
            else:
                state = 66
                bc = ' 数字识别错误'
                type_code = word_sign['error']
                return index_start, [str_code[start:index_start + 1],bc, type_code]
        elif state == 31:
            if s.isdigit():
                state = 31
            elif s == 'E' or s == 'e':
                state = 32
            elif s == '\n' or s in cal_sign.keys() or s in jie_sign.keys() or s == ' ':
                state = 36
                type_code = num_sign['小数']
                return index_start, [str_code[start:index_start], type_code]
            else:
                state = 66
                bc = ' 数字识别错误'
                type_code = word_sign['error']
                return index_start, [str_code[start:index_start + 1] , bc, type_code]
        elif state == 32:
            if s.isdigit():
                state = 34
            elif s == '+' or s == '-':
                state = 33
            else:
                state = 66
                bc = ' 数字识别错误'
                type_code = word_sign['error']
                return index_start, [str_code[start:index_start + 1] , bc, type_code]
        elif state == 33:
            if s.isdigit():
                state = 34
            else:
                bc = ' 数字识别错误'
                state = 66
                type_code = word_sign['error']
                return index_start, [str_code[start:index_start + 1] , bc, type_code]
        elif state == 34:
            if s.isdigit():
                state = 34
            elif s == '+' or s == '-':
                state = 34
            elif s in cal_sign.keys() or s in jie_sign.keys() or s == ' ' or s == '\n':

                type_code = num_sign['指数']
                return index_start, [str_code[start:index_start], type_code]
            else:
                state = 66
                bc = ' 数字指数识别错误'
                type_code = word_sign['error']
                return index_start, [str_code[start:index_start + 1] , bc, type_code]
        elif state == 37:
            if s.isdigit():
                if int(s) < 2:
                    state = 37
                else:
                    state = 66
                    bc = ' 数字进制识别错误'
                    type_code = word_sign['error']
                    return index_start, [str_code[start:index_start + 1] ,bc, type_code]

            elif s in jie_sign.keys() or s == ' ':

                state = 41
                type_code = num_sign['整数']
                return index_start - 1, [str_code[start:index_start], type_code]

            elif s == 'x' or s == 'X':
                state = 38
            else:
                state = 66
                bc = ' 数字进制识别错误'
                type_code = word_sign['error']
                return index_start, [str_code[start:index_start + 1] , bc, type_code]
        elif state == 38:
            kk = 0
            if s.isdigit() or s.isalpha():
                if s.isalpha():
                    s = s.lower()
                    if 102 >= ord(s) >= 97:
                        state = 39
                    else:
                        state = 66
                        bc='进制数字识别出错'
                        type_code = word_sign['error']
                        return index_start, [str_code[start:index_start + 1],bc, type_code]
                else:
                    state = 39
            else:
                state = 66
                bc = ' 数字进制超出错误'
                type_code = word_sign['error']
                return index_start, [str_code[start:index_start + 1],bc, type_code]
        elif state == 39:
            if s.isdigit() or s.isalpha():
                if s.isalpha():
                    s = s.lower()
                    if 102 >= ord(s) >= 97:
                        state = 39
                    else:
                        state = 66
                        bc = ' 数字识别错误'
                        type_code = word_sign['error']
                        return index_start, [str_code[start:index_start + 1],bc, type_code]
                else:
                    state = 39
            else:
                state = 40
                type_code = num_sign['进制数']
                return index_start, [str_code[start:index_start], type_code]
        else:
            state = 66
            bc='二进制数字错误'
            type_code = word_sign['error']
            return index_start, [str_code[start:index_start + 1],bc, type_code]
        index_start += 1


# 分辨字符常数
def distinguish_char(str_code, index_start, state):
    start = index_start

    while True:
        index_start += 1
        s = str_code[index_start]
        if state == 6:
            if s != '\'':
                state = 12
            elif s == "'":
                state = 66
                bc='空字符常数'
                type_code = word_sign['error']
                return index_start, [str_code[start:index_start + 1], bc,type_code]
        else:
            if s == '\'':
                state = 13
                type_code = word_sign['char']
                return index_start, [str_code[start:index_start + 1], type_code]
            elif s == '\n':
                state = 66
                bc = ' 两边引号不全！'
                type_code = word_sign['error']
                return index_start, [str_code[start:index_start + 1],bc, type_code]
            else:
                state = 12


# 分辨字符串常数
def distinguish_string(str_code, index_start, state):
    start = index_start

    while True:
        index_start += 1
        s = str_code[index_start]
        if state == 7:
            if s != '\"':
                state = 14
            if s == '\"':
                state = 66
                bc = ' 出现空字符串'
                type_code = word_sign['error']
                return index_start, [str_code[start:index_start + 1],bc, type_code]



        else:
            if s == '\"':
                state = 15
                type_code = word_sign['string']
                return index_start, [str_code[start:index_start + 1], type_code]
            elif s=='\n':
                state = 66
                bc = ' 两边引号不全！'
                type_code = word_sign['error']
                return index_start, [str_code[start:index_start + 1] ,  bc, type_code]
            else:
                state = 14


# 分辨注释和除法
def distinguis_zhushi(str_code, index_start, state):
    start = index_start
    while True:
        index_start += 1
        s = str_code[index_start]
        if state == 5:
            if s == '*':
                state = 16
            elif s == '/':
                state = 17
            elif s == ' ' or str_code[index_start + 1].isdigit():
                type_code = cal_sign['/']
                return index_start, [str_code[start:index_start], type_code]
            else:
                return index_start, [str_code[start:index_start], 660]
        elif state == 16:
            if s != '*':
                state = 16
            else:
                state = 18

        elif state == 17:
            while True:
                index_start += 1
                if str_code[index_start] == '\n':
                    type_code = word_sign['single_zhushi']
                    return index_start, [str_code[start:index_start], type_code]

        elif state == 18:
            if s == '/':
                state = 19
                type_code = word_sign['double_zhushi']
                return index_start, [str_code[start:index_start + 1], type_code]
            else:
                state = 16
        else:
            pass


# 分辨其他、操作符、界符
def distinguis_other(str_code, index_start, state):
    start = index_start
    while True:

        s = str_code[index_start]

        if state == 8:
            if s in jie_sign.keys():
                state = 20
            elif s in cal_sign.keys():
                state = 21
            else:
                bc = '出现未知符号'
                state = 66
                type_code = word_sign['error']
                return index_start, [str_code[start:index_start + 1],bc, type_code]
        if state == 21:
            k = 0
            m = str_code[index_start + 1]
            if s == '+' and str_code[index_start + 1] != '=' and str_code[index_start + 1] != '+':
                type_code = cal_sign['+']
                return index_start, [str_code[start:index_start + 1], type_code]
            elif s == '+' and str_code[index_start + 1] == '='  and str_code[index_start + 2] not in cal_sign.keys() :
                type_code = cal_sign['+=']
                return index_start + 1, [str_code[start:index_start + 2], type_code]
            elif s == '+' and str_code[index_start + 1] == '+'  and str_code[index_start + 2] not in cal_sign.keys():
                type_code = cal_sign['++']
                return index_start + 1, [str_code[start:index_start + 2], type_code]
            elif s == '-' and str_code[index_start + 1] != '=' and str_code[index_start + 1] != '-':
                type_code = cal_sign['-']
                return index_start, [str_code[start:index_start + 1], type_code]
            elif s == '-' and str_code[index_start + 1] == '='  and str_code[index_start + 2] not in cal_sign.keys():
                type_code = cal_sign['-=']
                return index_start + 1, [str_code[start:index_start + 2], type_code]
            elif s == '-' and str_code[index_start + 1] == '-'  and str_code[index_start + 2] not in cal_sign.keys():
                type_code = cal_sign['--']
                return index_start + 1, [str_code[start:index_start + 2], type_code]
            elif s == '*':
                type_code = cal_sign['*']
                return index_start, [str_code[start:index_start + 1], type_code]
            elif s == '%':
                type_code = cal_sign['%']
                return index_start, [str_code[start:index_start + 1], type_code]
            elif s == '#':
                type_code = cal_sign['#']
                return index_start, [str_code[start:index_start + 1], type_code]
            elif s == '=' and str_code[index_start + 1] != '=':
                type_code = cal_sign['=']
                return index_start, [str_code[start:index_start + 1], type_code]
            #             判定
            elif s == '=' and str_code[index_start + 1] == '='  and str_code[index_start + 2] not in cal_sign.keys():
                type_code = cal_sign['==']
                return index_start + 1, [str_code[start:index_start + 2], type_code]
            elif s == '<' and str_code[index_start + 1] == '='  and str_code[index_start + 2] not in cal_sign.keys():
                type_code = cal_sign['<=']
                return index_start + 1, [str_code[start:index_start + 2], type_code]
            elif s == '<' and str_code[index_start + 1] != '=':
                type_code = cal_sign['<']
                return index_start, [str_code[start:index_start + 1], type_code]
            elif s == '>' and str_code[index_start + 1] == '='  and str_code[index_start + 2] not in cal_sign.keys():
                type_code = cal_sign['>=']
                return index_start + 1, [str_code[start:index_start + 2], type_code]
            elif s == '>' and str_code[index_start + 1] != '=':
                type_code = cal_sign['>']
                return index_start, [str_code[start:index_start + 1], type_code]
            elif s == '!' and str_code[index_start + 1] == '=' and str_code[index_start + 2] not in cal_sign.keys():
                type_code = cal_sign['!=']
                return index_start + 1, [str_code[start:index_start + 2], type_code]
            elif s == '!' and str_code[index_start + 1] != '=':
                type_code = cal_sign['!']
                return index_start, [str_code[start:index_start + 1], type_code]
            #             条件
            elif s == '&' and str_code[index_start + 1] == '&' and str_code[index_start + 2] not in cal_sign.keys():
                type_code = cal_sign['&&']
                return index_start + 1, [str_code[start:index_start + 2], type_code]
            elif s == '&' and str_code[index_start + 1] != '&':
                type_code = cal_sign['&']
                return index_start, [str_code[start:index_start + 1], type_code]
            elif s == '|' and str_code[index_start + 1] != '|':
                type_code = cal_sign['|']
                return index_start, [str_code[start:index_start + 1], type_code]
            elif s == '|' and str_code[index_start + 1] == '|' and str_code[index_start + 2] not in cal_sign.keys():
                type_code = cal_sign['||']

                return index_start + 1, [str_code[start:index_start + 2], type_code]
            elif s == '.' and not str_code[index_start - 1].isdigit():
                type_code = cal_sign['.']
                return index_start, [str_code[start:index_start + 1], type_code]

            else:
                state = 66
                bc='运算符错误'
                type_code = word_sign['error']
                return index_start, [str_code[start:index_start + 1],bc, type_code]
        elif state == 20:
            if s == '{':
                type_code = jie_sign['{']
                return index_start, [str_code[start:index_start + 1], type_code]
            elif s == '}':
                type_code = jie_sign['}']
                return index_start, [str_code[start:index_start + 1], type_code]
            elif s == '(':
                type_code = jie_sign['(']
                return index_start, [str_code[start:index_start + 1], type_code]
            elif s == ')':
                type_code = jie_sign[')']
                return index_start, [str_code[start:index_start + 1], type_code]
            elif s == ';':
                type_code = jie_sign[';']
                return index_start, [str_code[start:index_start + 1], type_code]
            elif s == '[':
                type_code = jie_sign['[']
                return index_start, [str_code[start:index_start + 1], type_code]
            elif s == ']':
                type_code = jie_sign[']']
                return index_start, [str_code[start:index_start + 1], type_code]
            elif s == ',':
                type_code = jie_sign[',']
                return index_start, [str_code[start:index_start + 1], type_code]
            else:
                state = 66
                bc = '界符错误'
                type_code = word_sign['error']
                return index_start, [str_code[start:index_start + 1],bc, type_code]

        index_start += 1



def distinguish(str_code):
    state = 0
    start_index = 0
    result = []
    error=[]

    while True:
        try:

            s = str_code[start_index]

            if s != ' ' and s != '\t':
                line = str_code[:start_index].count('\n') + 1
                if s == '\n':
                    r = [0, 0]
                elif s.isalpha():
                    state = 3
                    start_index, r = distinguish_symbol(str_code, start_index, state)
                    r.append(line)
                    result.append(r)
                elif s.isdigit():
                    state = 4
                    start_index, r = distinguish_number(str_code, start_index, state)
                    r.append(line)
                    result.append(r)
                elif s == '/':
                    state = 5
                    start_index, r = distinguis_zhushi(str_code, start_index, state)
                    r.append(line)
                    line += r[0].count('\n')
                    if r[1]==cal_sign['/']:
                        result.append(r)
                elif s == '\'':
                    state = 6
                    start_index, r = distinguish_char(str_code, start_index, state)
                    r.append(line)
                    result.append(r)
                elif s == '\"':
                    state = 7
                    start_index, r = distinguish_string(str_code, start_index, state)

                    r.append(line)
                    result.append(r)
                else:
                    state = 8
                    start_index, r = distinguis_other(str_code, start_index, state)

                    r.append(line)
                    result.append(r)

            if r[-2] ==word_sign['error']:
                result[-1][1] = result[-1][1] + '请解决!'
                error.append(result[-1])
                del result[-1]
                cnt = 1
                for i in range(start_index, len(str_code)):
                    if str_code[i] == '\n':
                        start_index += cnt
                        line += 1
                        break
                    else:
                        cnt += 1
            #     如果一词报错，全行抛弃
            else:
                start_index += 1
            r = ['无事情', 22]
            if start_index >= len(str_code):
                return result,error
        except:
            start_index += 1
            pass
