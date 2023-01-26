from typeguard import typechecked
import pandas as pd
import etesters.select_test_points as tp
import tkinter as tk


@typechecked
def read_excellon(path: str)->list :
    f = open(path,'r')
    l = f.read().splitlines()
    f.close()
    return l

@typechecked
def extract_values(l :list):
    d = {'signal_name': [], 'x' : [], 'y': [], 'angle': [], 'value': [], 'package': []}
    dot = l[5].find("0.0")
    precision = len(l[5]) - dot - 2
    i=0
    for line in l :
        x=line.find('X')
        y=line.find('Y')
        if x!= -1 and y!=-1 :
            d['signal_name'].append("Excellon"+str(i))
            d['x'].append(int(line[x+1:y])/(10**int(precision)))
            d['y'].append(int(line[y+1:])/(10**int(precision)))
            d['angle'].append(0.0)
            d['value'].append("TESPOINT-SMD1.5MM")
            d["package"].append('TESTPOINT-1.5MM')
            i+=1
    df = pd.DataFrame().from_dict(d)
    return df




class gui_select_excellon_files:

    @typechecked
    def __init__(self, folder : tp.Production_folder) -> None:
        self.folder = folder
        return

    @typechecked
    def validate_fct(self)-> None:
        try:
            self.folder.enter_excellon_files(excellon_non_plated=self.list_box1.get(self.list_box1.curselection()))
        
        except :
            tk.messagebox.showwarning(title = 'ATTENTION', message = "Attention ! Tous les fichiers n'ont pas été sélectionné")
            pass

        self.frame.destroy()
        for btn in self.list_btn :
            btn.configure(state = tk.NORMAL) 

        return

    @typechecked
    def display(self, root: tk.Tk, list_btn: list)-> None :
        self.list_btn = list_btn 

        self.frame = tk.Frame(root, bg ='#436D6D')
        self.frame.pack(fill=tk.Y, side='right')

        self.list_box1,label1 = tp.create_files_listbox(self.frame, self.folder.path, '', 'Selectionner les fichiers Excellon non-Plated : ')

    
        label1.grid(row = 0, column=0, padx=10)
        self.list_box1.grid(row = 1, column=0)

        tk.Button(self.frame, text="Valider",fg="white", bg ='#436D6D', command=self.validate_fct).grid(row=2, column =0, pady=15, padx=50)

        return





