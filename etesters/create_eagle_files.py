import pandas as pd
from typeguard import typechecked
import etesters.select_test_points as tp
import etesters.pcb_dimension

import etesters



class DefaultSCH:
	"""
	A default .sch file that can be automatically modified and written 

	Attributes
	-------------------
	file: list
		list of the lines of the default file

	Methods
	------------------
	__init__(file_path):
		Initializes the class by reading a default sch file and storing it in a list
	write_file(path):
		Writes the new file in the folder specified in parameters
	add_one_part(index, name, value, deviceset, device, library, package3d_urn):
		Adds one part to the file
	add_all_parts(df):
		Adds all parts to the file
	add_one_instance( index, part, x, y, smashed, gate, size, layer, font, ratio, align):
		Adds one instance to the file
	add_all_instances(df):
		Adds all instances to the file
	add_one_net(index, x, y, name, class_, gate, pin, width,layer,size):
		Adds one net to the file
	add_all_nets(df)
		Adds all nets to the file

	"""

	@typechecked
	def __init__(self, file_path: str)-> None:
		"""
		Initializes the class by reading a default sch file and storing it in a list

		Parameters
		----------------------
		file_path : str
			Default = './default.sch'
			The path of the default file that will modified
		"""
		f = open(file_path,'r')
		self.file = f.read().splitlines()
		f.close()
		self._nb_tp_already_written = 0
		return
	

	@typechecked
	def write_file(self, path: str)-> None:
		"""
		Writes the new file in the folder specified in parameters

		Parameters
		-------------
		path : str
			the folder where the user wants to save the file
		
		"""
		f = open(path+"/etesters001.sch", 'w')
		for line in self.file :
			f.write(line+'\n')
		f.close()
		return


	@typechecked
	def add_one_part(self, index:int, name : str, value: str, deviceset: str ='TESPOINT', device: str='-SMD1.5MM', library: str='Generics_stg', package3d_urn="urn:adsk.eagle:package:19402626/2")-> None:
		"""
		Adds one part to the file

		Parameters
		-----------------------
		index: int
			the index where the part will be added
		name: str
			characteristic of a testpoint
		value :str
			characteristic of a testpoint
		deviceset : str
			Default = 'TESPOINT'
			characteristic of a testpoint
		device: str
		Default = '-SMD1.5MM'
			characteristic of a testpoint
		library: str
			Default = 'Generics_stg'
			characteristic of a testpoint
		package3d_urn: str
			Default = "urn:adsk.eagle:package:19402626/2"
			characteristic of a testpoint
		"""
		self.file.insert(index, '<part name="%s" library="%s" deviceset="%s" device="%s" package3d_urn="%s" value="%s"/>' %(name.strip(), library, deviceset, device, package3d_urn, value.strip()))
		return


	@typechecked
	def add_all_parts(self, df: pd.DataFrame)-> None:
		"""
		From the testpoints dataframe, adds all the parts in the file

		Parameters
		------------------
		df : pandas.DataFrame
			dataframe that contains the characteristics of the testpoints
		"""
		close_parts = self.file.index('</parts>')
		for i in range(len(df)) :
			self.add_one_part(close_parts, df['signal_name'][i], df['value'][i])
			close_parts += 1
		return


	@typechecked
	def add_one_instance(self, index: int, part: str, x:float, y: float, smashed: str ='yes', gate : str = 'TP1', size: str ='2.54', layer: str='95', font: str='vector', ratio: str="16", align:str='center-left')-> None:
		"""
		Adds one instance to the file

		Parameters
		------------------------------
		index: int
			the index where the instance will be added
		name: str
			characteristic of a testpoint
		part: str
			characteristic of a testpoint
		x: float
			x position
		y: float
			y position
		smashed : str
			Default = 'yes'
			characteristic of a testpoint
		gate: str
			Default = 'TP1'
			characteristic of a testpoint
		size: str
			default = '2.54'
			characteristic of a testpoint
		layer: str
			default = '95'
			characteristic of a testpoint
		font: str
			default = 'vector'
			characteristic of a testpoint
		ratio: str
			default='16'
			characteristic of a testpoint
		align: str
			default = 'center-left'
			characteristic of a testpoint
		"""
		self.file.insert(index,'<instance part="%s" gate="%s" x="%.3f" y="%.3f" smashed="%s">' % (part,gate,x,y,smashed))
		self.file.insert(index+1,'<attribute name="NAME" x="%.3f" y="%.3f" size="%s" layer="%s" font="%s" ratio="%s" align="%s"/>' % (x,y,size,layer,font,ratio,align))
		self.file.insert(index+2,'</instance>')
		return


	@typechecked
	def add_all_instances(self, df: pd.DataFrame):
		"""
		From the testpoints dataframe, adds all the instances in the file

		Parameters
		------------------
		df : pandas.DataFrame
			dataframe that contains the characteristics of the testpoints
		"""
		close_instances = self.file.index('</instances>')
		for i in range(len(df)):
			self.add_one_instance(close_instances , df['signal_name'][i], 0, (i+self._nb_tp_already_written)*5.08)
			close_instances +=3
		return

	@typechecked
	def add_one_net(self,index: int, x: float, y: float, name: str, class_: str="0", gate: str="TP1", pin: str="P$1", width: str="0.1524", layer :str="95", size: str = '1.778')-> None:
		"""
		Adds one net to the file

		Parameters
		--------------------
		index: int
			the index where the net will be added
		x: float
			x position
		y: float
			y position
		name :str
			characteristic of a testpoint
		class_: str
			default = '0'
			characteristic of a testpoint
		gate: str
			default = 'TP1'
			characteristic of a testpoint
		pin: str
			default = 'P$1'
			characteristic of a testpoint
		width: str
			default = '0.1524'
			characteristic of a testpoint
		layer : str
			default = '95'
			characteristic of a testpoint
		size : str
			default = '1.778'
			characteristic of a testpoint

		"""
		self.file.insert(index,'<net name="%s" class="%s">' % (name.strip(),class_))
		self.file.insert(index+1,'<segment>')
		self.file.insert(index+2,'<pinref part="%s" gate="%s" pin="%s"/>' % (name.strip(), gate, pin))
		self.file.insert(index+3, '<wire x1="%.3f" y1="%.3f" x2="%.3f" y2="%.3f" width="%s" layer="91"/>' % (x-5.08,y,x-20.32,y,width))
		self.file.insert(index+4, '<label x="%.3f" y="%.3f" size="%s" layer="%s"/>' % (x-17.18,y,size,layer))
		self.file.insert(index+5, '</segment>')
		self.file.insert(index+6, '</net>')
		return

	@typechecked
	def add_all_nets(self, df: pd.DataFrame)->None:
		"""
		Adds all nets to the file, from a df

		Parameters
		-----------------
		df: pandas.DataFrame
			the dataframe contains the characteristics of the tp that the users chose
		"""
		close_nets = self.file.index('</nets>')
		for i in range(len(df)):
			self.add_one_net(close_nets, 0, (i+self._nb_tp_already_written)*5.08, df['signal_name'][i])
			close_nets+=7
		self._nb_tp_already_written = len(df)

		return



