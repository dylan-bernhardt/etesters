import etesters.create_eagle_files as eagle
import etesters.select_test_points as tp
import tkinter as tk
import os
from tkinter import filedialog
from typeguard import typechecked
import etesters.pcb_dimension

@typechecked
def download_files(root: tk.Tk, folder: tp.Production_folder, dimension: etesters.pcb_dimension.pcb_dimension)-> str: 
    """
    Asking the user where to save the files on the root specified in parameters

    ...

    Parameters
    ---------------
    root : tkinter.Tk
        The root of the main gui
    folder : select_test_points.Production_folder
        The production folder
    dimension : pcb_dimension.pcb_dimension
        The object containig the size of the pcb that will be created

    Returns
    ---------------
    str 
        the path of the folder where the new files are stored
    """
    currdir = os.getcwd()
    zone_right = tk.Frame(root)
    zone_right.pack(fill=tk.Y, side='right')
    path = filedialog.askdirectory(parent=zone_right, initialdir=currdir, title='Please select a directory')
    zone_right.destroy()
    if path :
        eagle.create_brd_file(folder, dimension, path)
        eagle.create_sch_file(folder, path)
        folder.final_tp_names_bot_df.to_csv(path +"/"+ folder.pnp_bot, sep=",", mode="w", index=False, header= False)
        folder.final_tp_names_top_df.to_csv(path +"/"+ folder.pnp_top, sep=',', mode="w", index=False, header = False)
    return path
        
