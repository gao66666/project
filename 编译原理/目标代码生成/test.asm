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
a db 1
data ends

data segment
N db 0
data ends

p_1:
mov al,10
mov N,al
p_2:
mov al,1
mov a,al

p3:
mov ax,3
push ax
p4:
mov ax,4
push ax
p5:
call sum

sum:
push bp
mov bp,sp
sub sp,2

p27:
mov AX,DATA
mov DS,AX
LEA DX,OUTPUT
MOV AH,09H
INT 21H

mov al,a
mov bl,10
cmp al,bl
JA _C0
JMP far ptr pcase1
_C0:JMP far ptr pcase2

pcase1:
add a,30H
mov dl,a
mov ah,2
INT 21H
mov DL,0aH
mov AH,02H
INT 21H
JMP far ptr quit

pcase2:
mov al,a
mov bl,100
cmp al,bl
JA _C1
JMP far ptr pcase3
_C1:JMP far ptr pcase4

pcase3:
mov ax,0
add al,a
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
add al,a
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


