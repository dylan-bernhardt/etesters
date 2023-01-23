import tkinter as tk
import os
from tkinter import filedialog
from typeguard import typechecked
import etesters.create_eagle_files as eagle
import etesters.select_test_points as tp
import etesters.draw_gerber as dg
import etesters.download_files as df
import etesters.pcb_dimension



class App:

    @typechecked
    def __init__(self, title :str ='ETESTERS', bg: str = '#2F4F4F')-> None :
        self.title = title
        self.bg = bg
        self._compteur = 1
        self.folder = tp.Production_folder()
        return


    @typechecked
    def configure(self,title: str ='ETESTERS',bg: str ='#2F4F4F')-> None:
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
        self.btn6 = tk.Button(self.zone_left, width = 60, text="[6] Entrer les dimensions du pcb de test", fg="white", bg=self.bg, command = self.fct_6, state=tk.DISABLED)
        self.btn7 = tk.Button(self.zone_left, width = 60, text="[7] Télécharger les nouveaux fichiers", fg="white", bg=self.bg, command = self.fct_7, state=tk.DISABLED)
        self.btnquitter = tk.Button(self.zone_left, width = 60, text="Quitter", fg="white", bg=self.bg, command=self.fct_quitter)
        
        self.zone_left.pack(fill=tk.Y, side='left')

        self.btn1.pack(padx=10,pady=10)
        self.btn2.pack(padx=10,pady=10)
        self.btn3.pack(padx=10,pady=10)
        self.btn4.pack(padx=10,pady=10)
        self.btn5.pack(padx=10,pady=10)
        self.btn6.pack(padx=10,pady=10)
        self.btn7.pack(padx=10,pady=10)
        self.btnquitter.pack( padx=10,pady=10)

        self.list_btn = [self.btn1, self.btn2, self.btn3, self.btn4, self.btn5, self.btn6, self.btn7]

        self.root.mainloop()
        return


    @typechecked
    def fct_quitter(self)-> None:
        text = "Etes-vous sûr de vouloir quitter ?"
        if self._compteur != 7:
            text = "Vous n'avez pas terminé, êtes-vous sûr de vouloir quitter ? "
        else : 
            pass
        quit = tk.messagebox.askquestion("Quitter",text)
        
        if quit=='yes':
            self.root.destroy()
            try :
                for i in os.listdir(self.folder.path+"/filtered_pnp"):
                    os.remove(self.folder.path+"/filtered_pnp/%s" % i)
                os.rmdir(self.folder.path+"/filtered_pnp")
            except (FileNotFoundError, AttributeError) :
                pass
        else: 
            pass
        return 

 
    @typechecked
    def fct_1(self)-> None:
        self.enable_btn(0)
        if self._compteur == 1:
            self.folder.reset_path()
            currdir = os.getcwd()
            zone_right = tk.Frame(self.root)
            zone_right.pack(fill=tk.Y, side='right')

            path = filedialog.askdirectory(parent=zone_right, initialdir=currdir, title='Please select a directory')
            try :
                self.folder.change_path(path)
            except TypeError :
                pass
            zone_right.destroy()
            if self.folder.path :
                self._compteur+=1
            self.enable_btn(self._compteur)
                        
        else :
            restart = tk.messagebox.askquestion("Restart","Etes-vous sûr de vouloir refaire cette étape ?")
            if restart=='yes':
                self._compteur=1
                self.fct_1()
                
            else :
                pass
        
        return 


    @typechecked
    def fct_2(self)-> None:
        self.enable_btn(0)
        if self._compteur==2:
            self._compteur +=1
            tp.gui_select_pnp_file(self.folder, self.root, self.list_btn[:self._compteur])

        else : 
            restart = tk.messagebox.askquestion("Restart","Etes-vous sûr de vouloir refaire cette étape ?")
            if restart=='yes':
                self._compteur =2
                self.fct_2()
            else:
                pass

        return


    @typechecked
    def fct_3(self)-> None:
        self.enable_btn(0)
        if self._compteur==3:
            self._compteur+=1
            self.folder.tp_names_list_clear()
            tp.gui_select_tp(self.folder, self.root, self.list_btn[:self._compteur])
           
        else:
            restart = tk.messagebox.askquestion("Restart","Etes-vous sûr de vouloir refaire cette étape ?")
            if restart=='yes':
                self._compteur =3
                self.fct_3()
                for i in os.listdir(self.folder.path+"/filtered_pnp"):
                    os.remove(self.folder.path+"/filtered_pnp/%s" % i)
                os.rmdir(self.folder.path+"/filtered_pnp")
            else : 
                pass

        return


    @typechecked
    def fct_4(self)-> None:
        self.enable_btn(0)
        if self._compteur==4:
            self._compteur+=1
            image_bot = dg.GerberImage(self.folder, 'bottom')
            self.center = tk.messagebox.askquestion("Center?","Voulez-vous déplacer le centre du repère au centre de la carte? (Fortement conseillé, peu potentiellement buggué si non.) ")
            if self.center =='yes':
                image_bot.center_0_0()
            else :
                pass
            image_bot.draw(self.root, self.list_btn[:self._compteur])
                
        else :
            restart = tk.messagebox.askquestion("Restart","Etes-vous sûr de vouloir refaire cette étape ?")
            if restart=='yes':
                self._compteur =4
                self.fct_4()
            else : 
                pass
        return


    @typechecked
    def fct_5(self)-> None:   
        self.enable_btn(0)
        if self._compteur==5:
            self._compteur+=1
            image_top = dg.GerberImage(self.folder,'top')
            if self.center == 'yes':
                image_top.center_0_0()
            else : 
                pass
            image_top.draw(self.root, self.list_btn[:self._compteur])
              
        else :
            restart = tk.messagebox.askquestion("Restart","Etes-vous sûr de vouloir refaire cette étape ?")
            if restart=='yes':
                self._compteur =5
                self.fct_5()
            else : 
                pass

        return

    @typechecked
    def fct_6(self) -> None :
        self.enable_btn(0)
        if self._compteur==6 : 
            self._compteur+=1
            etesters.pcb_dimension.dimension_gui(self.folder, self.center).display(self.root, self.list_btn[:self._compteur])
        
        else : 
            restart = tk.messagebox.askquestion("Restart","Etes-vous sûr de vouloir refaire cette étape ?")
            if restart=='yes':
                self._compteur =6
                self.fct_6()
            else : 
                pass

        return 


    @typechecked
    def fct_7(self)-> None:
        self.enable_btn(0)

        if self._compteur==7:
            
            self._compteur+=1
            df.files(self.folder).write_files(self.root)
            tk.messagebox.showinfo('INFO', 'Les nouveaux fichiers ont bien été créés dans le dossier de production')
            self.enable_btn(self._compteur)

        else :
            restart = tk.messagebox.askquestion("Restart","Etes-vous sûr de vouloir refaire cette étape ?")
            if restart=='yes':
                self._compteur =7
                self.fct_7()
            else : 
                pass

        return      


    @typechecked
    def enable_btn(self, compteur : int)-> None:
        for i in range(len(self.list_btn)) :
            if i < compteur :
                self.list_btn[i].configure(state = tk.NORMAL)
            else :
                self.list_btn[i].configure(state = tk.DISABLED)

        return
