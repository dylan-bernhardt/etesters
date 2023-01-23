import tkinter as tk
import etesters.select_test_points as tp

class dimension_gui :

    def __init__(self,folder: tp.Production_folder, center: str)-> None :
        self.center= center
        self.folder = folder
        return 


    def validate_fct(self)-> None:
    
        longueur = float(self.s1.get())
        largeur = float(self.s2.get())
        if self.center == "yes":
            self.folder.set_pcb_test_dimension(-(longueur)/2,longueur/2,-(largeur)/2, largeur/2)
        else : 
            self.folder.set_pcb_test_dimension(0,longueur,0, largeur)

        

        
            
        for btn in self.list_btn :
            btn.configure(state = tk.NORMAL)
        self.frame.destroy()
        
        return  

    def display(self, root: tk.Tk , list_btn :list ) -> None :
        
        self.list_btn =  list_btn
        self.frame = tk.Frame(root, bg ='#436D6D')
        self.frame.pack(fill=tk.Y, side='right')
        tk.Label(self.frame, text= 'Longueur').grid(row=0, column= 0, pady =10, padx=10)
        tk.Label(self.frame, text= 'Largeur').grid(row=0, column= 1, pady =10, padx=10)
        self.s1 = tk.Spinbox(self.frame, from_=abs(self.folder.xmin) + abs(self.folder.xmax), to=(abs(self.folder.xmin) + abs(self.folder.xmax))*10)
        self.s2 = tk.Spinbox(self.frame, from_=abs(self.folder.ymin) + abs(self.folder.ymax),  to=(abs(self.folder.xmin) + abs(self.folder.xmax))*10)
        self.s1.grid(row = 1, column = 0, pady =10, padx=10)
        self.s2.grid(row= 1, column = 1, pady =10, padx=10)


        tk.Button(self.frame, text="Valider",fg="white", bg ='#436D6D', command=self.validate_fct).grid(row=2, column =1, pady=15, padx=50)

        
        return
    