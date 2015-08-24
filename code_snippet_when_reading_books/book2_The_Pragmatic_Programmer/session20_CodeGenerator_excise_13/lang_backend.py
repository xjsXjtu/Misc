#!/usr/bin/python


class LangEnum(object):
    c       = "C"
    java    = "J"
    
class LangBase(object):
	def __init__(self, msg_name=""):
		self._msg_name = msg_name
	
	def set_msg_name(self, msg_name):
		self._msg_name = msg_name
		
	def __raise_un_implement_error(self):
		print "Not implemented in the base class."
		raise(1)
	
	def comment(self, comments):
		self.__raise_un_implement_error()
	def start(self):
		self.__raise_un_implement_error()
	def field(self, name, type):
		self.__raise_un_implement_error()
	def end(self):
		self.__raise_un_implement_error()
	
class LangC(LangBase):
	def __init__(self, msg_name=""):
		LangBase.__init__(self, msg_name)
		
	def comment(self, comments):
		return '/* ' + comments + ' */'
		
	def start(self):
		return 'typedef struct {'
		
	def field(self, name, type):
		if '[' in type: 
			# array type
			p = type.find('[')
			return "    " + type[0:p] + "\t\t" + name + type[p:] + ';'
		else:
			# primitive type
			return '    ' + type + "\t\t" + name + ';'
		
	def end(self):
		return "} " + self._msg_name + ";"
	
class LangJava(LangBase):
	def __init__(self, msg_name = ""):
		LangBase.__raise_un_implement_error()
	
		
def test_langc_comment():
	lc = LangC("test_msg")
	assert lc.comment("comments") == "/* comments */"

def test_langc_start():
	lc = LangC("test_msg")
	assert lc.start() == "typedef struct {"
	
def test_langc_field_primitive():
	lc = LangC("test_msg")
	assert lc.field('a', 'int') == "    int\t\ta;"

def test_langc_field_array():
	lc = LangC("test_msg")
	assert lc.field('b', 'int[4][8]') == "    int\t\tb[4][8];"

def test_langc_end():
	lc = LangC("test_msg")
	assert lc.end() == "} test_msg;"
	
if __name__ == "__main__":
	lc = LangC("test_msg")
	print lc.comment("comments")
	print lc.start()
	print lc.field('a', 'int')
	print lc.field('b', 'int[4][8]')
	print lc.end()
	
	
	