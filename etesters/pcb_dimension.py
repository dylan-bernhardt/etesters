import tkinter as tk
import etesters.select_test_points as tp
from typeguard import typechecked

class pcb_dimension :
    """
    Gui where the user can choose the pcb (which will be used for the bench) dimensions.

    Attributes
    ------------------
    center : str
        Chooses if the origin matches with the center of the card or not
    folder : select_test_points.Production_folder
        Represents the production folder
    frame : tkinter.Frame
        Frame created to host the widgets
    s1 : tkinter.Spinbox
        The user types the values in
    s2 : tkinter.Spinbox
        The user types the values in
    xmin : float
        coordinate of vertex
    ymin : float
        coordinate of vertex
    xmax : float
        coordinate of vertex
    ymax : float
        coordinate of vertex 


    Methods
    -----------------
    __init__(folder, center):
        Initializes the useful elements as attributes for the class
    validate_fct():
        Function triggered when the Validate button is pressed
    display(root,list_btn):
        Display the gui

    """
    @typechecked
    def __init__(self,folder: tp.Production_folder, center: str)-> None :
        """
        Initializes the useful elements as attributes for the class

        Parameters
        -------------------
        folder : select_test_points.Production_folder
            The object represents the production folder which contains every information about the folder
        center : str
            Chooses if the origin matches with the center of the card or not
        
        """
        
        self.center= center
        self.folder = folder
        return 

    @typechecked
    def set_pcb_dimension(self, xmin: float, xmax: float, ymin: float, ymax:float)->None:
        """
        sets the pcb dimension

        Parameters
        --------------------
        xmin : float
            minimum x value
        xmax: float
            maximum x value
        ymin: float
            minimum y value
        ymax: float
            maximum y value
        """
        self.xmin = xmin
        self.ymin = ymin
        self.xmax=xmax
        self.ymax=ymax
        return


    @typechecked
    def validate_fct(self)-> None:
        """
        Function triggered when the validate button is pressed.
        It sets the dimension in the class.
        """
    
        longueur = float(self.s1.get())
        largeur = float(self.s2.get())
        if self.center == "yes":
            self.set_pcb_dimension(-(longueur)/2,longueur/2,-(largeur)/2, largeur/2)
        else : 
            self.set_pcb_dimension(0,longueur,0, largeur)

        for btn in self.list_btn :
            btn.configure(state = tk.NORMAL)
        self.frame.destroy()
        
        return  


    @typechecked
    def display(self, root: tk.Tk , list_btn :list ) -> None :
        """
        Display the gui. There are two spinboxes and one validate button.

        Parameters
        ------------------
        root : tkinter.Tk
            The root where the gui will be added
        list_btn : list
            The list of the buttons in the menu which have to be enabled at the end of the step.
        """
        
        self.list_btn =  list_btn
        self.frame = tk.Frame(root, bg ='#436D6D')
        self.frame.pack(fill=tk.Y, side='right')
        tk.Label(self.frame, text= 'Longueur', bg = '#436D6D', fg = 'white').grid(row=0, column= 0, pady =10, padx=10)
        tk.Label(self.frame, text= 'Largeur', bg= '#436D6D', fg = 'white').grid(row=0, column= 1, pady =10, padx=10)
        self.s1 = tk.Spinbox(self.frame, from_=abs(self.folder.xmin) + abs(self.folder.xmax), to=(abs(self.folder.xmin) + abs(self.folder.xmax))*10)
        self.s2 = tk.Spinbox(self.frame, from_=abs(self.folder.ymin) + abs(self.folder.ymax),  to=(abs(self.folder.xmin) + abs(self.folder.xmax))*10)
        self.s1.grid(row = 1, column = 0, pady =10, padx=10)
        self.s2.grid(row= 1, column = 1, pady =10, padx=10)


        tk.Button(self.frame, text="Valider",fg="white", bg ='#436D6D', command=self.validate_fct).grid(row=2, column =1, pady=15, padx=50)

        
        return
    