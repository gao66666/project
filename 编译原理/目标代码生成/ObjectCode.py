


class Objecet_Code:
    def __init__(self, mcode, var, out):
        self.mcode = mcode
        self.var = var
        self.out = out
        self.ocode = {}

    def transfor(self):
        for code, i in zip(self.mcode, range(len(self.mcode))):
            t = None
            if code[0] == '=':
                t = 'MOV AL,{}\nMOV {},AL'.format(code[1], code[3])
            elif code[0] == '+':
                t = 'MOV AL,{}\nADD AL,{}\nMOV {},AL'.format(code[1], code[2], code[3])
            elif code[0] == '-':
                t = 'MOV AL,{}\nSUB AL,{}\nMOV {},AL'.format(code[1], code[2], code[3])
            elif code[0] == '*':
                t = 'MOV AL,{}\nMOV BL,{}\nMUL BL\nMOV {},AL'.format(code[1], code[2], code[3])
            elif code[0] == '/':
                t = 'MOV AX,0\nMOV AL,{}\nMOV BL,{}\nDIV BL\nMOV {},AL'.format(code[1], code[2], code[3])
            elif code[0] == '%':
                t = 'MOV AX,0\nMOV AL,{}\nMOV BL,{}\nDIV BL\nMOV {},AH'.format(code[1], code[2], code[3])
            elif code[0] == 'j<':
                t = 'MOV AL,{}\nMOV BL,{}\nCMP AL,BL\nJB _LT{}\nJMP far ptr p{}\n_LT{}:JMP far ptr p{}'.format(code[1], code[2], i, self.mcode[i+1][3], i, code[3])
            elif code[0] == 'j<=':
                t = 'MOV AL,{}\nMOV BL,{}\nCMP AL,BL\nJNA _LE{}\nJMP far ptr p{}\n_LE{}:JMP far ptr p{}'.format(code[1], code[2], i, self.mcode[i+1][3], i, code[3])
            elif code[0] == 'j>':
                t = 'MOV AL,{}\nMOV BL,{}\nCMP AL,BL\nJA _GT{}\nJMP far ptr p{}\n_GT{}:JMP far ptr p{}'.format(code[1], code[2], i, self.mcode[i+1][3], i, code[3])
            elif code[0] == 'j>=':
                t = 'MOV AL,{}\nMOV BL,{}\nCMP AL,BL\nJNB _GE{}\nJMP far ptr p{}\n_GE{}:JMP far ptr p{}'.format(code[1], code[2], i, self.mcode[i+1][3], i, code[3])
            elif code[0] == 'j==':
                t = 'MOV AL,{}\nMOV BL,{}\nCMP AL,BL\nJE _EQ{}\nJMP far ptr p{}\n_EQ{}:JMP far ptr p{}'.format(code[1], code[2], i, self.mcode[i+1][3], i, code[3])
            elif code[0] == 'j':
                if self.mcode[i-1][0] in ['j<', 'j<=', 'j>', 'j>=', 'j==']:
                    continue
                t = 'JMP far ptr p{}'.format(code[3])
            self.ocode['p' + str(i+1)] = t
        write = []
        for k in self.var:
            write.append('{} db {}'.format(k[0], k[1]))
        for m in self.mcode:
            if 't' in str(m[3]):
                write.append('{} db 0'.format(m[3]))
        start = 'assume cs:code,ds:data,ss:stack,es:extended\n\n' \
                'extended segment\n\tdb 1024 dup (0)\nextended ends\n\n' \
                'stack segment\n\tdb 1024 dup (0)\nstack ends\n\n' \
                'data segment\n\tt_buff_p db 256 dup (24h)\n\tt_buff_s db 256 dup (0)\n\tOUTPUT db "The result is: ",' \
                '\'$\'\ndata ends\n\n' \
                'code segment\nstart:mov ax,extended\n\tmov es,ax\n\tmov ax,stack\n\tmov ss,ax\n\tmov sp,1024\n\tmov ' \
                'bp,sp\n\tmov ax,data\n\tmov ds,ax\n\n'
        data_seg = ''
        for w in write:
            data_seg = data_seg + 'data segment\n' + w + '\ndata ends\n\n'
        p_seg = ''
        for i in range(len(write)):
            w = write[i].split(' ')
            p_seg = p_seg + 'p_{}:\n'.format(str(i+1)) + 'mov al,{}\nmov {},al\n'.format(w[2], w[0])
        start = start + data_seg + p_seg
        end = 'mov AX,DATA\nmov DS,AX\nLEA DX,OUTPUT\nMOV AH,09H\nINT 21H\n\n' \
              'mov al,{}\nmov bl,10\ncmp al,bl\nJA _C0\nJMP far ptr pcase1\n_C0:JMP far ptr pcase2\n\n' \
              'pcase1:\nadd {},30H\nmov dl,{}\nmov ah,2\nINT 21H\nmov DL,0aH\nmov AH,02H\nINT 21H\nJMP far ptr quit\n\n' \
              'pcase2:\nmov al,{}\nmov bl,100\ncmp al,bl\nJA _C1\nJMP far ptr pcase3\n_C1:JMP far ptr pcase4\n\n' \
              'pcase3:\nmov ax,0\nadd al,{}\nmov bl,10\ndiv bl\nmov dx,ax\nadd dx,3030h\nmov ah,2\nint 21h\nmov dl,' \
              'dh\nmov ah,2\nint 21h\nmov dl,0ah\nmov ah,02h\nint 21h\nJMP far ptr quit\n\n' \
              'pcase4:\nmov ax,0\nadd al,{}\nmov bl,100\ndiv bl\nmov dl,al\nadd dl,30h\nmov al,ah\npush ax\nmov ah,' \
              '2\nint 21h\n\n' \
              'pop ax\nand ah,00h\nmov bl,10\ndiv bl\n\nmov dx,ax\nadd dx,3030h\nmov ah,2\nint 21h\n\n' \
              'mov dl,dh\nmov ah,2\nint 21h\nJMP far ptr quit\n\n' \
              'quit:\nmov ah,4ch\nINT 21H\ncode ends\nend start\n'.format(self.out, self.out, self.out, self.out, self.out, self.out)
        self.ocode['p1'] = start
        self.ocode[list(self.ocode.keys())[-1]] = end
        assembly = ''
        for k, v in self.ocode.items():

            if k == 'p1':
                assembly = assembly + v + '\n'
            else:
                assembly = assembly + k + ':\n' + v + '\n'
        # with open(r'test2.asm', 'w', encoding='utf-8') as f:
        #     f.write(assembly)
        return assembly


