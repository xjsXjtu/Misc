# xjs.xjtu@gmail.com
# 2015.02.14
# Issues:
#   None
from the_parser import Parse

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



