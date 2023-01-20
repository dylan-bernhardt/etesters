import tkinter as tk
import importlib
import turtle
import pandas as pd
from typeguard import typechecked
import etesters.select_test_points as tp

class GerberImage:
	@typechecked
	def __init__(self,folder: tp.Production_folder, side: str)-> None:
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
	def draw(self, root: tk.Tk, btn: tk.Button)-> None:
		self.btn = btn
		self.xmin,self.ymin,self.xmax,self.ymax= min_max_values(self.d, self.side)
		self.folder.set_pcb_dimension(self.xmin, self.xmax, self.ymin, self.ymax)
		self.canva = tk.Canvas(root)
		self.canva.pack(side='right')
		tk.Button(self.canva,bg='#436D6D', text='Valider', fg='white', command=self.btn_func).pack()

		screen=turtle.TurtleScreen(self.canva)
		turtle.setup(width=1280, height=720)
		turtle.setworldcoordinates(self.xmin,self.ymin,self.xmax,self.ymax+((self.ymax-self.ymin)/720)*150)
		turtle.tracer(0)
		turtle.hideturtle()

		draw_title(self.side, self.xmin, self.xmax, self.ymax, self.ymin)
		turtle.update()

		turtle.pu()
		turtle.goto(0,0)
		turtle.dot(20,'blue')

		draw_gerber(self.d)
		turtle.update()

		draw_tp(self.tp_df)
		turtle.update()

		turtle.onscreenclick(self.recolor)
		return

	@typechecked
	def recolor(self,x,y)-> None:
		
		new_color = 'red'
		for i in range(len(self.tp_df['x'])):
			if abs(x-self.tp_df['x'][i])<10*abs(self.xmax-self.xmin)/1280 and abs(y-self.tp_df['y'][i])<10*abs(self.ymax-self.ymin)/720:
				turtle.pu()
				turtle.goto(self.tp_df['x'][i],self.tp_df['y'][i])
				if self.tp_df['color'][i] == 'red':
					new_color='green'
				self.tp_df.at[i, 'color']=new_color    
				turtle.dot(20,new_color)
				
		turtle.update()
		return			        

	@typechecked
	def btn_func(self)-> None:
		self.tp_df.drop(self.tp_df[self.tp_df['color'] == 'red'].index, inplace=True)
		self.tp_df.drop(['color'], axis=1, inplace=True)
		self.folder.enter_final_tp_names(self.tp_df.reset_index(),self.side)
		self.canva.destroy()
		self.btn.configure(state = tk.NORMAL)
		return


@typechecked
def read_gerber(file_name :str,folder_path: str)-> list :

	f=open(folder_path+'/'+file_name,'r')
	lines = f.readlines()
	f.close()
	return lines


@typechecked
def rearrange_useful_values(lines :list)-> dict:

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

	xmin= min(d['x'])
	ymin= min(d['y'])
	xmax= max(d['x'])
	ymax= max(d['y'])
	if side== 'bottom':
		xmin,xmax= xmax,xmin
	return xmin,ymin,xmax,ymax


@typechecked
def draw_gerber(d: dict)-> None:

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

	for i in range(len(tp_df['x'])):
		turtle.pu()
		turtle.goto(tp_df['x'][i],tp_df['y'][i])
		turtle.dot(20,'green')
	return


@typechecked
def draw_title(side: str, xmin: float, xmax: float, ymax: float, ymin : float)-> None:
   
	turtle.pu()
	turtle.goto((xmax+xmin)/2,ymax+((ymax-ymin)/720)*100)
	text= 'Sélectionner les test points que vous souhaitez garder pour le banc, puis fermer.\n Ne fermez pas tant que l image n est pas apparue'
	turtle.write(text, align='center', font=('Verdana',10,"normal"))
	turtle.goto((xmax+xmin)/2,ymax+((ymax-ymin)/720)*60)
	text= 'FACE : ' + side
	turtle.write(text, align='center', font=('Verdana',15,"bold"))
	return