class DefaultBRD:

	"""
	A default .sch file that can be automatically modified and written

	Attributes
	-------------------
	file: list
		list of the lines of the default file

	Methods
	------------------
	__init__(file_path):
		Initializes the class by reading a default brd file and storing it in a list
	write_file(path):
		Write the new file in the folder specified in parameters
	add_rectangular_board(x0,y0,x1,y1):
		Adds a rectangular board to the file
	add_one_element(index, name, x, y, value, package, library, package3d_urn, smashed, size ,layer, ratio, align):
		Adds one element to the file
	add_all_elements(df):
		Add all elements to the file
	add_one_signal(index, name, pad):
		Add one signal to the file
	add_all_signals(df):
		Add al signals to the file


	
	"""

	@typechecked
	def __init__(self, file_path: str)-> None:
		"""
		Initializes the class by reading a default brd file and storing it in a list

		Parameters
		----------------------
		file_path : str
			The path of the default file that will modified
		"""
		f = open(file_path,'r')
		self.file = f.read().splitlines()
		f.close()
		return


	@typechecked
	def write_file(self, path)-> None:
		"""
		Writes the new file in the folder specified in parameters

		Parameters
		-------------
		path : str
			the folder where the user wants to save the file
		"""
		f = open(path+"/etesters001.brd", 'w')
		for line in self.file :
			f.write(line+'\n')
		f.close()
		return


	@typechecked
	def add_rectangular_board(self, x0: float, y0: float, x1: float, y1: float)-> None:
		"""
		Adds the rectangular board in the file

		Parameters
		-------------------
		x0 :float
			 minimum x value
		y0 :float
			 minimum y value
		x1 :float
			maximum x value	 
		y1 :float
			 maximum y value
		"""
		close_board = self.file.index('</plain>')
		self.file.insert(close_board,'<wire x1="%d" y1="%d" x2="%d" y2="%d" width="0" layer="20"/>' % (x0, y0, x0, y1))
		self.file.insert(close_board,'<wire x1="%d" y1="%d" x2="%d" y2="%d" width="0" layer="20"/>' % (x0, y0, x1, y0))
		self.file.insert(close_board,'<wire x1="%d" y1="%d" x2="%d" y2="%d" width="0" layer="20"/>' % (x1, y0, x1, y1))
		self.file.insert(close_board,'<wire x1="%d" y1="%d" x2="%d" y2="%d" width="0" layer="20"/>' % (x0, y1, x1, y1))
		return


	@typechecked
	def add_one_element(self , index: int, name: str, x:float, y:float, value: str, package: str, library: str = "Generics_stg", package3d_urn: str="urn:adsk.eagle:package:19402626/2", smashed: str="yes", size:float = 1 ,layer :int = 25, ratio: int= 16, align: str= 'center-left', locked:str='yes')-> None:
		"""
		Adds one element to the file

		Parameters
		-------------------
		index:int
			the index where the element will be added
		name :str
			characteristic of a test point
		x:float
			x position
		y: float
			y position
		value:str
			characteristic of a test point
		package: str
			characteristic of a test point
		library: str
			default = "Generics_stg"
			characteristic of a test point
		package3d_urn:str
		default = "urn:adsk.eagle:package:19402626/2"
			characteristic of a test point
		smashed:str
		default = "yes"
			characteristic of a test point
		size:float
			default = 1
			characteristic of a test point
		layer:int
			default = 25
			characteristic of a test point
		ratio:float
			default = 16
			characteristic of a test point
		align:str
			default = "center-left"
			characteristic of a test point
		locked : str
			default = 'yes'
			characterisitc of a test point
		"""
		self.file.insert(index,'<element name="%s" library="%s" package="%s" package3d_urn="%s" value="%s" x="%.3f" y="%.3f" locked="%s" smashed="%s">' % (name.strip(),library,package.strip(),package3d_urn,value.strip(),x,y,locked,smashed))
		self.file.insert(index+1,'<attribute name="NAME" x="%.3f" y="%.3f" size="%.3f" layer="%d" ratio="%d" align="%s"/>' % (x+1,y,size,layer,ratio,align))
		self.file.insert(index+2,'</element>')
		return


	@typechecked
	def add_all_elements(self, df : pd.DataFrame)-> None:
		"""
		From the testpoints dataframe, adds all the elements in the file

		Parameters
		------------------
		df : pandas.DataFrame
			dataframe that contains the characteristics of the testpoints
		"""
		close_elements = self.file.index('</elements>')
		for i in range(len(df)):
			self.add_one_element(close_elements, df['signal_name'][i], df['x'][i], df['y'][i] ,df['value'][i], df['package'][i])
			close_elements += 3
		return


	@typechecked
	def add_one_signal(self, index, name: str, pad: str='1')-> None:
		"""
		Adds one signal to the file

		Parameters
		------------------------------
		index: int
			the index where the signal will be added
		name : str
			characteristic of the tp
		pad : str
			default = '1'
			characteristic of the tp
		"""

		self.file.insert(index,'<signal name="%s">' % name.strip())
		self.file.insert(index+1,'<contactref element="%s" pad="%s"/>' % (name.strip(),pad))
		self.file.insert(index+2,'</signal>')
		return


	@typechecked
	def add_all_signals(self, df: pd.DataFrame)-> None:
		"""
		From the testpoints dataframe, adds all the signals in the file

		Parameters
		------------------
		df : pandas.DataFrame
			dataframe that contains the characteristics of the testpoints
		"""
		close_signals = self.file.index('</signals>')
		for i in range(len(df)):
			self.add_one_signal(close_signals, df['signal_name'][i])
			close_signals+=3
		return



