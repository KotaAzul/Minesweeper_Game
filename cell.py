from tkinter import Button, Label
import random
from tkinter.constants import BOTH
from typing import Sized
import settings
import ctypes
import sys
import os

class Cell:
    all =[]
    cell_count_label_object=None
    def __init__(self, x, y, is_mine=False, is_revealed=False):
        self.is_mine=is_mine
        self.is_revealed=is_revealed
        self.cell_btn_object=None
        self.x=x
        self.y=y
        #Append the object into the Cell.all list
        Cell.all.append(self)

    def __repr__(self):
        return f"Cell {self.x},{self.y}"


    def create_btn_object(self, location):
        btn = Button(
            location,
            width=2, #! modify to fit in whole space, scaling button size up/down
            height=1, #! modify to fit in whole space, scaling button size up/down
            bg='steel blue'
            #text=f'{self.x},{self.y}' #! delete for final
            #font=('',settings.GRID_SIZE)
        )
        btn.bind('<Button-1>', self.left_click_actions) 
        btn.bind('<Button-3>', self.right_click_actions)
        btn.bind('<Button-2>', self.middle_click_actions)
        self.cell_btn_object = btn
    
    
    def left_click_actions(self, event):
        if self.is_mine:
            self.show_mine()
        elif self.surrounding_cells_mine_count == 0:
            self.safe_cascade()
        else:
            self.show_cell()
        
        #check win condition
        revealed_cell_count = [cell for cell in Cell.all if cell.is_revealed]
        if (len(Cell.all)-len(revealed_cell_count)) == settings.MINES_COUNT:
            ctypes.windll.user32.MessageBoxW(0,'CONGRATULATIONS','THE BOMBS ARE DEFEATED',0)
            sys.exit()
            
                
    def show_mine(self): #interrupt the game and display loss screen
        self.cell_btn_object.configure(bg='black')
        ctypes.windll.user32.MessageBoxW(0, 'BOOM', 'Restart', 0)
        self.restartApp()
        #sys.exit()

    def restartApp(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)

    @property
    def surrounding_cells(self):
        surr_cells =[ #creates array of cells surrounding the selected cell
            self.get_cell_axis(self.x-1,self.y-1),
            self.get_cell_axis(self.x,self.y-1),
            self.get_cell_axis(self.x+1,self.y-1),
            self.get_cell_axis(self.x-1,self.y),
            self.get_cell_axis(self.x+1,self.y),
            self.get_cell_axis(self.x-1,self.y+1),
            self.get_cell_axis(self.x,self.y+1),
            self.get_cell_axis(self.x+1,self.y+1),
        ]
       
        #eliminate None values in list
        surr_cells = [cell for cell in surr_cells if cell is not None] 
        return surr_cells

    @property
    def surrounding_cells_mine_count(self):
        surr_mine_count=0        

        for cell in self.surrounding_cells:
            if cell.is_mine:
                surr_mine_count+=1
        return surr_mine_count
        
    def show_cell(self):
        print(self.get_cell_axis(self.x, self.y)) #! delete for final
        print(self.surrounding_cells) #! delete for final
        print(self.surrounding_cells_mine_count) #! delete for final
        self.cell_btn_object.configure(bg='white')
        #change btn object text to display count of surrounding mines
        if self.surrounding_cells_mine_count != 0:
            self.is_revealed=True
            self.cell_btn_object.configure(text=f'{self.surrounding_cells_mine_count}')
        
        #update cell count label
        revealed_cell_count = [cell for cell in Cell.all if cell.is_revealed]
        print(len(revealed_cell_count)) #! delete for final
        Cell.cell_count_label_object.configure(text=f'Cells Remaining: {len(Cell.all)-len(revealed_cell_count)}')

    def reveal_surround(self):
        for cell in self.surrounding_cells:
            cell.show_cell()
                  

    def safe_cascade(self): #recursive function to continually reveal adjacent safe spaces
        self.cell_btn_object.configure(bg='white')
        self.is_revealed=True
        self.reveal_surround()
        for cell in self.surrounding_cells:
            if (cell.surrounding_cells_mine_count == 0) and cell.is_revealed==False:
                cell.safe_cascade()
            else:
                cell.show_cell()
                   
    def get_cell_axis(self, x,y): #return cell based on xy values
        for cell in Cell.all:
            if cell.x ==x and cell.y == y:
                return cell

    def right_click_actions(self, event): #signify a known mine
        print(f'{self.__repr__} has been right clicked!')
        if self.is_revealed==False:
            if self.cell_btn_object.cget('bg') == 'red':
                    self.cell_btn_object.configure(bg='steel blue')
            else:
                    self.cell_btn_object.configure(bg='red')
        print(self.is_revealed) #! delete for final
        
    def middle_click_actions(self, event): #signify a potential mine
        print(f'{self.__repr__} has been middle clicked!')
        if self.is_revealed==False:
            if self.cell_btn_object.cget('bg') == 'yellow':
                    self.cell_btn_object.configure(bg='steel blue')
            else:
                    self.cell_btn_object.configure(bg='yellow')

    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(
            location,
            bg='black',
            fg='white',
            text=f'Cells Remaining: {settings.CELL_COUNT}',
            font=('',20)
        )
        Cell.cell_count_label_object = lbl



    @staticmethod
    def randomize_mines():
        mines = random.sample(
            Cell.all, settings.MINES_COUNT 
        ) 

        for picked_cell in mines:
            picked_cell.is_mine=True

        print(f'There are {len(mines)} mines: {mines}') #! delete for final


    
    