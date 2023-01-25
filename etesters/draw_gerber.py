import tkinter as tk
import importlib
import turtle
import pandas as pd
from typeguard import typechecked
import etesters.select_test_points as tp



class GerberImage:
	"""
	An image of a gerber file
	The user can choose on it the testpoints to keep or not
	
	Attributes
	--------------------
	folder : select_test_points.Production_folder
		The production folder
	side: str
		the side of the drawing
	tp_df: pandas.DataFrame
		dataframe that contains characteritic of the test point
		the dataframe is filtered by the user choice
		the testpoints represented by a red dot are removed
	xmin: float
		size of the card
	xmax: float
		size of the card
	ymin: float
		size of the card
	ymax: float
		size of the card

	Methods
	-------------------------
	__init__(folder,side):
		Initialize and rearrange the useful values
	center_0_0():
		center the center of the card
	draw(root,list_btn):
		Draw the title, the card and his testpoints on a blank page
		A validate button is also create
	recolor(x,y):
		recolor the testpoint when you click on it
	btn_funct():
		validate btn function
	
	"""

	@typechecked
	def __init__(self,folder: tp.Production_folder, side: str)-> None:
		"""
		Initialize and rearrange the useful values

		Parameters
		--------------
		folder : select_test_points.Production_folder
			the object that represents the production folder
		side :str
			the side of the card to draw

		"""
		importlib.reload(turtle)
		self.folder = folder
		self.side=side
		if side=='top':
			self.d = rearrange_useful_values(read_gerber(self.folder.legend_top, self.folder.path))
			self.tp_df= pd.read_csv(self.folder.path+'/filtered_pnp/'+'FILTERED__'+self.folder.pnp_top, delimiter=',')
			self.tp_df=self.tp_df.assign(color='green')

		elif side=='bottom':
			self.d = rearrange_useful_values(read_gerber(self.folder.legend_bot, self.folder.path))
			self.tp_df= pd.read_csv(self.folder.path+'/filtered_pnp/'+'FILTERED__'+self.folder.pnp_bot, delimiter=',')
			self.tp_df=self.tp_df.assign(color='green')
		return
		

	@typechecked
	def center_0_0(self)-> None :
		"""
		If the user wants to center the card on the reper, he/she can
		Every values is modified to center the card
		"""
		xmin,ymin,xmax,ymax = min_max_values(self.d, 'top')
		x_add = -xmin - (xmax-xmin)/2
		y_add = -ymin - (ymax-ymin)/2
		self.tp_df['x']+=x_add
		self.tp_df['y']+=y_add
		for i in range(len(self.d['x'])):
			self.d['x'][i] += x_add
			self.d['y'][i] += y_add
		return


	@typechecked
	def draw(self, root: tk.Tk, list_btn: list)-> None:
		"""
		Draw the title, the card and his testpoints on a blank page
		A validate button is also created

		Parameters 
		---------------------
		root : tkinter.Tk	
			the root where the button has to be added
		list_btn : list
			the button of the menu that need to be enabled at the end of the step
		"""
		self.list_btn = list_btn
		self.xmin,self.ymin,self.xmax,self.ymax= min_max_values(self.d, self.side)
		

		self.folder.set_pcb_dimension(self.xmin, self.xmax, self.ymin, self.ymax)
		
		turtle.setup(width=1600, height=900)
		if self.side == "bottom":
			turtle.setworldcoordinates(self.xmin+(50*abs(self.xmin-self.xmax)/1500),self.ymin-(100*(self.ymax-self.ymin)/700),self.xmax-(50*abs(self.xmin-self.xmax)/1500),self.ymax+(100*(self.ymax-self.ymin)/700))

			
			
		if self.side == "top":
			turtle.setworldcoordinates(self.xmin-(50*(self.xmax-self.xmin)/1500),self.ymin-(100*(self.ymax-self.ymin)/700),self.xmax+(50*(self.xmax-self.xmin)/1500),self.ymax+(100*(self.ymax-self.ymin)/700))
			
		
		self._px_size_x = abs(self.xmax-self.xmin)/1500
		self._px_size_y = abs(self.ymax - self.ymin)/700
		turtle.tracer(0)
		turtle.hideturtle()


		
		
		
		draw_title(self.side, self.xmin, self.xmax, self.ymax, self.ymin, self._px_size_y)
		turtle.update()

		draw_gerber(self.d)
		turtle.update()

		draw_tp(self.tp_df)
		turtle.update()

		draw_axis(self.side, self.xmin, self.xmax, self.ymin, self.ymax, self._px_size_x, self._px_size_y)
		turtle.update()

		draw_coordinates(self.xmin, self.xmax, self.ymin, self.ymax)
		turtle.update()

		draw_legend(self.side, self.xmin, self.xmax, self.ymin, self.ymax, self._px_size_x, self._px_size_y)
		turtle.update()

		turtle.onscreenclick(self.btn)
		return


	@typechecked
	def btn(self,x,y)-> None:	
		"""
		Every test point is represented by a green dot
		When you click on it, it became red
		If you click again, it became green again
		It allows the user to choose which test point he/she wants to keep

		Parameters
		----------------
		x: float
			the x-axis value where the mouse pointer was when the user clicked
		y: float
			the y-axis value where the mouse pointer was when the user clicked
		"""
		sgn = 1
		if self.side == "bottom":
			sgn = -1
		new_color = 'red'
		for i in range(len(self.tp_df['x'])):
			if abs(x-(self.tp_df['x'][i]))<=10*self._px_size_x and abs(y-self.tp_df['y'][i])<=10*self._px_size_y:
				turtle.pu()
				turtle.goto(self.tp_df['x'][i],self.tp_df['y'][i])
				if self.tp_df['color'][i] == 'red':
					new_color='green'
				self.tp_df.at[i, 'color']=new_color    
				turtle.dot(20,new_color)



		if abs(x-(self.xmin+sgn*700*self._px_size_x))<=10*self._px_size_x and abs(y-(self.ymin-80*self._px_size_y))<=10*self._px_size_y:
			for i in range(len(self.tp_df['x'])):
				turtle.pu()
				turtle.goto(self.tp_df['x'][i],self.tp_df['y'][i])
				turtle.dot(20,"green")
				self.tp_df.at[i, 'color']="green"

		if abs(x-(self.xmin+sgn*1000*self._px_size_x))<=10*self._px_size_x and abs(y-(self.ymin-80*self._px_size_y))<=10*self._px_size_y :
			for i in range(len(self.tp_df['x'])):
				turtle.pu()
				turtle.goto(self.tp_df['x'][i],self.tp_df['y'][i])
				turtle.dot(20,"red")
				self.tp_df.at[i, 'color']="red"

		if abs(x-(self.xmax-sgn*30*self._px_size_x))<=50*self._px_size_x and abs(y-(self.ymin-80*self._px_size_y))<= 20*self._px_size_y :
			self.tp_df.drop(self.tp_df[self.tp_df['color'] == 'red'].index, inplace=True)
			self.tp_df.drop(['color'], axis=1, inplace=True)
			self.folder.enter_final_tp_names(self.tp_df.reset_index(),self.side)
			turtle.bye()
			for btn in self.list_btn :
				btn.configure(state = tk.NORMAL)
			return

		
		turtle.update()


			
		
		
		return			        