@typechecked
def create_brd_file(folder: tp.Production_folder, dimension : etesters.pcb_dimension.pcb_dimension, path: str)-> None:
	"""
	Create the .brd file for the new pcb 

	Parameters
	----------------
	folder : select_test_points.Production_folder
		the production folder
	dimension: pcb_dimension.pcb_dimension
		dimension of the new pcb
	path: str
		the path where the file is created
	"""
	brd_file= DefaultBRD(etesters.__path__[0] + "/default.brd")
	brd_file.add_rectangular_board(dimension.xmin, dimension.ymin, dimension.xmax, dimension.ymax)
	brd_file.add_all_elements(folder.final_tp_names_bot_df)
	brd_file.add_all_elements(folder.final_tp_names_top_df)
	brd_file.add_all_signals(folder.final_tp_names_bot_df)
	brd_file.add_all_signals(folder.final_tp_names_top_df)
	brd_file.write_file(path)
	return


@typechecked
def create_sch_file(folder: tp.Production_folder, path: str)-> None:
	"""
	Create the .sch file for the new pcb 
	
	Parameters
	----------------
	folder : select_test_points.Production_folder
		the production folder
	path: str
		the path where the file is created
	"""
	sch_file = DefaultSCH(etesters.__path__[0] + "/default.sch")
	sch_file.add_all_instances(folder.final_tp_names_bot_df)
	sch_file.add_all_parts(folder.final_tp_names_bot_df)
	sch_file.add_all_nets(folder.final_tp_names_bot_df)
	sch_file.add_all_instances(folder.final_tp_names_top_df)
	sch_file.add_all_parts(folder.final_tp_names_top_df)
	sch_file.add_all_nets(folder.final_tp_names_top_df)
	sch_file.write_file(path)
	return






