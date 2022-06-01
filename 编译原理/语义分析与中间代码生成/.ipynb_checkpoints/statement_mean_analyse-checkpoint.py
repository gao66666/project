import sys

sys.path.append('D:\\代码\\编译原理')
sys.path.append('D:\\代码')

import pandas as pd
from 语法分析 import LL1
from 语法分析.predict_analyse import get_tree
from 词法分析 import auto_analyse

def Creat_SignTable(code):
    get_tree(code,False)
    # df = pd.DataFrame()
code='''
    int main () {
    int result ;
    int a ;
    int b ;
    char s;
    }

'''
Creat_SignTable(code)