@typechecked
def read_gerber(file_name :str,folder_path: str)-> list :
	"""
	Read a gerber file and stored its lines in a list

	Parameters
	-------------------
	file_name : str
		the name of the file to read
	folder_path : str
		the path of the fodler where the file to read is stored

	Returns
	-------------------
	list 
		the list that contains every lines of the file
	"""
	f=open(folder_path+'/'+file_name,'r')
	lines = f.readlines()
	f.close()
	return lines


@typechecked
def rearrange_useful_values(lines :list)-> dict:
	"""
	Rearrange the useful values from the list of the lines of the gerber file

	Parameters
	---------------------
	lines: list
		the lines of the file are stored in the list
	Returns
	----------------
	dict
		rearranged dictionnary
	"""
	extract_dict = {'x': [], 'y': [], 'd': [], 'precision': 0}
	for i in lines :
		fsla=i.find('FSLA')
		x=i.find('X')
		y=i.find('Y')
		d=i.find('D')
		star=i.find('*')
		if x!=-1 and y!=-1 and fsla!=-1:
			extract_dict['precision']=i[x+2]
		if x== 0 and y!= -1 and d!= -1 and star!= -1:
			extract_dict['x'].append(int(i[1:y])/(10**int(extract_dict['precision'])))
			extract_dict['y'].append(int(i[y+1:d])/(10**int(extract_dict['precision'])))
			extract_dict['d'].append(int(i[d+1:d+3]))
	return extract_dict


