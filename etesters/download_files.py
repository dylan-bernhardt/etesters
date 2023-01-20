import etesters.create_eagle_files as eagle
import etesters.select_test_points as tp
import tkinter as tk
import os
from tkinter import filedialog

class files :
    def __init__(self, folder :tp.Production_folder) :
        self.folder = folder
        return
    def write_files(self, root: tk.Tk): 
        currdir = os.getcwd()
        zone_right = tk.Frame(root, bg='#2F4F4F')
        zone_right.pack(fill=tk.Y, side='right')
        path = filedialog.askdirectory(parent=zone_right, initialdir=currdir, title='Please select a directory')
        zone_right.destroy()
        eagle.create_brd_file(self.folder, path)
        eagle.create_sch_file(self.folder, path)
        self.folder.final_tp_names_bot_df.to_csv(path +"/"+ self.folder.pnp_bot, sep=",", mode="w", index=False, header= False)
        self.folder.final_tp_names_top_df.to_csv(path +"/"+ self.folder.pnp_top, sep=',', mode="w", index=False, header = False)
        
        return
        