# if __name__ == '__main__':
    # quan = [['main', '', '', ''], ['=', '1', '', 'i'], ['j<=', 'i', '2', 8], ['j', '', '', 13], ['+', 'i', '1', 't2'], ['=', 't2', '', 'i'], ['j', '', '', 3], ['j==', 'a', 'i', 10], ['j', '', '', 13], ['/', 'sum', '2', 't3'], ['=', 't3', '', 'sum'], ['j', '', '', 5], ['sys', '', '', '']]
    # var_ = [['a','2'], ['i','1'] ,['sum','5'],]
    # o = Objecet_Code(quan, var_, 'sum')
    # f=o.transfor()
    # print(f)
    # from 语义分析与中间代码生成.statement_mean_analyse import Creat_SignTable
    # from 语义分析与中间代码生成 import statement_mean_analyse
    # mid,symbol=Creat_SignTable(
    #     '''
    #         int main ( ) {
    #         int i = 1 ;
    #         int a = 2 ;
    #         int sum = 6 ;
    #         if ( a > i ) {
    #         sum = a + sum ;
    #         for ( i = 0 ; i < a ; i = i + 1 )
    #         {
    #         sum = sum + i ;
    #         }
    #         }
    #         }
    #     '''
    #
    # )
    # print(mid)
    # target=Objecet_Code(mid,symbol,'sum')
    # f=target.transfor()
    # print(f)