@typechecked
def min_max_values(d: dict, side: str='top')-> tuple:
	"""
	Extract and set the min,max of the card

	Parameters
	-----------------
	d : dict
		contains the values of the gerber file
	side : str
		Default = 'top'
		the side of the card
		if the side is bottom, we need to reverse the card to correctly see the legend ie. xmin,xmax = xmax,xmin
	
	Returns 
	-----------------
	tuple 
		tuple of the max values
	"""

	xmin= min(d['x'])
	ymin= min(d['y'])
	xmax= max(d['x'])
	ymax= max(d['y'])
	if side== 'bottom':
		xmin,xmax= xmax,xmin
	return xmin,ymin,xmax,ymax


@typechecked
def draw_gerber(d: dict)-> None:
	"""
	draw the gerber file
	the gerber file values are stored in a dict

	Parameters
	-----------------
	d: dict
		dict that contains the values of the gerber files
	"""
	turtle.pu()
	for i in range(len(d['x'])):
		if d['d'][i] == 1:
			turtle.pd()
			turtle.goto(d['x'][i],d['y'][i])
			turtle.pu()
		if d['d'][i] == 2:
			turtle.pu()
			turtle.goto(d['x'][i],d['y'][i])
		if d['d'][i] == 3:
			turtle.pu()
			turtle.goto(d['x'][i],d['y'][i])
	return


@typechecked
def draw_tp(tp_df: pd.DataFrame)-> None:
	"""
	Draw a green dot for every test points 

	Parameters
	----------------
	tp_df : pandas.DataFrame
		dataframe that contains the test points positions & names
	"""
	for i in range(len(tp_df['x'])):
		turtle.pu()
		turtle.goto(tp_df['x'][i],tp_df['y'][i])
		turtle.dot(20,'green')
	return


@typechecked
def draw_title(side: str, xmin: float, xmax: float, ymax: float, ymin : float, _px_size_y: float)-> None:
	"""
	Draw the title of the windows on his top
	It won't overlap the card drawing


	Parameters
	--------------------
	side : str
		the side of the drawing
	xmin : float
		dimension of the card drawing
	ymin: float
		dimension of the card drawing
	xmax: float
		dimension of the card drawing
	ymax: float
		dimension of the card drawing
	"""
	turtle.pu()
	turtle.goto((xmax+xmin)/2,ymax+(60 * _px_size_y))
	text= "Sélectionner les test points que vous souhaitez garder pour le banc, puis fermer.\n Ne fermez pas tant que l'image n'est pas apparue"
	turtle.write(text, align='center', font=('Verdana',10,"normal"))
	turtle.goto((xmax+xmin)/2,ymax+(35* _px_size_y))
	text= 'FACE : ' + side
	turtle.write(text, align='center', font=('Verdana',15,"bold"))
	return


@typechecked
def draw_axis(side: str, xmin: float, xmax: float, ymin: float, ymax: float, _px_size_x: float, _px_size_y: float)->None:
	if side == "bottom":
		sgn=-1 
	else:
		sgn=+1 
	_add_x = 50*_px_size_x
	_add_y = 30*_px_size_y
	turtle.pu()
	turtle.goto(xmax+sgn*_add_x,0)
	turtle.pd()
	turtle.goto(xmin-sgn*_add_x,0)
	turtle.pu()
	turtle.goto(0,ymax+_add_y)
	turtle.pd()
	turtle.goto(0,ymin-_add_y)
	turtle.pu()
	turtle.goto(0,-5*_px_size_y)
	turtle.pd()
	turtle.circle(5*_px_size_y)
	turtle.pu()

	turtle.goto(xmax+sgn*_add_x-sgn*5*_px_size_x,5*_px_size_y)
	turtle.pd()
	turtle.goto(xmax+sgn*_add_x,0)
	turtle.goto(xmax+sgn*_add_x-sgn*5*_px_size_x,-5*_px_size_y)
	turtle.pu()

	turtle.goto(xmin-sgn*_add_x+sgn*5*_px_size_x,5*_px_size_y)
	turtle.pd()
	turtle.goto(xmin-sgn*_add_x,0)
	turtle.goto(xmin-sgn*_add_x+sgn*5*_px_size_x,-5*_px_size_y)
	turtle.pu()

	turtle.goto(5*_px_size_x,ymax+_add_y-5*_px_size_y)
	turtle.pd()	
	turtle.goto(0,ymax+_add_y)
	turtle.goto(-5*_px_size_x,ymax+_add_y-5*_px_size_y)
	turtle.pu()

	turtle.goto(5*_px_size_x,ymin-_add_y+5*_px_size_y)
	turtle.pd()
	turtle.goto(0,ymin-_add_y)
	turtle.goto(-5*_px_size_x,ymin-_add_y+5*_px_size_y)
	turtle.pu()

	return


