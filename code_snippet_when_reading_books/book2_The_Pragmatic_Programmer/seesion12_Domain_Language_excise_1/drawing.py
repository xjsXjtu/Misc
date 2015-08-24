# xjs.xjtu@gmail.com
# 2015.02.13
# Issues:
#	1. how to write unittest for the UI-like API, such as line_up() ??
#  	2. If assert in included inside the API implementation, how should I write the unittest ??

import matplotlib.pyplot as plt
	
class Drawing(object):
	"""
	define meta-actions, currently supports:
		pen down 	(x, y)	: start to draw at the position of "x, y"
		line up		(lengthgth)	: draw a line with lengthgth of "lengthgth" 
		line down	(lengthgth)	
		line left	(lengthgth)	
		line right	(lengthgth)	
	"""
	def __init__(self):
		self._status	= 1		# 0: pen up; 1: pen down
		self._style		= 'b-'
		self._cur_x		= 0
		self._cur_y		= 0
		self._xmin		= -1
		self._xmax		= 1
		self._ymin		= -1
		self._ymax		= 1
		pass
	def get_status(self):
		return self._status
	def get_stype(self):
		return self._style
	def get_cur_x(self):
		return self._cur_x
	def get_cur_y(self):
		return self._cur_y
		
	def pen_down(self, x=0, y=0):
		self._status	= 1
		self._cur_x 	= x
		self._cur_y 	= y
	
	def pen_up(self):
		self._status 	= 0
	
	def show(self):
		plt.axis([self._xmin, self._xmax, self._ymin, self._ymax])
		plt.show()
		
	def set_style(self, s):
		self._style 	= s
		
	def _update_bounder(self):
		self._xmax = max(self._xmax, self._cur_x + 1)
		self._xmin = min(self._xmin, self._cur_x - 1)
		self._ymax = max(self._ymax, self._cur_y + 1)
		self._ymin = min(self._ymin, self._cur_y - 1)
		
	def line_up(self, length):
		assert(self._status)
		plt.plot([self._cur_x, self._cur_x], 
				 [self._cur_y, self._cur_y + length],
				 self._style)
		self._cur_y += length
		self._update_bounder()
	
	def line_down(self, length):
		assert(self._status)
		plt.plot([self._cur_x, self._cur_x], 
				 [self._cur_y, self._cur_y - length],
				 self._style)
		self._cur_y -= length
		self._update_bounder()

	def line_left(self, length):
		assert(self._status)
		plt.plot([self._cur_x, self._cur_x - length], 
				 [self._cur_y, self._cur_y],
				 self._style)
		self._cur_x -= length
		self._update_bounder()
	
	def line_right(self, length):
		assert(self._status)
		plt.plot([self._cur_x, self._cur_x + length], 
				 [self._cur_y, self._cur_y],
				 self._style)
		self._cur_x += length
		self._update_bounder()


def test_pen_up():
	d = Drawing()
	d.pen_up()
	assert(d.get_status() == 0)

def test_pen_down0():
	d = Drawing()
	d.pen_down()
	assert(d.get_status() == 1)

def test_pen_down1():
	d = Drawing()
	d.pen_down(-1, -2)
	assert(d.get_status() == 1 and d.get_cur_x() == -1 and d.get_cur_y() == -2)

def test_line_up():
	d = Drawing()
	d.pen_down()
	d.line_up(1)
	assert(d.get_cur_x() == 0 and d.get_cur_y() == 1)

def test_line_down():
	d = Drawing()
	d.pen_down()
	d.line_down(1)
	assert(d.get_cur_x() == 0 and d.get_cur_y() == -1)

def test_line_left():
	d = Drawing()
	d.pen_down()
	d.line_left(1)
	assert(d.get_cur_x() == -1 and d.get_cur_y() == 0)

def test_line_right():
	d = Drawing()
	d.pen_down()
	d.line_right(1)
	assert(d.get_cur_x() == 1 and d.get_cur_y() == 0)
	
def test_rect():
	d = Drawing()
	d.pen_down()
	d.line_right(0.5)
	d.line_up(1)
	d.line_left(0.5)
	d.line_down(1)
	d.pen_up()
	d.show()
	assert(d.get_cur_x() == 0 and d.get_cur_y() == 0)
	
if __name__ == "__main__":
	test_rect()
	
	
			
		