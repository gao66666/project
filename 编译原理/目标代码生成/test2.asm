assume cs:code,ds:data,ss:stack,es:extended

extended segment
	db 1024 dup (0)
extended ends

stack segment
	db 1024 dup (0)
stack ends

data segment
	t_buff_p db 256 dup (24h)
	t_buff_s db 256 dup (0)
	OUTPUT db "Your output is:",'$'
data ends

code segment
start:mov ax,extended
	mov es,ax
	mov ax,stack
	mov ss,ax
	mov sp,1024
	mov bp,sp
	mov ax,data
	mov ds,ax

data segment
a db 2
data ends

data segment
i db 1
data ends

data segment
sum db 5
data ends

data segment
t2 db 0
data ends

data segment
t3 db 0
data ends

p_1:
mov al,2
mov a,al
p_2:
mov al,1
mov i,al
p_3:
mov al,5
mov sum,al
p_4:
mov al,0
mov t2,al
p_5:
mov al,0
mov t3,al

p2:
MOV AL,1
MOV i,AL
p3:
MOV AL,i
MOV BL,2
CMP AL,BL
JNA _LE2
JMP far ptr p13
_LE2:JMP far ptr p8
p5:
MOV AL,i
ADD AL,1
MOV t2,AL
p6:
MOV AL,t2
MOV i,AL
p7:
JMP far ptr p3
p8:
MOV AL,a
MOV BL,i
CMP AL,BL
JE _EQ7
JMP far ptr p13
_EQ7:JMP far ptr p10
p10:
MOV AX,0
MOV AL,sum
MOV BL,2
DIV BL
MOV t3,AL
p11:
MOV AL,t3
MOV sum,AL
p12:
JMP far ptr p5
p13:
mov AX,DATA
mov DS,AX
LEA DX,OUTPUT
MOV AH,09H
INT 21H

mov al,sum
mov bl,10
cmp al,bl
JA _C0
JMP far ptr pcase1
_C0:JMP far ptr pcase2

pcase1:
add sum,30H
mov dl,sum
mov ah,2
INT 21H
mov DL,0aH
mov AH,02H
INT 21H
JMP far ptr quit

pcase2:
mov al,sum
mov bl,100
cmp al,bl
JA _C1
JMP far ptr pcase3
_C1:JMP far ptr pcase4

pcase3:
mov ax,0
add al,sum
mov bl,10
div bl
mov dx,ax
add dx,3030h
mov ah,2
int 21h
mov dl,dh
mov ah,2
int 21h
mov dl,0ah
mov ah,02h
int 21h
JMP far ptr quit

pcase4:
mov ax,0
add al,sum
mov bl,100
div bl
mov dl,al
add dl,30h
mov al,ah
push ax
mov ah,2
int 21h

pop ax
and ah,00h
mov bl,10
div bl

mov dx,ax
add dx,3030h
mov ah,2
int 21h

mov dl,dh
mov ah,2
int 21h
JMP far ptr quit

quit:
mov ah,4ch
INT 21H
code ends
end start

