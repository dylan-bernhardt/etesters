import pandas as pd
from typeguard import typechecked
import tkinter as tk
import os
import etesters.menu as menu



class Production_folder :
    """
    Represents and contains the production folder and its characteristics
    Contains also the choices done by the user

    Attributes
    ---------------
    path : str
        The path of the folder
    pnp_bot : str
        name of the pnp bot file
    pnp_top : str
        name of the pnp top file
    legend_top : str
        name of the legend top file
    legend_bot : str
        name of the legend bottom file
    excellon_non_plated :
        name of the excellon non plated file
    tp_names_top : str
        list that contains the names of the testpoints for the top side
    tp_names_bot : str
        list that contains the names of the testpoints for the bottom side    
    final_tp_names_top_df : pandas.Dataframe
        dataframe that contains the characteristics for the testpoints on the top side that the user chose
    final_tp_names_bot_df : pandas.Dataframe
        dataframe that contains the characteristics for the testpoints on the bottom side that the user chose
    xmin: float
        define the dimension of the pcb
    xmax : float
        define the dimension of the pcb
    ymin: float
        define the dimension of the pcb
    ymax : float
        define the dimension of the pcb
    
    
    Methods
    ---------------
    __init__():
        Initializes 2 lists which will contain the names of the testpoints
    change_path(path):
        Changes the folder path
    reset_path() : 
        Resets the path
    enter_files(pnp_bot, pnp_top, legend_top, legend_bot):
        Sets the name of the different files
    enter_tp_names(name, side):
        Adds one name to the list tp_names_bot/top, depending on the side
    tp_names_list_clear():
        Resets the two list in order to rechoose the names
    enter_final_tp_names(self, df, side):
        Sets the user choice in a dataframe. 
    set_pcb_dimension(xmin, xmax, ymin, ymax):
        set the size of the pcb describes in the production folder
    """
    

    @typechecked
    def __init__(self)-> None:
        """
        Initializes useful values

        """
        self.tp_names_top=[]
        self.tp_names_bot=[]
        return 


    @typechecked
    def change_path(self, path : str)-> None:
        """
        Changes the current path 

        Parameters
        ---------------
        path : str
            the new path

        """
        self.path = path
        return

    @typechecked
    def reset_path(self)-> None:
        """
        Reset the current path
        """
        self.path = ""
        return

    @typechecked
    def enter_pnp_and_legend_files(self, pnp_bot: str, pnp_top: str, legend_top: str, legend_bot: str)-> None:
        """
        Sets the 4 file names

        Parameters
        ---------------
        pnp_bot : str
            name of the file
        pnp_top: str
            name of the file
        legend_top : str
            name of the file
        legend bot : str
            name of the file
        """
        self.pnp_bot=pnp_bot
        self.pnp_top=pnp_top
        self.legend_top = legend_top
        self.legend_bot=legend_bot
        return 

    @typechecked
    def enter_excellon_files(self, excellon_non_plated: str)-> None :
        """
        Sets the name of the excellon file

        Parameters
        ----------------------
        excellon-non-plated : str
            the name of the file
        """
        
        self.excellon_non_plated =excellon_non_plated
        return


    @typechecked
    def enter_tp_names(self, name : str, side : str)-> None:
        """
        Add one name in the corresponding list

        Parameters
        ---------------
        name : str
            The name of the testpoint that the user chose
        side : str
            The side where the user users chose the testpoints

        """
        if side =='top':
            self.tp_names_top.append(name)
        elif side == 'bottom':
            self.tp_names_bot.append(name)
        else :
            pass
        return


    @typechecked
    def tp_names_list_clear(self)-> None:
        """
        Clears the list that contains the names of the testpoints
        It is useful when the user needs to choose again the names when a mistake has been done

        """
        self.tp_names_top.clear()
        self.tp_names_bot.clear()
        return 


    @typechecked
    def enter_final_tp_names(self, df: pd.DataFrame, side :str)-> None:
        """
        Sets a dataframe in the class depending of the side
        It adds the elements of the dataframe in parameters to the dataframe which already exists

        Parameters
        ---------------
        df : pandas.DataFrame
            The dataframe which is filtered by the user choices
        side : str
            The side of the card where the made his choices

        """ 
        if side=='top':
            self.final_tp_names_top_df=pd.concat([self.final_tp_names_top_df, df], ignore_index=True)
            
        elif side=='bottom':
            self.final_tp_names_bot_df=pd.concat([self.final_tp_names_bot_df, df], ignore_index=True)

        
        return



    @typechecked
    def set_pcb_dimension(self, xmin: float, xmax: float, ymin: float, ymax: float)-> None:
        """
        Sets the dimension of the pcb describes in the production folder

        Parameters
        ---------------
        xmin : float
            minimum x value
        xmax: float
            maximum x value
        ymin: float
            minimum y value
        ymax: float
            minimum y value

        """
        self.xmax = xmax
        self.xmin = xmin
        self.ymin = ymin
        self.ymax = ymax
        return



