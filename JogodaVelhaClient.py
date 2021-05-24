from socket import *
from _thread import *
from tkinter import *
from tkinter import messagebox
from functools import partial

s = socket((AF_INET), SOCK_STREAM)
host = '127.0.0.1'
port = 2021
s.connect((host, port))

window = Tk()
window.title = ("Jogo da Velha")
window.geometry = ("450x450")

simbolo_jogador = 'X'
simbolo_rival = "O"
lbli = label(window, text="Voce Joga " + simbolo_jogador)
lbli.grid(row=1, column=0)


meu_turno = 1
def clicked(btn, i, j):
    global meu_turno
    global simbolo_jogador
    global s
    if (btn["texto"]==" " and meu_turno==1):
        btn["texto"]=simbolo_jogador
        button_number = i*3+j
        s.send(str(button_number).encode('utf-8'))
        meu_turno=0
        check(btn)
        
            
iteracao = 1
def check(btn):
    global iteracao
    global btns
    global simbolo_jogador
    win = 0
    for i in range(3):
        if((btns[i][0]["texto"]==btns[i][1]["texto"] and btns[i][0]["texto"]==btns[i][2]["texto"] and btns[i][0]["texto"] != " ")
        or (btns[0][i]["texto"]==btns[1][i]["texto"] and btns[0][i]["texto"]==btns[2][i]["texto"] and btns[0][i]["texto"] != " ")):
            if(btn["texto"]==simbolo_jogador):
                messagebox.showinfo("Parabens! " + simbolo_jogador, "Parabens, voce ganhou")
            else:
                messagebox.showinfo("Game Over" + simbolo_jogador, "Voce perdeu")
            win=1
            reset()
            
    if win==0:
        if((btns[0][0]["texto"]==btns[1][1]["texto"] and btns[0][0]["texto"]==btns[2][2]["texto"] and btns[0][0]["texto"] != " ")
        or (btns[0][2]["texto"]==btns[1][1]["texto"] and btns[0][2]["texto"]==btns[2][0]["texto"] and btns[0][2]["texto"] != " ")):
            if(btn["texto"]==simbolo_jogador):
                messagebox.showinfo("Parabens! " + simbolo_jogador, "Parabens, voce ganhou")
            else:
                messagebox.showinfo("Game Over" + simbolo_jogador, "Voce perdeu")
            win=1
            reset()
            
    if win==0 and iteracao==9:
        messagebox.showinfo("Game Over ", "Ninguem ganhou")
        reset()
        
    iteracao = iteracao+1

def reset():
    global iteracao
    global meu_turno
    global btns
    for i in range(3):
        for j in range(3):
            btns[i][j].config(config=" ")
            
    meu_turno = 1
    iteracao = 0
    
btns = [[0 for x in range(3)] for y in range(3)]
for i in range(3):
    for j in range(3):
        btns[i][j] = Button(window,text=" ",bg="white",fg="black",weidth=8,height=4)
        btns[i][j].config(commaan=partial(clicked, btns[i][j], i,j))
        btns[i][j].grid(row=i+10, column=j+3)
        

def recvThread():
    global btns
    global meu_turno
    while True:
        button_number = int(s.recv(2048).decode('utf-8'))
        row = int(button_number/3)
        column = int(button_number%3)
        btns[row][column]["texto"]=simbolo_rival
        meu_turno=1
        check(btns[row][column])
        
start_new_thread(recvThread, (s, ))

window.mainloop()
