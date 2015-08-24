# xjs.xjtu@gmail.com
# 2015.02.14
# Issues:
#   1. If assert in included inside the API implementation, how should I write the unittest ??
from drawing import Drawing

# class ActionEnum(object):
#     pen_style   = -10   # select pen style
#     pen_down    = 0     # start to draw
#     pen_up      = 10    # end drawing
#     line_up     = 20    # <==> north
#     line_down   = 30    # <==> south
#     line_left   = 40    # <==> west
#     line_right  = 50    # <==> east


class Parse(object):
    def __init__(self):
        self._pen_style_list = ['b-', 'r-o', 'g-*']
        self._draw = Drawing()
        pass
    
    def get_cur_x(self):
        return self._draw.get_cur_x()
    def get_cur_y(self):
        return self._draw.get_cur_y()
    def get_style(self):
        return self._draw.get_stype()
    def get_status(self):
        return self._draw.get_status()
    def show(self):
        return self._draw.show()
    
    def parse_one_line(self, line):
        line2 = line = line.strip()
        if line.find('#') != -1:
            line2 = line[0:line.find('#')]   # remove comments
        words = line2.split()
        if len(words) == 0:
            return
        
        if words[0] == 'P':
            assert(len(words) == 2)
            self._draw.set_style(self._pen_style_list[int(words[1])])
        elif words[0] == 'D':
            assert(len(words) == 1)
            self._draw.pen_down()
        elif words[0] == 'U':
            assert(len(words) == 1)
            self._draw.pen_up()
        elif words[0] == 'W':
            assert(len(words) == 2)
            self._draw.line_left(int(words[1]))
        elif words[0] == 'N':
            assert(len(words) == 2)
            self._draw.line_up(int(words[1]))
        elif words[0] == 'E':
            assert(len(words) == 2)
            self._draw.line_right(int(words[1]))
        elif words[0] == 'S':
            assert(len(words) == 2)
            self._draw.line_down(int(words[1]))
        else:
            print "Error: Un-supported Action!, in line \"" + line + "\""
            assert(1)
     
def test_null():
    p = Parse()
    oldx = p.get_cur_x()
    oldy = p.get_cur_y()
    t = p.parse_one_line("")
    assert((oldx == p.get_cur_x()) and (oldy == p.get_cur_y()))

def test_comment():
    p = Parse()
    oldx = p.get_cur_x()
    oldy = p.get_cur_y()
    t = p.parse_one_line("# This is test.")
    assert(oldx == p.get_cur_x() and oldy == p.get_cur_y())

def test_P():
    p = Parse()
    t = p.parse_one_line("P 2")
    assert(p.get_style() == p._pen_style_list[2])

def test_P_with_comment():
    p = Parse()
    t = p.parse_one_line("P 2 # this is comment")
    assert(p.get_style() == p._pen_style_list[2])
   
def test_D():
    p = Parse()
    t = p.parse_one_line("D ")
    assert(0 == p.get_cur_x() and 0 == p.get_cur_y() and 1 == p.get_status())

def test_U():
    p = Parse()
    t = p.parse_one_line("U")
    assert(0 == p.get_status())

def test_W():
    p = Parse()
    oldx = p.get_cur_x()
    oldy = p.get_cur_y()
    t = p.parse_one_line("W 2")
    assert(oldx -2 == p.get_cur_x() and oldy == p.get_cur_y())

def test_E():
    p = Parse()
    oldx = p.get_cur_x()
    oldy = p.get_cur_y()
    t = p.parse_one_line("E 2")
    assert(oldx + 2 == p.get_cur_x() and oldy == p.get_cur_y())

def test_N():
    p = Parse()
    oldx = p.get_cur_x()
    oldy = p.get_cur_y()
    t = p.parse_one_line("N 2")
    assert(oldx == p.get_cur_x() and oldy + 2 == p.get_cur_y())

def test_S():
    p = Parse()
    oldx = p.get_cur_x()
    oldy = p.get_cur_y()
    t = p.parse_one_line("S 2")
    assert(oldx == p.get_cur_x() and oldy -2 == p.get_cur_y())

if __name__ == "__main__":
    p = Parse()
    f = open("test.actions")
    try:
        for line in f:
            p.parse_one_line(line)
        p.show()
    except:
        assert(1)
    finally:
        f.close()

