import tkinter
from tkinter import *
import random
import copy


index = 0
timer = 0
score = 0
tsugi = 0
cursor_x = 0
cursor_y = 0
mouse_x = 0
mouse_y = 0
mouse_c = 0
Nagasa = 73
w = h = 20 
flag = 0
mae_x = 0
mae_y = 0
flag = 0

def mouse_move(e):
    global mouse_x, mouse_y
    mouse_x = e.x
    mouse_y = e.y

def mouse_press(e):
    global mouse_c
    mouse_c = 1

def mouse_release(e):
    global mouse_c
    mouse_c = 0

def draw_ban():
    global flag
    cvs.delete("BAN")
    for y in range(8):
        for x in range(8):
            if ban[y][x] > 0:
                cvs.create_image(x*72+60, y*72+60, image=img_ban[ban[y][x]], tag="BAN")
                flag = 0

def make_ban():
    global ban, check, num
    for y in range(8):
        for x in range(8):
            ban[y][x] = num
            num = random.randint(1, 8)

    for y in range(1, 7):
        for x in range(8):
            if ban[y][x] > 0:
                if ban[y-1][x] == ban[y][x] and ban[y+1][x] == ban[y][x]:
                    ban[y][x] = random.randint(1, 8)

    for y in range(8):
        for x in range(1, 7):
            if ban[y][x] > 0:
                if ban[y][x-1] == ban[y][x] and ban[y][x+1] == ban[y][x]:
                    ban[y][x] = random.randint(1,8)

    for y in range(1, 7):
        for x in range(1, 7):
            if ban[y][x] > 0:
                if ban[y-1][x] == ban[y][x] and ban[y+1][x] == ban[y][x] or ban[y][x-1] == ban[y][x] and ban[y][x+1] == ban[y][x]:
                    ban[y][x] = random.randint(1, 8)
                    
    check = copy.deepcopy(ban)


def check_ban():
    global ban
    for y in range(1, 7):
        for x in range(8):
            if ban[y][x] > 0:
                if ban[y-1][x] == ban[y][x] and ban[y+1][x] == ban[y][x]:
                    ban[y-1][x] = 0
                    ban[y][x] = 0
                    ban[y+1][x] = 0
                    draw_ban()

    for y in range(8):
        for x in range(1, 7):
            if ban[y][x] > 0:
                if ban[y][x-1] == ban[y][x] and ban[y][x+1] == ban[y][x]:
                    ban[y][x-1] = 0
                    ban[y][x] = 0
                    ban[y][x+1] = 0
                    draw_ban()

def sweep_ban():
    num = 0
    for y in range(8):
        for x in range(8):
            if ban[y][x] == 0:
                ban[y][x] = 0
                num = num + 1
    return num

def drop_ban():
    flg = False
    for y in range(7, -1, -1):
        for x in range(8):
            if ban[y][x] != 0 and ban[y+1][x] == 0:
                ban[y+1][x] = ban[y][x]
                ban[y][x] = 0
    return flg

def over_ban():
    n = 0
    for x in range(8):
        if ban[6][x] == 0:
            n = n + 1
    if n == 8:
        return True

    return False

def draw_txt(txt, x, y, siz, col, tg):
    fnt = ('Times New Roman', siz, 'bold')
    cvs.create_text(x, y, text=txt, fill=col, font=fnt, tag=tg)

def game_main():
    global index, timer, score, tsugi, flag, mae_x, mae_y
    global cursor_x, cursor_y, mouse_c
    if index == 0:
        draw_txt('パズルおとし', 312, 240, 100, 'violet', 'TITLE')
        draw_txt('Click to start', 312, 560, 50, 'orange', 'TITLE')
        index = 1
        mouse_c = 0
    elif index == 1:
        if mouse_c == 1:
            mouse_c = 0
            score = 0
            tsugi = 0
            cursor_x = 0
            cursor_y = 0
            draw_ban()
            cvs.delete('TITLE')
            index = 2
    
    elif index == 2:
        if drop_ban() == False:
            index = 3
        draw_ban()

    elif index == 3:
        if  over_ban() == True:
            draw_txt('CLEAR', 312, 348, 60, 'red', 'OVER')
            if mouse_c == 1:
                cvs.delete('OVER')
                make_ban()
                index = 0
                draw_ban()

        if 24 <= mouse_x and mouse_x < 24+72*8 and 24 <= mouse_y and mouse_y < 24+72*10:
            cursor_x = int((mouse_x-24)/72)
            cursor_y = int((mouse_y-24)/72)
            if flag == 0:
                mae_x = cursor_x
                mae_y = cursor_y
            flag = 1

            if mouse_c == 1:       
                if cursor_y != mae_y or cursor_x != mae_x:
                    dummy = ban[cursor_y][cursor_x]
                    ban[cursor_y][cursor_x] = check[mae_y][mae_x]
                    ban[mae_y][mae_x] = dummy
                    draw_ban()
       
            if mouse_c == 0:
                check_ban()
                drop_ban()
                sc = sweep_ban()
                score = score + sc 
            
    cvs.delete('INFO')
    draw_txt('SCORE' + str(score), 130, 60, 32, 'blue', 'INFO')
    root.after(10, game_main)

root = tkinter.Tk()
root.title('パズルおとし')
root.resizable(False, False)
root.bind('<Motion>', mouse_move)
root.bind('<ButtonPress>', mouse_press)
root.bind("<ButtonRelease>", mouse_release)
cvs = tkinter.Canvas(root, width=620, height=620)
cvs.pack()

num = random.randint(0, 8)
ban = [[0 for i in range(8)] for j in range(9)]
check = [[0 for i in range(8)] for j in range(9)]
make_ban()

        
for i in range(9):
    if i == 0 or i == 8:
        cvs.create_line(w, h+i*Nagasa, w+8 * Nagasa, h+i*Nagasa, fill='black', width=2.0)
        cvs.create_line(w+i*Nagasa, h, w+i*Nagasa, h+8*Nagasa, fill='black', width=2.0)
    if i == 6:
        cvs.create_line(w, h+i*Nagasa, w+8 * Nagasa, h+i*Nagasa, fill='blue', width=1.5)

img_ban = [
    None,
    tkinter.PhotoImage(file="1.png"),
    tkinter.PhotoImage(file="2.png"),
    tkinter.PhotoImage(file="3.png"),
    tkinter.PhotoImage(file="4.png"),
    tkinter.PhotoImage(file="5.png"),
    tkinter.PhotoImage(file="6.png"),
    tkinter.PhotoImage(file="7.png"),
    tkinter.PhotoImage(file="8.png")
]

draw_ban()
game_main()
root.mainloop()