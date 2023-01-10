#!/usr/bin/env python3
#importing needed modules
from tkinter import *
from collections import deque
import heapq,time,random

#on hovering
def on_enter(e):
    e.widget.config(cursor = 'hand2',bg ='#5f669c')
#on unhovering
def on_leave(e):
    e.widget.config(cursor='',bg = '#6d75c2'  if not e.widget['text'] != 'Run' else '#222852')
#hiding the algo menu
def hide_menu(e,d):
    d.place_forget()
    e.widget.bind('<Button-1>', lambda e: show_menu(e,d))
#showing the algo menu
def show_menu(e,d):
    d.place(x=364,y=37)
    d.tkraise()
    e.widget.bind('<Button-1>', lambda e: hide_menu(e,d))
#picking the algo
def pick(e,curr_algo,menu,button):
    curr_algo.config(text = e['text'])
    time.sleep(0.09)
    menu.place_forget()
    button.bind('<Button-1>', lambda e: show_menu(e,menu))
#block hover
def block_enter(e,m):
    if m.itemcget(e,'fill') == '#04071c':
        m.itemconfig(e,fill = '#888ebd')

#block unhover
def block_leave(e,m):
    if m.itemcget(e,'fill') == '#888ebd':
        m.itemconfig(e,fill = '#04071c')


#changing block status
def change_block_status(block,canv,mode,):
    if mode['text'].split()[2] == 'Start' and canv.itemcget(block,'fill') !='red':
        canv.itemconfigure('start',fill = '#04071c')
        canv.dtag('start')
        canv.itemconfigure(block,fill = 'yellow')
        canv.addtag_withtag('start',block)
    elif mode['text'].split()[2] == 'Target' and canv.itemcget(block,'fill') !='yellow':
        canv.itemconfigure('end',fill = '#04071c')
        canv.dtag('end')
        canv.itemconfigure(block,fill = 'red',tags = 'end')
    elif mode['text'].split()[2] == 'Wall':
        curr_color = canv.itemcget(block,'fill')
        if curr_color == '#2c4b7d':
            canv.itemconfigure(block, fill = '#04071c')
        elif curr_color == '#888ebd':
            canv.itemconfigure(block, fill = '#2c4b7d' )

#clearing the grid
def clear_grid(e,canv,mat,root):
    canv.dtag('start') ; canv.dtag('end')
    grads = ['#2379fa','#3684f7','#4a8ff7','#5e94e6','#7dadf5','#93baf5','#a8c5f0']
    grads.reverse()
    q = deque()
    for i in range(40):
        for j in range(40):
            block = mat[i][j]
            q.append((i,j))
            if len(q) == 8:
                prev = q.popleft()
                if canv.itemcget(prev,'fill') not in ('red','yellow'):
                    canv.itemconfig(mat[prev[0]][prev[1]],fill = '#04071c')
            for l in range(len(q)):
                x,y = q[l]
                canv.itemconfig(mat[x][y],fill = grads[l])                
            root.update_idletasks()
    for i,j in q:
        canv.itemconfig(mat[i][j],fill = '#04071c')

    if e.widget['text'] == 'Clear Grid':
        canv.itemconfigure(mat[20][8],fill = 'yellow')
        canv.addtag_withtag('start',mat[20][8])
        canv.itemconfigure(mat[20][32],fill = 'red')
        canv.addtag_withtag('end',mat[20][32])
    root.update_idletasks()


def all_walls(e,canv,mat,root):
    for i in range(40):
        for j in range(40):
            block  = mat[i][j]
            time.sleep(0.0001)
            canv.itemconfig(block,fill = '#2c4b7d')
            root.update_idletasks()
    root.update()


