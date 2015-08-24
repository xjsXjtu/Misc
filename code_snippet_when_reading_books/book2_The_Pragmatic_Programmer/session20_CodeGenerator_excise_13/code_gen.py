#!/usr/bin/python

import os
from lang_backend import LangC, LangJava, LangEnum
    
class Parser(object):
    def __init__(self, lang):
        self._lang = lang   # LangEnum
        if lang == LangEnum.c:
            self._be = LangC()
        elif lang == LangEnum.java:
            self._be = LangJava()
        else:
            print "Error: Not supported language"
            raise(1)
    
    def _remove_double_slash(self, line):
        p = line.find("//")
        if p == -1:
            return line
        else:
            return line[0:p]
    
    def parse_one_line(self, line):
        line = self._remove_double_slash(line.strip())
        if line == "":
            return ""
        tag = line[0]
        content = line[1:].strip()
        if tag == '#':
            return self._be.comment(content)
        elif tag == 'M':
            self._be.set_msg_name(content)
            return self._be.start()
        elif tag == 'F':
            words = content.split()
            name = words[0]
            type = words[1]
            return self._be.field(name, type)
        elif tag == 'E':
            return self._be.end()
        else:
            print "Error: Not support tag of \" " + tag + " \""
            raise(1)
    
    def parse_file(self, filename):
        f = open(filename)
        for line in f:
            out = self.parse_one_line(line)
            if out:
                print out

def test_oneline_comment1():
    p = Parser(LangEnum.c)
    assert p.parse_one_line("# comments") == "/* comments */"

def test_oneline_comment2():
    p = Parser(LangEnum.c)
    assert p.parse_one_line("// comments") == ""

def test_oneline_start():
    p = Parser(LangEnum.c)
    assert p.parse_one_line("M test_msg") == "typedef struct {"

def test_oneline_field_primitive():
    p = Parser(LangEnum.c)
    assert p.parse_one_line("F a int") == "    int\t\ta;"

def test_oneline_field_array():
    p = Parser(LangEnum.c)
    assert p.parse_one_line("F b int[4][8]") == "    int\t\tb[4][8];"

def test_oneline_end():
    p = Parser(LangEnum.c)
    p.parse_one_line("M test_msg")
    assert p.parse_one_line("E") == "} test_msg;"

if __name__ == "__main__":
    p = Parser(LangEnum.c)
    p.parse_file("test_input.txt")
    
    
    
    