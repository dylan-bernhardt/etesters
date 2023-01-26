from typeguard import typechecked
import pandas as pd
import etesters.select_test_points as tp
import tkinter as tk


@typechecked
def read_excellon(path: str)->list :
    """
    read the excellon file and stores its lines in a list

    Parameters
    --------------------------
    path : str
        the path of the file that will be read
    """
    f = open(path,'r')
    l = f.read().splitlines()
    f.close()
    return l

@typechecked
def extract_values(l :list)-> pd.DataFrame:
    """
    extracts and sorts the values from the list in a dataframe

    Parameters
    ------------------
    l: list
        the list that contains the lines of the file

    Returns
    --------------
    pd.DataFrame
        the sorted dataframe
    """

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
    """
    A gui for the user so he can choose the correct file name

    Attributes
    ---------------------
    folder: tp.Production_folder
        the object that contains the production folder and every information about it

    Methods
    --------------------
    __init__(folder):
        initializes the class
    validate_fct():
        the function triggered when the validate button is pressed
    display(root, list_btn)
        diplays the guy
    """
    @typechecked
    def __init__(self, folder : tp.Production_folder) -> None:
        """
        initializes the class

        Parameters
        -------------------------
        folder : Production_folder
            the object that ocntaisn the production folder and every information about it
        """
        self.folder = folder
        return

    @typechecked
    def validate_fct(self)-> None:
        """
        the function triggered when the validate button is pressed
        """
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
        """
        displays the gui

        Parameters
        ------------------
        root: Tk
            the root where the gui will be added
        list_btn: list
            the list of the menu buttons that will need to be enabled after the step
        """
        self.list_btn = list_btn 

        self.frame = tk.Frame(root, bg ='#436D6D')
        self.frame.pack(fill=tk.Y, side='right')

        self.list_box1,label1 = tp.create_files_listbox(self.frame, self.folder.path, '', 'Selectionner les fichiers Excellon non-Plated : ')

    
        label1.grid(row = 0, column=0, padx=10)
        self.list_box1.grid(row = 1, column=0)

        tk.Button(self.frame, text="Valider",fg="white", bg ='#436D6D', command=self.validate_fct).grid(row=2, column =0, pady=15, padx=50)

        return