#generating a random maze
def create_Maze(e,canv,mat,root):
    canv.dtag('start') ; canv.dtag('end')
    all_walls(e,canv,mat,root)
    cells = {(x, y) for x in range(39) for y in range(39)}
    walls = {(x, y) for x in range(39) for y in range(39) if x > 0 and y > 0}
    while walls:
        x, y = random.choice(list(walls))
        walls.remove((x, y))
        if (x-1, y) in cells and (x+1, y) in cells:
            canv.itemconfig(mat[x][y],fill = '#04071c')            
            if (x-1, y) != (x+1, y):
                cells.remove((x-1, y))
                cells.remove((x+1, y))
                cells.add((x, y))
        elif (x, y-1) in cells and (x, y+1) in cells:
            canv.itemconfig(mat[x][y],fill = '#04071c')            
    
            if (x, y-1) != (x, y+1):
                cells.remove((x, y-1))
                cells.remove((x, y+1))
                cells.add((x, y))
        else:
            continue
        root.update_idletasks()
    
    start_x, start_y = random.sample(cells,1)[0]
    cells.remove((start_x,start_y))
    end_x, end_y = random.sample(cells,1)[0]
    canv.itemconfig(mat[start_x][start_y],fill = 'yellow')
    canv.itemconfig(mat[end_x][end_y],fill = 'red')
    canv.addtag_withtag('start',mat[start_x][start_y])
    canv.addtag_withtag('end',mat[end_x][end_y])
    root.update()
        
#set mode
def set_mode(e,curr):
    temp = e.widget['text'].split()[1]
    curr.config(text = 'Current Mode: '+temp)

