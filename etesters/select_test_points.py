
import pandas as pd
from typeguard import typechecked
import tkinter as tk
import os


class Production_folder :

    @typechecked
    def __init__(self)-> None:
        self.path = './production'
        self.tp_names_top=[]
        self.tp_names_bot=[]
        return 

    @typechecked
    def change_path(self, path : str)-> None:
        self.path = path
        return

    @typechecked
    def enter_files(self, pnp_bot: str, pnp_top: str, legend_top: str, legend_bot: str)-> None:
        self.pnp_bot=pnp_bot
        self.pnp_top=pnp_top
        self.legend_top = legend_top
        self.legend_bot=legend_bot
        return 

    @typechecked
    def enter_tp_names(self, name : str, side : str)-> None:
        if side =='top':
            self.tp_names_top.append(name)
        if side == 'bottom':
            self.tp_names_bot.append(name)
        return

    @typechecked
    def tp_names_list_clear(self)-> None:
        self.tp_names_top.clear()
        self.tp_names_bot.clear()
        return 

    @typechecked
    def enter_final_tp_names(self, df: pd.DataFrame, side :str)-> None:
        if side=='top':
            self.final_tp_names_top_df=df
        if side=='bottom':
            self.final_tp_names_bot_df=df
        return

    @typechecked
    def set_pcb_dimension(self, xmin: float, xmax: float, ymin: float, ymax: float)-> None:
        self.xmax = xmax
        self.xmin = xmin
        self.ymin = ymin
        self.ymax = ymax
        return



@typechecked
def filter_test_points(pd: pd.DataFrame, list_tp: list, column_name: str = 'package') -> pd.DataFrame:
    """
    Filter a dataframe with test points
    @param pd: dataframe to filter
    @param list_tp: list of test points to filter
    @param column_name: name of the column to filter
    @return: filtered dataframe
    """
    filtered_df = pd[pd[column_name].apply(lambda s: s.strip()).isin(list_tp)]
    return filtered_df


@typechecked
def filter_test_points_file(file_name: str, list_tp: list, folder_path: str, column_name: str = 'package') -> pd.DataFrame:
    """
    Filter a csv file with test points
    @param file_name: name of the csv file to filter
    @param list_tp: list of test points to filter
    @param column_name: name of the column to filter
    @return: filtered dataframe
    """
    df = pd.read_csv(folder_path+'/'+file_name, delimiter=',', names=['signal_name', 'x', 'y', 'angle', 'value', column_name])
    filtered_df = filter_test_points(df, list_tp, column_name)
    return filtered_df


@typechecked
def create_filtered_test_points_file(file_name: str, list_tp: list, folder_path: str, column_name: str = 'package') -> None:
    """
    Create a new csv file with the filtered test points of a csv file
    @param file_name: name of the csv file to filter
    @param list_tp: list of test points to filter
    @param column_name: name of the column to filter
    @param filtered_name: name of the new csv file
    """
    filtered_name= 'FILTERED__'+file_name
    filtered_df = filter_test_points_file(file_name, list_tp, folder_path, column_name)


    isExist = os.path.exists(folder_path+'/filtered_pnp')
    if not isExist:
        os.makedirs(folder_path+"/filtered_pnp")
    
    filtered_df.to_csv(folder_path+'/filtered_pnp/'+filtered_name, sep=",", mode="w", index=False)
    
    return




@typechecked
def gui_select_tp(folder: Production_folder, root: tk.Tk, column_name: str = 'package') -> None:
    
    #@typechecked
    def select_all_checkbutton1(*args)-> None:
        for i in range(len(btn1)):
            if select_all1.get()==1:
                btn1[i].select()
            else:
                btn1[i].deselect()
        return

    #@typechecked
    def select_all_checkbutton2(*args)-> None:
        for i in range(len(btn2)):
            if select_all2.get()==1:
                btn2[i].select()
            else:
                btn2[i].deselect()
            return

    @typechecked
    def exit1()-> None:
        for i in range(len(enable1)):
            if enable1[i].get()==1:
                folder.enter_tp_names(l1[i].strip(),'bottom')
        

        create_filtered_test_points_file(folder.pnp_bot, folder.tp_names_bot, folder.path)
        frame1.destroy()
        return


    @typechecked
    def exit2()-> None:

        for i in range(len(enable2)):
            if enable2[i].get()==1:
                folder.enter_tp_names(l2[i].strip(),'top')
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
def gui_select_pnp_file(folder: Production_folder, root: tk.Tk)-> None :
    
    @typechecked
    def validate_fct()-> None:
        folder.enter_files(pnp_bot=list_box1.get(list_box1.curselection()), pnp_top=list_box2.get(list_box2.curselection()), legend_bot =list_box3.get(list_box3.curselection()), legend_top= list_box4.get(list_box4.curselection()))
        frame.destroy()
        

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


    t='\n'+text+side+'\n'
    label = tk.Label(root, text= t, font =(10), fg="white", bg ='#436D6D')
    
    l=os.listdir(folder_path)
    list_box = tk.Listbox(root, height=len(l),width = 40, relief='flat', selectbackground="#2F4F4F", bg ='#436D6D', fg = 'white', selectforeground ='white', exportselection = False, highlightcolor = 'white')
    for i in range(len(l)):
        list_box.insert(i,l[i]) 

    return list_box,label













