import tkinter as tk
import os
from tkinter import filedialog
from typeguard import typechecked

import create_eagle_files as eagle
import select_test_points as tp
import draw_gerber as dg
import download_files as df



class App:

    @typechecked
    def __init__(self, title :str ='ETESTERS', bg: str = '#2F4F4F')-> None :
        self.title = title
        self.bg = bg
        self.compteur = 1
        self.folder = tp.Production_folder()
        self.validate = True
        return

    @typechecked
    def configure(self,title: str,bg: str)-> None:
        self.title = title
        self.bg = bg
        return

    @typechecked
    def display(self)-> None :
        self.root = tk.Tk()
        self.root.title(self.title)
        self.root.resizable(width= 0, height= 0)
        self.root.configure(background=self.bg)
        self.zone_left= tk.Frame(self.root, bg=self.bg) 


        self.btn1 = tk.Button(self.zone_left, width = 60, text="[1] Selectionner le dossier de production ", fg="white", bg=self.bg, command =self.fct_1)
        self.btn2 = tk.Button(self.zone_left, width = 60,  text="[2] Choisir les fichiers Pick & Place et les fichiers de légende", fg="white", bg=self.bg, command =self.fct_2, state=tk.DISABLED)
        self.btn3 = tk.Button(self.zone_left, width = 60, text="[3] Selectionner les noms des packages correspondant aux tests points", fg="white", bg=self.bg, command=self.fct_3, state=tk.DISABLED)
        self.btn4 = tk.Button(self.zone_left, width = 60, text="[4] Selectionner les points de test à garder pour la face bottom", fg="white", bg=self.bg, command = self.fct_4, state=tk.DISABLED)
        self.btn5 = tk.Button(self.zone_left, width = 60, text="[5] Selectionner les points de test à garder pour la face top", fg="white", bg=self.bg, command =self.fct_5, state=tk.DISABLED)
        self.btn6 = tk.Button(self.zone_left, width = 60, text="[6] Télécharger les nouveaux fichiers", fg="white", bg=self.bg, command = self.fct_6, state=tk.DISABLED)
        self.btnquitter = tk.Button(self.zone_left, width = 60, text="Quitter", fg="white", bg=self.bg, command=self.fct_quitter)
        
        self.zone_left.pack(fill=tk.Y, side='left')

        self.btn1.pack( padx=10,pady=10)
        self.btn2.pack( padx=10,pady=10)
        self.btn3.pack( padx=10,pady=10)
        self.btn4.pack( padx=10,pady=10)
        self.btn5.pack( padx=10,pady=10)
        self.btn6.pack( padx=10,pady=10)
        self.btnquitter.pack( padx=10,pady=10)

        self.root.mainloop()
        return

    @typechecked
    def fct_quitter(self)-> None:
        text = "Etes-vous sûr de vouloir quitter ?"
        if self.compteur != 9:
            text = "Vous n'avez pas terminé, êtes-vous sûr de vouloir quitter ? "
        quit = tk.messagebox.askquestion("Quitter",text)
        if quit=='yes':
            self.root.destroy()
        return 

    @typechecked
    def fct_1(self)-> None:
    
        if self.compteur == 1:
            currdir = os.getcwd()
            zone_right = tk.Frame(self.root, bg='#2F4F4F')
            zone_right.pack(fill=tk.Y, side='right')
            path = filedialog.askdirectory(parent=zone_right, initialdir=currdir, title='Please select a directory')
            self.folder.change_path(path)
            zone_right.destroy()
            self.compteur+=1
            print(self.folder.path)
        
        else :
            restart = tk.messagebox.askquestion("Restart","Etes-vous sûr de vouloir refaire cette étape ?")
            if restart=='yes':
                self.compteur=1
                self.fct_1()
                self.btn2.configure(state=tk.DISABLED)
                self.btn3.configure(state=tk.DISABLED)
                self.btn4.configure(state=tk.DISABLED)
                self.btn5.configure(state=tk.DISABLED)
                self.btn6.configure(state=tk.DISABLED)
   

        self.btn2.configure(state=tk.NORMAL)
        return 

    @typechecked
    def fct_2(self)-> None:

        if self.compteur==2:
            tp.gui_select_pnp_file(self.folder, self.root)
            self.compteur +=1

        else : 
            restart = tk.messagebox.askquestion("Restart","Etes-vous sûr de vouloir refaire cette étape ?")
            if restart=='yes':
                self.compteur =2
                self.fct_2()
                self.btn3.configure(state=tk.DISABLED)
                self.btn4.configure(state=tk.DISABLED)
                self.btn5.configure(state=tk.DISABLED)
                self.btn6.configure(state=tk.DISABLED)


    
        self.btn3.configure(state=tk.NORMAL)
        return

    @typechecked
    def fct_3(self)-> None:

        if self.compteur==3:
            tp.gui_select_tp(self.folder, self.root)
            self.compteur+=1
           
        else:
            restart = tk.messagebox.askquestion("Restart","Etes-vous sûr de vouloir refaire cette étape ?")
            if restart=='yes':
                self.compteur =3
                self.folder.tp_names_list_clear()
                self.fct_3()
                self.btn4.configure(state=tk.DISABLED)
                self.btn5.configure(state=tk.DISABLED)
                self.btn6.configure(state=tk.DISABLED)

           
        self.btn4.configure(state=tk.NORMAL)
        return

    @typechecked
    def fct_4(self)-> None:
    
        if self.compteur==4:
            image_bot = dg.GerberImage(self.folder, 'bottom')
            image_bot.center_0_0()
            image_bot.draw(self.root)
            self.compteur+=1
                
        else :
            restart = tk.messagebox.askquestion("Restart","Etes-vous sûr de vouloir refaire cette étape ?")
            if restart=='yes':
                self.compteur =4
                self.fct_4()
                self.btn5.configure(state=tk.DISABLED)
                self.btn6.configure(state=tk.DISABLED)


        self.btn5.configure(state=tk.NORMAL)
        return

    @typechecked
    def fct_5(self)-> None:   

        if self.compteur==5:
            image_top = dg.GerberImage(self.folder,'top')
            image_top.center_0_0()
            image_top.draw(self.root)
            self.compteur+=1
              
        else :
            restart = tk.messagebox.askquestion("Restart","Etes-vous sûr de vouloir refaire cette étape ?")
            if restart=='yes':
                self.compteur =5
                self.fct_5()
                self.btn6.configure(state=tk.DISABLED)

        
        self.btn6.configure(state=tk.NORMAL)
        return


    @typechecked
    def fct_6(self)-> None:
       

        if self.compteur==6:
            
            df.files(self.folder).write_files(self.root)
            tk.messagebox.showinfo('INFO', 'Les nouveaux fichiers ont bien été créés dans le dossier de production')

            self.compteur+=1

        else :
            restart = tk.messagebox.askquestion("Restart","Etes-vous sûr de vouloir refaire cette étape ?")
            if restart=='yes':
                self.compteur =6
                self.fct_6()

        return      



App().display()