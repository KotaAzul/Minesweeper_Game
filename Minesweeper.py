from tkinter import *
from cell import Cell
import settings
import utils

# opens a window and sets window vaiables
root = Tk()
root.configure(bg="black") # background color
root.geometry(f'{settings.WIDTH}x{settings.HEIGHT}') # window pixel size
root.title ("Incendiary Device Hoover (TM)")
#root.resizable(False, False) #prevents user from changing WIDTH and HEIGHT dimensions

# create frames within window
top_frame = Frame(
    root,
    bg = 'pink',
    width=settings.WIDTH,
    height=utils.height_prct(10),
)
top_frame.place(x=0, y=0)

game_title = Label(
    top_frame,
    bg='pink',
    fg='black',
    text='Incendiary Device Hoover',
    font=('', 45)
)
game_title.place(x=utils.width_prct(25),y=0)

# left_frame = Frame(
#     root,
#     bg='cyan', 
#     width=utils.width_prct(25),
#     height=utils.height_prct(90) 
# )
# left_frame.place(x=0, y=utils.height_prct(10))

center_frame = Frame(
    root,
    bg='palegreen1',
    width=utils.width_prct(100),
    height=utils.height_prct(90),
)
center_frame.place(x=utils.width_prct(0), y=utils.height_prct(10))
center_frame.columnconfigure(0, weight=1)
center_frame.rowconfigure(1, weight=1)

#create the main game button grid in center_frame 
for x in range(settings.GRID_SIZE):
    for y in range (settings.GRID_SIZE):
        c = Cell(x,y)
        c.create_btn_object(center_frame)
        c.cell_btn_object.grid(
            column=x, row=y, sticky=NSEW
        )
        
print(Cell.all) #!delete for final
print(len(Cell.all)) #!delete for final

Cell.randomize_mines()

#Call the label of Cell class
Cell.create_cell_count_label(top_frame)
Cell.cell_count_label_object.place(x=0,y=0)



root.mainloop() #closes window