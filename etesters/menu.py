import tkinter as tk
import os
from tkinter import filedialog
from typeguard import typechecked
import pandas as pd
import etesters.create_eagle_files as eagle
import etesters.select_test_points as tp
import etesters.draw_gerber as dg
import etesters.download_files as df
import etesters.pcb_dimension
import etesters.excellon_files as exc



class App:
    """
    Gui to configure & export the files that will be used in order to build the electronic test bench


    Attributes
    --------------------
    title: str
        The title of the gui
    bg : str
        The color of the background
    folder : select_test_points.Production_folder
        Corresponds to the folder containing all the production files
    root : tkinter.Tk
        The root of the gui
    zone_left : tkinter.Frame
        A zone on the left of the screen containing buttons
    btn1-7 : tkinter.Button 
        Button
    center : str
        "yes" if the origin matches with the center of the pcb
        else "no"
    list_btn: list
        The list containing every buttons. Useful if you want to disable consecutive buttons.


    Methods
    --------------------
    configure(title :str, bg: str)
        Configures the gui appearance
    display()
        Displays the gui
    fct_quitter()
        Action done when exit button is pressed
    enable_btn(compteur)
        Enables the first "compteur" buttons and disables the others
    fct_1()
        Function triggered when the 1st button is pressed
    fct_2()
        Function triggered when the 2nd button is pressed
    fct_3()
        Function triggered when the 3rd button is pressed
    fct_4()
        Function triggered when the 4th button is pressed
    fct_5()
        Function triggered when the 5th button is pressed
    fct_6()
        Function triggered when the 6th button is pressed
    fct_7()
        Function triggered when the 7th button is pressed
    fct_8()
        Function triggered when the 8th button is pressed
    fct_9()
        Function triggered when the 9th button is pressed
    """
    @typechecked
    def __init__(self, title :str ='ETESTERS', bg: str = '#2F4F4F')-> None :
        """
        Init useful attributes for the gui as title, bg or _compteur.
        _compteur prevents the user to do the steps in the wrong order.

        Parameters
        ----------------
        title : str, default = 'ETESTERS'
            the title of the gui
        bg : str, default = "#2F4F4F"
            the bg color

        """

        self.title = title
        self.bg = bg
        self._compteur = 1
        self.folder = tp.Production_folder()
        return


    @typechecked
    def configure(self,title: str ='ETESTERS',bg: str ='#2F4F4F')-> None:
        """
        Configures the appearance settings

        Parameters
        -------------
        title : str, default = 'ETESTERS'
            title of the gui
        bg: str, default = '#2F4F4F'
            background color

        Returns
        --------------
        """
        self.title = title
        self.bg = bg
        return


    @typechecked
    def display(self)-> None :
        """
        Displays the gui 
        """
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
        self.btn7 = tk.Button(self.zone_left, width = 60, text="[7] Sélectionner le fichier excellon", fg="white", bg=self.bg, command = self.fct_7, state=tk.DISABLED)
        self.btn8 = tk.Button(self.zone_left, width = 60, text="[8] Sélectionner les points d'intérêt à garder", fg="white", bg=self.bg, command = self.fct_8, state=tk.DISABLED)
        self.btn9 = tk.Button(self.zone_left, width = 60, text="Télécharger les nouveaux fichiers", fg="white", bg=self.bg, command = self.fct_9, state=tk.DISABLED)
        self.btnquitter = tk.Button(self.zone_left, width = 60, text="Quitter", fg="white", bg=self.bg, command=self.fct_quitter)
        
        self.zone_left.pack(fill=tk.Y, side='left')

        self.btn1.pack(padx=10,pady=10)
        self.btn2.pack(padx=10,pady=10)
        self.btn3.pack(padx=10,pady=10)
        self.btn4.pack(padx=10,pady=10)
        self.btn5.pack(padx=10,pady=10)
        self.btn6.pack(padx=10,pady=10)
        self.btn7.pack(padx=10,pady=10)
        self.btn8.pack(padx=10,pady=10)
        self.btn9.pack(padx=10,pady=10)
        self.btnquitter.pack( padx=10,pady=10)

        self.list_btn = [self.btn1, self.btn2, self.btn3, self.btn4, self.btn5, self.btn6, self.btn7, self.btn8]

        self.root.mainloop()
        return


    @typechecked
    def fct_quitter(self)-> None:
        """
        Asks to close the gui if the user wants to leave
        Open the folder where the new files are stored, if it exists

        """

        text = "Etes-vous sûr de vouloir quitter ?"
        if self._compteur != 9:
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
            try :
               os.system("open %s" % self.new_path)
            except AttributeError :
                pass
             
     
        return 

 
    @typechecked
    def fct_1(self)-> None:
        """
        Function triggered when the first button is pressed. A gui is opened. The user has to select the folder which contains the production files.
        The action can be remade as many times as wanted.
        If the users closes the gui without selecting a folder, he cannot do the next action.
        """
        if self._compteur == 1:
            self.enable_btn(0)
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
        """
        Function triggered when button 2 is pressed. It allows the user to select the two PnP files & the two legend files in the folder he selected at previous step.
        The step can be remade as many times as wanted.
        """
        if self._compteur==2:
            self.enable_btn(0)
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
        """
        Function triggered when the 3rd button is pressed. 
        The user has to select the names of the testpoints he wants to keep on the test bench.        
        """
        if self._compteur==3:
            self.enable_btn(0)
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
        """
        Function triggered when the 4th button is pressed.
        It opens an drawing of the bottom side of the card. The user has to recolor in 'red' the testpoints that he wants to forget for the bench.
        A gui is firstly openned and asks if the origin should match the center of the card.
        The step can be remade as many times as wanted.

        """
        if self._compteur==4:
            self.folder.final_tp_names_bot_df=pd.DataFrame(None)
            self.enable_btn(0)
            self._compteur+=1
            d = dg.rearrange_useful_values(dg.read_gerber(self.folder.legend_bot, self.folder.path))
            tp_df= pd.read_csv(self.folder.path+'/filtered_pnp/'+'FILTERED__'+self.folder.pnp_bot, delimiter=',')
            image_bot = dg.GerberImage(self.folder, 'bottom', tp_df, d)
            self.center = tk.messagebox.askquestion("Center?","Voulez-vous déplacer le centre du repère au centre de la carte?")
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
        """
        Function triggered when the 5th button is pressed.
        It opens an drawing of the top side of the card. The user has to recolor in 'red' the testpoints that he wants to forget for the bench.
        The step can be remade as many times as wanted.
      
        """
        if self._compteur==5:
            self.folder.final_tp_names_top_df=pd.DataFrame(None)
            self.enable_btn(0)
            self._compteur+=1
            d = dg.rearrange_useful_values(dg.read_gerber(self.folder.legend_top, self.folder.path))
            tp_df= pd.read_csv(self.folder.path+'/filtered_pnp/'+'FILTERED__'+self.folder.pnp_top, delimiter=',')
            image_top = dg.GerberImage(self.folder,'top', tp_df, d)
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
        """
        Function triggered when the 6th button is pressed.
        The user has to enter the size of the future pcb containing the test points.
        The step can be remade as many times as wanted.
        """
        if self._compteur==6 : 
            self._tmp = self.folder.final_tp_names_top_df.copy()
            self.enable_btn(0)
            self._compteur+=1
            self.dimension = etesters.pcb_dimension.pcb_dimension(self.folder, self.center)
            self.dimension.display(self.root, self.list_btn[:self._compteur]+[self.btn9])
        
        else : 
            restart = tk.messagebox.askquestion("Restart","Etes-vous sûr de vouloir refaire cette étape ?")
            if restart=='yes':
                self._compteur =6
                self.fct_6()
            else : 
                pass

        return 




    def fct_7(self)-> None :
        """
        Function triggered when the 7th button is pressed
        The user has to choose the name of the excellon file
        """
        if self._compteur==7:
            
            self.enable_btn(0)
            self._compteur+=1
            exc.gui_select_excellon_files(self.folder).display(self.root, self.list_btn[:self._compteur])
                       

        else :
            restart = tk.messagebox.askquestion("Restart","Etes-vous sûr de vouloir refaire cette étape ?")
            if restart=='yes':
                self._compteur =7
                self.fct_7()
            else : 
                pass

        return  


    def fct_8(self)-> None :
        """
        Function triggered when the 8 button is pressed
        It opens a drawing of the card
        The user has to recolor in red the hole he doesn't want to keep for the test bench
        """
        
        if self._compteur==8:
            self.folder.final_tp_names_top_df = self._tmp.copy()
            self.enable_btn(0)
            self._compteur+=1
            
            d= dg.rearrange_useful_values(dg.read_gerber(self.folder.legend_top, self.folder.path))
            df = exc.extract_values(exc.read_excellon(self.folder.path+"/"+self.folder.excellon_non_plated))
            image_non_plated = dg.GerberImage(self.folder, 'top', df, d)
            if self.center =='yes':
                image_non_plated.center_0_0()

            image_non_plated.draw(self.root, self.list_btn[:self._compteur])
                                    

        else :
            restart = tk.messagebox.askquestion("Restart","Etes-vous sûr de vouloir refaire cette étape ?")
            if restart=='yes':
                self._compteur =8
                self.fct_8()

            else : 
                pass

        return

    @typechecked
    def fct_9(self)-> None:
        """
        Function triggered when the 9th button is pressed.
        A gui is openned and the user has to choose the repertory where the files will be saved.
        The step can be remade as many times as wanted.
        """
        try :
            self.new_path=df.download_files(self.root, self.folder, self.dimension)
            tk.messagebox.showinfo('INFO', 'Les nouveaux fichiers ont bien été créés dans le dossier %s' % self.new_path)
            self.enable_btn(self._compteur)
        except TypeError:
            pass
        return    

    @typechecked
    def enable_btn(self, compteur : int)-> None:
        """
        Enable and disable consecutive buttons. 

        Parameters
        ------------------
        compteur : int
            The number of button the user wants to enable.
            For example, if compteur = 3, buttons 1, 2 & 3 will be enabled. Others will be disabled.
        """
        for i in range(len(self.list_btn)) :
            if i < compteur :
                self.list_btn[i].configure(state = tk.NORMAL)
            else :
                self.list_btn[i].configure(state = tk.DISABLED)

        return
