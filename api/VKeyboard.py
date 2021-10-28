# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 16:42:35 2020

@author: hutton
"""

import tkinter as tk


class VKeyboard(tk.Frame):
    def __init__(self, master, entry):
        tk.Frame.__init__(self, master)
        tk.Frame.configure(self,bg='white')

        self.entry = entry
        self.entry.pack(pady = 20)
        self.create()

    def select(self, entry, value):
        #pyautogui.press(event)
        global uppercase
        uppercase = False
    
        if value == "Space":
            value = ' '
        elif value == 'Enter':
            value = '\n'
        elif value == 'Tab':
            value = '\t'
    
        if value == "←":
            if isinstance(entry, tk.Entry):
                entry.delete(len(entry.get())-1, 'end')
            #elif isinstance(entry, tk.Text):
            else: # tk.Text
                entry.delete('end - 2c', 'end')
        elif value in ('Caps Lock', 'Shift'):
            uppercase = not uppercase # change True to False, or False to True
        elif value =='英':
            self.kb_num.grid_forget()
            self.kb_en.grid()
        elif value =='數':
            self.kb_en.grid_forget()
            self.kb_num.grid()
        else:
            if uppercase:
                value = value.upper()
            entry.insert('end', value)
        return
    def create(self):
        alphabets_num = [
        ['+','1','2','3'],
        ['*','4','5','6'],
        ['/','7','8','9'],
        ['英','-','0','←']
        ]    
        alphabets_en = [
        ['A','B','C','D'],
        ['E','F','G','H'],
        ['I','J','K','L'],
        ['M','N','O','P'],
        ['Q','R','S','T'],
        ['U','V','W','X'],
        ['數','Y','Z','←']
        ] 
        self.kb_num = tk.Frame(self)
        self.kb_en = tk.Frame(self)
        for y, row in enumerate(alphabets_num):
    
            x = 0
    
            #for x, text in enumerate(row):
            for text in row:
    
                width = 5
                columnspan = 1
    
                tk.Button(self.kb_num, text=text, width=width, 
                          command=lambda value=text: self.select(self.entry, value),
                          padx=3, pady=3, bd=12, bg="black", fg="white", takefocus = False
                         ).grid(row=y, column=x, columnspan=columnspan)
    
                x+= columnspan    
                
        for y, row in enumerate(alphabets_en):
    
            x = 0
    
            #for x, text in enumerate(row):
            for text in row:
    
                width = 5 
                columnspan = 1
    
                tk.Button(self.kb_en, text=text, width=width, 
                          command=lambda value=text: self.select(self.entry, value),
                          padx=3, pady=3, bd=12, bg="black", fg="white", takefocus = False
                         ).grid(row=y, column=x, columnspan=columnspan)
    
                x+= columnspan    
        self.kb_num.grid()