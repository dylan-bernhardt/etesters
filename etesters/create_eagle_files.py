import pandas as pd
from typeguard import typechecked
import etesters.select_test_points as tp
import etesters.pcb_dimension



class DefaultSCH:
	"""
	A default .sch file that can be automatically modified and written 

	Attributes
	-------------------

	Methods
	------------------
	__init__
	write_file
	add_one_part
	add_all_parts
	add_one_instance
	add_all_instances

	"""

	@typechecked
	def __init__(self, file_path: str = './eagle_default/default.sch')-> None:
		"""
		Initializes the class by reading a default sch file and storing it in a list

		Parameters
		----------------------
		file_path : str
			Default = './eagle_default/default.sch'
			The path of the default file that will modified
		"""
		f = open(file_path,'r')
		self.file = f.read().splitlines()
		f.close()
		return
	

	@typechecked
	def write_file(self, path: str)-> None:
		"""
		Write the new file in the folder specified in parameters

		Parameters
		-------------
		path : str
			the folder where the user wants to save the file
		
		"""
		f = open(path+"/scheme.sch", 'w')
		for line in self.file :
			f.write(line+'\n')
		f.close()
		return


	@typechecked
	def add_one_part(self, index:int, name : str, value: str, deviceset: str ='TESPOINT', device: str='-SMD1.5MM', library: str='Generics_stg', package3d_urn="urn:adsk.eagle:package:19402626/2")-> None:
		"""
		Add one part to the file

		Parameters
		-----------------------
		index: int
			characteristic of a testpoint
		name: str
			characteristic of a testpoint
		value :str
			characteristic of a testpoint
		deviceset : str
			characteristic of a testpoint
		device: str
			characteristic of a testpoint
		library: str
			characteristic of a testpoint
		package3d_urn: str
			characteristic of a testpoint
		"""
		self.file.insert(index, '<part name="%s" library="%s" deviceset="%s" device="%s" package3d_urn="%s" value="%s"/>' %(name, library, deviceset, device, package3d_urn, value))
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
	def add_one_instance(self, index: int, name: str, part: str, x:float, y: float, smashed: str ='yes', gate : str = 'TP1', size: str ='2.54', layer: str='95', font: str='vector')-> None:
		"""
		Add one instance to the file

		Parameters
		------------------------------
		index: int
			characteritic of a testpoint
		name: str
			characteritic of a testpoint
		part: str
			characteritic of a testpoint
		x: float
			characteritic of a testpoint
		y: float
			characteritic of a testpoint
		smashed : str
			characteritic of a testpoint
		gate: str
			characteritic of a testpoint
		size: str
			characteritic of a testpoint
		lauer: str
			characteritic of a testpoint
		font: str
			characteritic of a testpoint
		"""
		self.file.insert(index,'<instance part="%s" gate="%s" x="%f" y="%f" smashed="%s">' % (part,gate,x,y,smashed))
		self.file.insert(index+1,'<attribute name="%s" x="%f" y="%f" size="%s" layer="%s" font="%s"/>' % (name,x,y,size,layer,font))
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
			self.add_one_instance(close_instances , df['signal_name'][i], df['signal_name'][i], df['y'][i], df['x'][i])
			close_instances +=3
		return



class DefaultBRD:

	"""
	A default .sch file that can be automatically modified and written

	Attributes
	-------------------

	Methods
	------------------
	__init__
	write_file
	add_rectangular_board
	add_one_element
	add_all_elements
	add_one_signal
	add_all_signals

	
	"""

	@typechecked
	def __init__(self, file_path: str= './eagle_default/default.brd')-> None:
		"""
		Initializes the class by reading a default brd file and storing it in a list

		Parameters
		----------------------
		file_path : str
			Default = './eagle_default/default.brd'
			The path of the default file that will modified
		"""
		f = open(file_path,'r')
		self.file = f.read().splitlines()
		f.close()
		return


	@typechecked
	def write_file(self, path)-> None:
		"""
		Write the new file in the folder specified in parameters

		Parameters
		-------------
		path : str
			the folder where the user wants to save the file
		"""
		f = open(path+"/board.brd", 'w')
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
			 specified the size of the new pcb
		y0 :float
			 specified the size of the new pcb
		x1 :float
			 specified the size of the new pcb
		y1 :float
			 specified the size of the new pcb
		"""
		close_board = self.file.index('</plain>')
		self.file.insert(close_board,'<wire x1="%d" y1="%d" x2="%d" y2="%d" width="0" layer="20"/>' % (x0, y0, x0, y1))
		self.file.insert(close_board,'<wire x1="%d" y1="%d" x2="%d" y2="%d" width="0" layer="20"/>' % (x0, y0, x1, y0))
		self.file.insert(close_board,'<wire x1="%d" y1="%d" x2="%d" y2="%d" width="0" layer="20"/>' % (x1, y0, x1, y1))
		self.file.insert(close_board,'<wire x1="%d" y1="%d" x2="%d" y2="%d" width="0" layer="20"/>' % (x0, y1, x1, y1))
		return


	@typechecked
	def add_one_element(self , index: int, name: str, x:float, y:float, value: str, package: str, library: str = "Generics_stg", package3d_urn: str="urn:adsk.eagle:package:19402626/2", smashed: str="yes", size:float = 1 ,layer :int = 25, ratio: float= 16, align: str= 'center-left')-> None:
		"""
		Add one element to the file

		Parameters
		-------------------
		index:int
			Characteritic of a test point
		name :str
			Characteritic of a test point
		x:float
			Characteritic of a test point
		value:str
			Characteritic of a test point
		package: str
			Characteritic of a test point
		library: str
			Characteritic of a test point
		package3d_urn:str
			Characteritic of a test point
		smashed:str
			Characteritic of a test point
		soze:float
			Characteritic of a test point
		layer:int
			Characteritic of a test point
		ratio:float
			Characteritic of a test point
		align:str
			Characteritic of a test point
		"""
		self.file.insert(index,'<element name="%s" library="%s" package="%s" package3d_urn="%s" value="%s" x="%s" y="%s" smashed="%s">' % (name,library,package,package3d_urn,value,x,y,smashed))
		self.file.insert(index+1,'<attribute name="%s" x="%f" y="%f" size="%f" layer="%d" ratio="%f" align="%s"/>' % (name,x,y,size,layer,ratio,align))
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
		
		"""

		self.file.insert(index,'<signal name="%s">' % name)
		self.file.insert(index+1,'<contactref element="%s" pad="%s"/>' % (name,pad))
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
		the path where to create the file
	"""
	brd_file= DefaultBRD()
	brd_file.add_rectangular_board(dimension.xmin, dimension.ymin, dimension.xmax, dimension.ymax)
	brd_file.add_all_elements(folder.final_tp_names_top_df)
	brd_file.add_all_elements(folder.final_tp_names_bot_df)
	brd_file.add_all_signals(folder.final_tp_names_top_df)
	brd_file.add_all_signals(folder.final_tp_names_bot_df)
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
		the path where to create the file
	"""
	sch_file = DefaultSCH()
	sch_file.add_all_instances(folder.final_tp_names_top_df)
	sch_file.add_all_instances(folder.final_tp_names_bot_df)
	sch_file.add_all_parts(folder.final_tp_names_bot_df)
	sch_file.add_all_parts(folder.final_tp_names_top_df)
	sch_file.write_file(path)
	return






