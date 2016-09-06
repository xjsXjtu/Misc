#! /usr/bin/python

import sys
import os
import optparse
import subprocess

def ParseCmdline():   
    parser = optparse.OptionParser(__doc__)
    parser.add_option("-i", "--in", dest="infile", metavar="NAME", action="store", default="",
                      help='Input file name, containing hex FEC mask table.')
    parser.add_option("-o", "--out", dest="outfile", metavar="NAME", action="store", default="",
                      help='Output file name, containing binary FEC mask table.')
    options, args = parser.parse_args()
    return options
  
def ConvertOneHexLine(line):
    if "0x" not in line:
        return line
    words = line.strip().strip(',').split(',')
    outline = "  "
    for w in words:
        if "0x" in w and int(w, 16) >= 0 and int(w, 16) <= 255:
            outline += "{0:08b}".format(int(w, 16)) + ", "
        else:
            outline += w + ", "
    return outline
  
def ConvertOneHexTableFile(srcfile, dstfile):
    if not os.path.exists(srcfile):
        print "ERROR: ", srcfile, "does not exist!"
        return
    with open(dstfile, 'w') as fout:
        print >> fout, "This file is generated automatically from ", srcfile
        with open(srcfile, 'r') as fin:
            for line in fin:
                #print line.strip()
                print >> fout, ConvertOneHexLine(line.strip())

if __name__ == '__main__':
    option = ParseCmdline()
    if not (option.infile and option.outfile):
        print "Usage: ./convert_table_to_binary.py -i infile -o outfile"
    elif not os.path.exists(option.infile):
        print "ERROR: Input file", option.infile, "does NOT exist!"
    elif os.path.exists(option.outfile):
        print "ERROR: Output file", option.outfile, "already exists!"        
    else:
        ConvertOneHexTableFile(option.infile, option.outfile)
