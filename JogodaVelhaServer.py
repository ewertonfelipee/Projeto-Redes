from tkinter import *
from tkinter import messagebox
from functools import partial
from socket import *
from _thread import *

s = socket((AF_INET), SOCK_STREAM)
host = "127.0.0.1"
port = 2021
s.bind((host, port))
s.listen(12)
c, ad = s.accept()

window = Tk()
window.title("Jogo da velha")
window.geometry("300x300")

simbolo_jogador = 'O'
simbolo_rival = 'X'
lbli = Label(window, text = "Você joga com: " + simbolo_jogador + ".")
lbli.grid(row=1, column=0)

meu_turno = 0
def clicked (btn, i, j):
    global meu_turno
    global simbolo_jogador
    global c
    if (btn["text"] == " " and meu_turno == 1):
        btn["text"] = simbolo_jogador
        button_number = i*3+j
        c.send(str(button_number).encode('utf-8'))
        meu_turno=0
        check(btn)

iteracao = 1
def check (btn):
    global iteracao
    global btns
    global simbolo_jogador
    win = 0
    for i in range(3):
        if ((btns[i][0]["text"] == btns[i][1]["text"] and btns[i][0]["text"] == btns[i][2]["text"] and btns[i][0]["text"] != " ")
        or (btns[0][i]["text"] == btns[1][i]["text"] and btns[0][i]["text"] == btns[2][i]["text"] and btns[0][i]["text"] != " ")):
            if (btn["text"] == simbolo_jogador):
                messagebox.showinfo("Vitória!",  "Parabéns!")
            else:
                messagebox.showinfo("Derrota!", "Mais sorte na próxima partida!")
            win = 1
            reset()
    
    if (win == 0):
        if ((btns[0][0]["text"] == btns[1][1]["text"] and btns[0][0]["text"] == btns[2][2]["text"] and btns[0][0]["text"] != " ")
        or (btns[0][2]["text"] == btns[1][1]["text"] and btns[0][2]["text"] == btns[2][0]["text"] and btns[0][2]["text"] != " ")):
            if(btn["text"]==simbolo_jogador):
                messagebox.showinfo("Vitória!",  "Parabéns!")
            else:
                messagebox.showinfo("Derrota!", "Mais sorte na próxima partida!")
            win = 1
            reset()
    
    if ((win == 0) and (iteracao == 9)):
        messagebox.showinfo("Velha!", "Ninguém ganhou!")
        reset()
    
    iteracao += 1

def reset ():
    global iteracao
    global meu_turno
    global btns
    for i in range(3):
        for j in range(3):
            btns[i][j].config(text = " ")
    meu_turno = 0
    iteracao = 0

btns = [[0 for x in range(3)] for y in range(3)]
for i in range(3):
    for j in range(3):
        btns[i][j] = Button(window, text = " ", bg = "red", fg = "black", width = 8, height = 4)
        btns[i][j].config(command = partial(clicked, btns[i][j], i, j))
        btns[i][j].grid(row = i+10, column = j+3)

def recvThread (c):
    global btns
    global meu_turno
    while True:
        button_number = int(c.recv(2).decode('utf-8'))
        row = int(button_number/3)
        column = int(button_number%3)
        btns[row][column]["text"] = simbolo_rival
        meu_turno = 1
        check(btns[row][column])
        
start_new_thread(recvThread, (c, ))

window.mainloop()