@typechecked
def draw_coordinates(xmin: float,xmax: float,ymin: float,ymax: float)->None :
	turtle.pu()
	turtle.goto(0,ymax)
	turtle.pd()
	turtle.write("%.1f" % ymax, align='center', font=('Verdana',10,"normal"))

	turtle.pu()
	turtle.goto(0,ymin)
	turtle.pd()
	turtle.write("%.1f" % ymin, align='center', font=('Verdana',10,"normal"))

	turtle.pu()
	turtle.goto(xmax,0)
	turtle.pd()
	turtle.write("%.1f" % xmax, align='center', font=('Verdana',10,"normal"))

	turtle.pu()
	turtle.goto(xmin,0)
	turtle.pd()
	turtle.write("%.1f" % xmin, align='center', font=('Verdana',10,"normal"))
	
	return


@typechecked
def draw_legend(side: str, xmin: float, xmax: float, ymin: float, ymax: float, _px_size_x: float, _px_size_y: float)-> None:
	sgn=1
	if side == "bottom":
		sgn = -1

	turtle.pu()
	turtle.goto(xmin+sgn*100*_px_size_x,ymin-80*_px_size_y)
	turtle.dot(20,'green')
	turtle.goto(xmin+sgn*200*_px_size_x, ymin-80*_px_size_y)
	turtle.pd()
	turtle.write("Sélectionné", align='right', font=('Verdana',10,"normal"))

	turtle.pu()
	turtle.goto(xmin+sgn*400*_px_size_x,ymin-80*_px_size_y)
	turtle.dot(20,'red')
	turtle.goto(xmin+sgn*550*_px_size_x, ymin-80*_px_size_y)
	turtle.pd()
	turtle.write("Non-sélectionné", align='right', font=('Verdana',10,"normal"))

	turtle.pu()
	turtle.goto(xmin+sgn*700*_px_size_x,ymin-80*_px_size_y)
	turtle.dot(20,'grey')
	turtle.goto(xmin+sgn*850*_px_size_x, ymin-80*_px_size_y)
	turtle.pd()
	turtle.write("Tout sélectionner", align='right', font=('Verdana',10,"normal"))

	turtle.pu()
	turtle.goto(xmin+sgn*1000*_px_size_x,ymin-80*_px_size_y)
	turtle.dot(20,'grey')
	turtle.goto(xmin+sgn*1150*_px_size_x, ymin-80*_px_size_y)
	turtle.pd()
	turtle.write("Tout désélectionner", align='right', font=('Verdana',10,"normal"))

	turtle.pu()
	turtle.goto(xmax-sgn*80*_px_size_x,ymin-60*_px_size_y)
	turtle.pd()
	turtle.goto(xmax+sgn*20*_px_size_x,ymin-60*_px_size_y)
	turtle.goto(xmax+sgn*20*_px_size_x,ymin-100*_px_size_y)
	turtle.goto(xmax-sgn*80*_px_size_x,ymin-100*_px_size_y)
	turtle.goto(xmax-sgn*80*_px_size_x,ymin-60*_px_size_y)
	turtle.pu()
	turtle.goto(xmax-sgn*9*_px_size_x,ymin-90*_px_size_y)
	turtle.write("Valider", align='right', font=('Verdana',10,"normal"))

	return