#main function
def run():
    
    #main window configuration
    root = Tk()
    root.geometry('500x500')
    root.title('Path Finding Visualizer')
    root.config(bg = '#04071c')
    root.resizable(False,False)

    #top bar
    top_bar = Frame(bg = '#10111c')
    top_bar.pack(side = TOP,fill = X,ipady=(10))

    #bottom bar
    bottom_bar = Frame(bg = '#10111c')
    bottom_bar.pack(side = BOTTOM,fill = X,ipady=(2))

    # a label for current mode
    current_mode = Label(bg = '#04071c',text = 'Current Mode: Wall',fg = 'white',bd=1)
    current_mode.place(x = 45,y = 40)
    
    # algorithms dropdown menu
    algo_menu = Frame(bg = '#222852')
    algo_list = ['Depth First Search','Breadth First Search','Dijkstra','Bellman ford','A Star']
    for name in algo_list:
        label = Label(master = algo_menu,text = name,bg = '#222852',fg = 'white',highlightbackground='#8085ab',highlightcolor='#8085ab',highlightthickness=1,font = ('',8))
        label.bind('<Enter>', lambda e: on_enter(e))
        label.bind('<Leave>', lambda e: on_leave(e))
        label.pack(side=TOP,fill=BOTH,ipady=(5),ipadx=(5))
        label.bind('<Button-1>',lambda e,l=label: pick(l,curr_algo,algo_menu,drop_button))
    
    #run button
    run_button = Label(master = top_bar,text = 'Run',bg = '#6d75c2',fg = 'white',font = ('',8))
    run_button.pack(side = LEFT,padx = (5,0),ipadx=(5),ipady=(5))
    run_button.bind('<Enter>', lambda e: on_enter(e))
    run_button.bind('<Leave>', lambda e: on_leave(e))

    # pick start button
    pick_start_button = Label(master = top_bar,text = 'Set Start',bg = '#222852',fg = 'white',font = ('',8))
    pick_start_button.pack(side = LEFT,padx = (5,0),ipadx=(5),ipady=(5))
    pick_start_button.bind('<Enter>', lambda e: on_enter(e))
    pick_start_button.bind('<Leave>', lambda e: on_leave(e))
    pick_start_button.bind('<Button-1>',lambda e: set_mode(e,current_mode))


    #pick end button
    pick_end_button = Label(master = top_bar,text = 'Set Target',bg = '#222852',fg = 'white',font = ('',8))
    pick_end_button.pack(side = LEFT,padx = (5,0),ipadx=(5),ipady=(5))
    pick_end_button.bind('<Enter>', lambda e: on_enter(e))
    pick_end_button.bind('<Leave>', lambda e: on_leave(e))
    pick_end_button.bind('<Button-1>',lambda e: set_mode(e,current_mode))

    #pick wall button
    pick_wall_button = Label(master = top_bar,text = 'Create Wall',bg = '#222852',fg = 'white',font = ('',8))
    pick_wall_button.pack(side = LEFT,padx = (5,0),ipadx=(5),ipady=(5))
    pick_wall_button.bind('<Enter>', lambda e: on_enter(e))
    pick_wall_button.bind('<Leave>', lambda e: on_leave(e))
    pick_wall_button.bind('<Button-1>',lambda e: set_mode(e,current_mode))

    #drop down button
    drop_button = Label(master = top_bar,text = '↓',bg = '#222852',fg = 'white',font = ('',8))
    drop_button.pack(side = RIGHT,padx = (0,10),ipadx=(5),ipady=(5))
    drop_button.bind('<Enter>', lambda e: on_enter(e))
    drop_button.bind('<Leave>', lambda e: on_leave(e))
    drop_button.bind('<Button-1>', lambda e: show_menu(e,algo_menu))
    
    
    #curr algo indicator
    curr_algo = Label(master = top_bar,text = 'Depth First Search',bg = '#222852',fg = 'white')
    curr_algo.config(font = ('',8))
    curr_algo.pack(side = RIGHT,padx = (0),ipadx=(5),ipady=(5))

    #main grid for visualization
    main_canvas = Canvas(bd = 0,highlightthickness=0,width=401,height=401,bg = '#04071c' )
    main_canvas.pack(side = TOP,pady=(20,0))
    mat = [[0]*40 for _ in range(40)]
    for y in range(0,400,10):
        for x in range(0,400,10):
            mat[y//10][x//10] = main_canvas.create_rectangle(x,y,x+10,y+10,outline='#222852',fill = '#04071c')
            main_canvas.tag_bind(mat[y//10][x//10],'<Enter>',lambda e,val = mat[y//10][x//10]: block_enter(val,main_canvas))
            main_canvas.tag_bind(mat[y//10][x//10],'<Leave>',lambda e,val = mat[y//10][x//10]: block_leave(val,main_canvas))
            main_canvas.tag_bind(mat[y//10][x//10],'<Button-1>',lambda e,val = mat[y//10][x//10]: change_block_status(val,main_canvas,current_mode))
    
    #setting initial start and end positions
    main_canvas.itemconfigure(mat[20][8],fill = 'yellow')
    main_canvas.addtag_withtag('start',mat[20][8])
    main_canvas.itemconfigure(mat[20][32],fill = 'red')
    main_canvas.addtag_withtag('end',mat[20][32])
    
    #clearing the grid
    clear_grid_button = Label(master = bottom_bar,text = 'Clear Grid',bg = '#222852',fg = 'white',font = ('',8))
    clear_grid_button.pack(side = LEFT,padx = (5,0),ipadx=(4),ipady=(4))
    clear_grid_button.bind('<Enter>', lambda e: on_enter(e))
    clear_grid_button.bind('<Leave>', lambda e: on_leave(e))
    clear_grid_button.bind('<Button-1>', lambda e: clear_grid(e,main_canvas,mat,root))

    #clear walls
    maze_button = Label(master = bottom_bar,text = 'Generate Maze',bg = '#222852',fg = 'white',font = ('',8))
    maze_button.pack(side = LEFT,padx = (5,0),ipadx=(4),ipady=(4))
    maze_button.bind('<Enter>', lambda e: on_enter(e))
    maze_button.bind('<Leave>', lambda e: on_leave(e))
    maze_button.bind('<Button-1>', lambda e: create_Maze(e,main_canvas,mat,root))
    
    #application loop
    root.mainloop()

    

if __name__ == '__main__':
    #start of application
    run()