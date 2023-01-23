import etesters.create_eagle_files as eagle
import etesters.select_test_points as tp
import tkinter as tk
import os
from tkinter import filedialog
from typeguard import typechecked



class files :
    """
    4 files that can be written in a folder chosen by the user : 2 eagle files & 2 PnP files
    These files are necessary to build the electronic test bench

    ...
    
    Attributes
    ----------------
    folder : select_test_points.Production_folder
        object that corresponds to the gerber production folder

    Methods
    ----------------
    write_files(root : tkinter.Tk)
        Open a gui to choose a folder where to write and save the files
    """
    @typechecked
    def __init__(self, folder :tp.Production_folder)-> None :
        self.folder = folder
        return


    @typechecked
    def write_files(self, root: tk.Tk)-> None: 
        """
        Asking the user where to save the files on the root specified in parameters

        ...

        Parameters
        ---------------
        root : tkinter.Tk
            The root of the main gui
        """
        currdir = os.getcwd()
        zone_right = tk.Frame(root)
        zone_right.pack(fill=tk.Y, side='right')
        path = filedialog.askdirectory(parent=zone_right, initialdir=currdir, title='Please select a directory')
        zone_right.destroy()
        if path :
            eagle.create_brd_file(self.folder, path)
            eagle.create_sch_file(self.folder, path)
            self.folder.final_tp_names_bot_df.to_csv(path +"/"+ self.folder.pnp_bot, sep=",", mode="w", index=False, header= False)
            self.folder.final_tp_names_top_df.to_csv(path +"/"+ self.folder.pnp_top, sep=',', mode="w", index=False, header = False)
        return
        