@typechecked
def filter_test_points(pd: pd.DataFrame, list_tp: list, column_name: str = 'package') -> pd.DataFrame:
    """
    Filtered a dataframe from a list of name.

    Parameters
    ---------------
    pd : pandas.DataFrame 
        The dataframe that needs to be filtered
    list_tp : list
        List of the testpoints names
    column_name : str
        Default = 'package'
        The column the users wants to filter
    
    Returns
    ---------------
    pandas.DataFrame
        The filtered dataframe.

    """
    
    filtered_df = pd[pd[column_name].apply(lambda s: s.strip()).isin(list_tp)]
    return filtered_df


@typechecked
def filter_test_points_file(file_name: str, list_tp: list, folder_path: str, column_name: str = 'package') -> pd.DataFrame:
    """
    Filters a csv file with test points

    Parameters
    ---------------
    file_name : str
        file to filtered
    list_tp : list
        list of tp names
    folder_path : str
        path of the file
    column_name : str
        Default = 'package'
        column the user wants to filtered

    Returns
    ---------------
    pandas.DataFrame 
        The filtered dataframe

    """
    df = pd.read_csv(folder_path+'/'+file_name, delimiter=',', names=['signal_name', 'x', 'y', 'angle', 'value', column_name])
    filtered_df = filter_test_points(df, list_tp, column_name)
    return filtered_df


@typechecked
def create_filtered_test_points_file(file_name: str, list_tp: list, folder_path: str, column_name: str = 'package') -> None:
    """
    Create a new csv file with the filtered test points of a csv file

    Parameters
    ---------------
    file_name: str
        name of the csv file to filter
    list_tp : list
        list of the tp names
    folder_path :
        the file path
    column_name: str
        the column to filter

    """
    filtered_name= 'FILTERED__'+file_name
    filtered_df = filter_test_points_file(file_name, list_tp, folder_path, column_name)


    isExist = os.path.exists(folder_path+'/filtered_pnp')
    if not isExist:
        os.makedirs(folder_path+"/filtered_pnp")
    filtered_df.to_csv(folder_path+'/filtered_pnp/'+filtered_name, sep=",", mode="w", index=False)
    return


@typechecked
def gui_select_tp(folder: Production_folder, root: tk.Tk, list_btn: list , column_name: str = 'package') -> None:
    """
    A gui for the user to select the tp names

    Parameters
    ---------------
    folder : Production_folder
        the object that represents the production folder
    root : tkinter.Tk
        the root where the gui will be added
    list_btn : list
        list of the menu buttons that need to be enabled at the end of the step
    column_name : str
        column to filter


    """
    #@typechecked
    def select_all_checkbutton1(*args)-> None:
        """
        Function that selects all the tp names of the first side
        """
        for i in range(len(btn1)):
            if select_all1.get()==1:
                btn1[i].select()
            else:
                btn1[i].deselect()
        return

    #@typechecked
    def select_all_checkbutton2(*args)-> None:
        """
        Function that selects all the tp names of the second side

        """
        for i in range(len(btn2)):
            if select_all2.get()==1:
                btn2[i].select()
            else:
                btn2[i].deselect()
            return


    @typechecked
    def exit1()-> None:
        """
        Function triggered when the validate button from the first side is triggered
        A new file is created with the tp chosen
        When both has been activated, the menu buttons are enabled again


        """
        for i in range(len(enable1)):
            if enable1[i].get()==1:
                folder.enter_tp_names(l1[i].strip(),'bottom')
        if "filtered_pnp" in os.listdir(folder.path) :
            for btn in list_btn :
                btn.configure(state = tk.NORMAL)
        create_filtered_test_points_file(folder.pnp_bot, folder.tp_names_bot, folder.path)
        frame1.destroy()
        return


    @typechecked
    def exit2()-> None:
        """
        Function triggered when the validate button from the second side is triggered
        A new file is created with the tp chosen
        When both has been activated, the menu buttons are enabled again

        """
        for i in range(len(enable2)):
            if enable2[i].get()==1:
                folder.enter_tp_names(l2[i].strip(),'top')
        if "filtered_pnp" in os.listdir(folder.path) :
            for btn in list_btn :
                btn.configure(state = tk.NORMAL)
        create_filtered_test_points_file(folder.pnp_top, folder.tp_names_top, folder.path)
        frame2.destroy()
        return


    
    frame1 = tk.LabelFrame(root, text= 'Selectionner les noms des tp')
    frame1.pack(fill=tk.Y, side='right', padx=10, pady=10)


    frame2 = tk.LabelFrame(root, text= 'Selectionner les noms des tp')
    frame2.pack(fill=tk.Y, side='right', padx=10, pady=10)
    

    df1 = pd.read_csv(folder.path+'/'+folder.pnp_bot, delimiter=',', names=['signal_name', 'x', 'y', 'angle', 'value', column_name])
    l1 = df1.drop_duplicates(subset = [column_name])[column_name]
    l1=l1.reset_index()[column_name]

    enable1=[0 for i in range(len(l1))]
    btn1=[0 for i in range(len(l1))]
    for i in range(len(l1)) :
        enable1[i] = tk.IntVar()
        btn1[i] = tk.Checkbutton(frame1, text=l1[i],variable=enable1[i], onvalue=1, offvalue=0)
        btn1[i].pack(anchor=tk.W, padx=5)

    select_all1= tk.IntVar()
    select_all1.trace("w", select_all_checkbutton1)
    tk.Checkbutton(frame1 ,text = "Select all",variable=select_all1, onvalue=1, offvalue=0).pack(pady=10, padx=5, anchor = tk.W)


    df2 = pd.read_csv(folder.path+'/'+folder.pnp_top, delimiter=',', names=['signal_name', 'x', 'y', 'angle', 'value', column_name])
    l2 = df2.drop_duplicates(subset = [column_name])[column_name]
    l2=l2.reset_index()[column_name]

    enable2=[0 for i in range(len(l2))]
    btn2=[0 for i in range(len(l2))]
    for i in range(len(l2)) :
        enable2[i] = tk.IntVar()
        btn2[i] = tk.Checkbutton(frame2, text=l2[i],variable=enable2[i], onvalue=1, offvalue=0)
        btn2[i].pack(anchor=tk.W, padx=5, )


    select_all2= tk.IntVar()
    select_all2.trace("w", select_all_checkbutton2)
    tk.Checkbutton(frame2 ,text = "Select all",variable=select_all2, onvalue=1, offvalue=0).pack(pady=10, padx=5, anchor = tk.W)

    tk.Button(frame1, text= 'Valider', command = exit1, fg="white", bg ='#2F4F4F').pack(padx=20,pady=20, anchor=tk.S)
    tk.Button(frame2, text= 'Valider', command = exit2, fg="white", bg ='#2F4F4F').pack(padx=20,pady=20, anchor=tk.S)
    return


