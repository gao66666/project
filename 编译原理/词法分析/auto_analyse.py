import ply.lex as lex
from ply.lex import TOKEN
import pandas as pd

df = pd.read_csv('D:\代码\编译原理\词法分析\\type_code.csv')
keyword_sign = df[df['类型'] == '关键词'][['字符', '种别码']].set_index('字符').to_dict()['种别码']
word_sign = df[df['类型'] == '特殊符'][['字符', '种别码']].set_index('字符').to_dict()['种别码']
cal_sign = df[df['类型'] == '运算与逻辑符'][['字符', '种别码']].set_index('字符').to_dict()['种别码']
jie_sign = df[df['类型'] == '界符'][['字符', '种别码']].set_index('字符').to_dict()['种别码']
num_sign = df[df['类型'] == '数值符号'][['字符', '种别码']].set_index('字符').to_dict()['种别码']


def MyLexer():
    # List of token names.   This is always required

    tokens = (
        'error1',
        'error2',
        'error3',
        'error4',
        'error5',
        'error6',
        'error7',
        'unkow_error',
        'operator',
        'zhushi',
        'num_sign',
        'IDN',
        'char_const',
        'string_conts',
        'b_num',
        'keyword',
        'cal_signs',
        'jie_sign',
        'point_num',
        'space',
    )


    def t_error3(t):
        '0[xX]\d?[g-zG-Z].*'
        t.value = (t.value, '进制数字识别错误')
        return t

    def t_b_num(t):
        r'0[xX]+[0-9a-fA-F]+'
        t.value = (t.value, num_sign['进制数'])
        return t

    # 字符常量
    def t_char_const(t):
        r'\'.*\n*.*\''
        t.value = (t.value, 'CHAR')
        return t

    def t_error5(t):
        '\'.*;?\\n'
        t.value = (t.value, '只有一单个引号错误')
        return t
        # 字符串变量

    def t_string_const(t):
        r'\".*\"'
        t.value = (t.value, 'STR')
        return t

    def t_error6(t):
        '\".*\\n'
        t.value = (t.value, '只有一个双引号错误')
        return t

    def t_error7(t):
        '/\*.*\\n'
        t.value = (t.value, '注释错误')
        return t

    def t_error1(t):
        '(\d+[a-zA-Z]+.*)|(_+[a-zA-Z0-9])'
        t.value = (t.value, '标识符命名错误')
        return t

    def t_error2(t):
        '0+[0-8]?\.?\d+[eE]?\d+[+-]?\d*.*'
        t.value = (t.value, '数字前方0识别错误')
        return t

    def t_unkow_error(t):
        '(\@.*)|(\d+\.\d+\.)'
        t.value = (t.value, '未知错误')
        return t

    # t_ignore_comment = r'\t'
    KEYWORDS = list(keyword_sign.keys())
    keyword = '|'.join(keyword.replace(' ', '\s+') for keyword in KEYWORDS)

    @TOKEN(keyword)
    def t_KEYWORD(t):
        # remove spaces
        value = ''.join(x for x in t.value if not x.isspace())
        t.value = (value.lower(), value)

        return t

    # 注释
    def t_zhushi(t):
        '(/\*.*\\n*.*\*/)|(//.*)'
        pass

    # 标识符
    def t_IDN(t):
        '[a-z_A-Z]+[0-9_a-zA-Z]*'
        t.value = (t.value, 'IDN')
        return t

    # 小数
    def t_point_num_sign(t):
        """
        ([1-9]{1}\d*\.+\d*[Ee]?\d*[+-]?\d+)
        |
        (0{1}\.+\d*[Ee]?\d*[+-]?\d+)"""
        t.value = (t.value, 'FLOAT')
        return t

    # 整数
    def t_num_sign(t):
        """
        (\d+[Ee]?\d*[+-]?)
        |0"""
        t.value = (t.value, 'INT10')
        return t

    CALSIGNS = list(cal_sign.keys())
    CALSIGNS = sorted(CALSIGNS, key=lambda x: len(x), reverse=True)
    calsign = '|'.join(['\\' + c.replace(' ', '\s+') for c in CALSIGNS if c not in ['||']])

    @TOKEN(calsign)
    def t_operator(t):
        # remove spaces
        t.value = (t.value, t.value)
        return t

    JIES = list(jie_sign.keys())
    JIES = sorted(JIES, key=lambda x: len(x), reverse=True)
    jiesign = '|'.join(['\\' + c.replace(' ', '\s+') for c in JIES if c not in ['||']])
    er4 = f'[{jiesign}]{2}'

    def t_error4(t):
        '[\+\-\*/=<>]{1}[\+\-\*/=<>]{1}[\+\-\*/=<>]+'
        t.value = (t.value, '多个运算符错误')
        return t

    @TOKEN(jiesign)
    def t_jie_sign(t):
        # remove spaces
        t.value = (t.value, t.value)
        return t

    # Define a rule so we can track line numbers
    def t_newline(t):
        r'\n'
        t.lexer.lineno += 1

    # 错误
    def t_error(t):
        # print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    return lex.lex()