@typechecked
def gui_select_pnp_file(folder: Production_folder, root: tk.Tk, list_btn: list)-> None :
    """
    A gui for the user to select the names of the pnp & legend files

    Parameters
    ---------------
    folder : Production_folder
        The object that represents the production file
    root : tkinter.Tk
        the root where the gui will be added 
    list_btn : 
        the list of the menu btn that need to be enabled at the end of the step

    """
    
    @typechecked
    def validate_fct()-> None:
        """
        Function triggered when the validate btn is pressed
        It appends the chosen names to the list in the production folder
        It also enables again the buttons on the menu 

        """
        try :
            folder.enter_pnp_and_legend_files(pnp_bot=list_box1.get(list_box1.curselection()), pnp_top=list_box2.get(list_box2.curselection()), legend_bot =list_box3.get(list_box3.curselection()), legend_top= list_box4.get(list_box4.curselection()))
        except :
            tk.messagebox.showwarning(title = 'ATTENTION', message = "Attention ! Tous les fichiers n'ont pas été sélectionné")
            pass
        frame.destroy()
        for btn in list_btn :
            btn.configure(state = tk.NORMAL)    
        

    frame = tk.Frame(root, bg ='#436D6D')
    frame.pack(fill=tk.Y, side='right')

    list_box1,label1 = create_files_listbox(frame, folder.path, 'bottom', 'Selectionner les fichiers P&P pour la face : ')

    
    label1.grid(row = 0, column=0, padx=10)
    list_box1.grid(row = 1, column=0)

    list_box2, label2 = create_files_listbox(frame, folder.path, 'top', 'Selectionner les fichiers P&P pour la face : ')
    
    label2.grid(row = 0, column=1, padx=10)
    list_box2.grid(row = 1, column=1)
    
    list_box3, label3 = create_files_listbox(frame, folder.path, 'bottom', 'Selectionner les fichiers de légende pour la face : ')
    
    label3.grid(row = 2, column=0, padx=10)
    list_box3.grid(row = 3, column=0)

    list_box4, label4 = create_files_listbox(frame, folder.path, 'top', 'Selectionner les fichiers de légende pour la face : ')
    
    label4.grid(row =2, column=1, padx=10)
    list_box4.grid(row = 3, column=1)

    tk.Button(frame, text="Valider",fg="white", bg ='#436D6D', command=validate_fct).grid(row=4, column =1, pady=15, padx=50)
    
    return 


@typechecked
def create_files_listbox(root : tk.Frame, folder_path: str, side: str, text: str)-> tuple:
    """
    Create the list box of the file names that are in the production folder

    Parameters
    ---------------
    root : tkinter.Tk
        Root where the list box is created
    folder_path : str
        the folder that will be read
        all the files that are in will be proposed to the user

        
    Returns
    ---------------
    tuple : 
        contains the list of the boxes and the list of their label

    """
    t='\n'+text+side+'\n'
    label = tk.Label(root, text= t, font =(10), fg="white", bg ='#436D6D')
    
    l=os.listdir(folder_path)
    list_box = tk.Listbox(root, height=len(l),width = 40, relief='flat', selectbackground="#2F4F4F", bg ='#436D6D', fg = 'white', selectforeground ='white', exportselection = False, highlightcolor = 'white')
    for i in range(len(l)):
        list_box.insert(i,l[i]) 

    return list_box,label