def get_lex(data):
    # data=data.replace(' ','')
    lexer = MyLexer()
    lexer.input(data)
    # Tokenize
    re = []
    err = []
    while True:
        tok = lexer.token()
        if not tok: break  # No more input
        if '错误' in str(tok.value[1]):
            err.append([tok.value[0], tok.value[1], tok.lineno + 1, tok.type, ])
        else:
            re.append([tok.value[0], tok.value[1], tok.lineno + 1, tok.type, ])
    return re, err
# data="""
# /*这是实验一的
# 测试用例*/
# //大家把测试界面截图放文件中
# abc
# 12
# 1.2
# 12a
# 1.2e2+3
# 00.234e3
# 0x34
# 0x3g
# 0912
# ++
# +=
# >==3
# char b = 'b';
# string c = "acc";
# bool d = true;
# //以下是词法分析器的完整测试
# int main()
# {
# 	int n, days1, days2, count = 0;
# 	char input1[11];
# 	int alldays;
# 	int num1, num2;
# 	scanf("%d", &n);
# 	getchar();
# 	int year[3] = { 0 };
# 	for (int i = 0; i < n; i++)
# 	{
# 		memset(year, 0, sizeof(year));
# 		gets(input1);
# 		convert(input1, year);
# 		days2 = diffdays(year[0], year[1], year[2]);
# 		gets(input1);
# 		memset(year, 0, sizeof(year));
# 		convert(input1, year);
# 		days1 = diffdays(year[0], year[1], year[2]);
# 		alldays = days1 - days2;
# 		int temp = diffdays(2018, 12, 8);
# 		num1 = (days1 - temp) % 7;
# 		num2 = (days2 - temp) % 7;
# 		if (num1 == 0 && num2 == 0)
# 		{
# 			printf("%d\n", alldays / 7 + 1);
# 			continue;
# 		}
# 		if (temp < days2)
# 		{
# 			if (num1 != 0)
# 				alldays -= num1;
# 			if (num2 != 0)
# 				alldays -= (7 - num2);
# 			count += 1;
# 		}
# 		else if (temp > days2&&temp < days1)
# 		{
# 			if (num1 != 0)
# 				alldays -= num1;
# 			if (num2 != 0)
# 				alldays -= num2;
# 			count += 1;
# 		}
# 		else if (temp > days1)
# 		{
# 			if (num1 != 0)
# 				alldays -= (7 - num1);
# 			if (num2 != 0)
# 				alldays -= num2;
# 			count += 1;
# 		}
# 		else if (temp == days1 || temp == days2)
# 			count++;
# 		printf("%d\n", alldays / 7 + count);
# 	}
# }
# """
# print(get_lex(data))
