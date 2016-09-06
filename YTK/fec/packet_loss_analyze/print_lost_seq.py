#! /usr/bin/python

import sys
import os
import optparse
import subprocess

MAX_JITTER = 20 # when finding a wrap, drop the next (2 * MAX_JITTER) seq numbers to avoid two seq interleaved.
               # see example in af520505_all-stat/highq-statistics/2515530.dump line 54005~54032
MIN_SEQ_JUMP_WHEN_RECONNECT = 100

def ParseCmdline():   
    parser = optparse.OptionParser(__doc__)
    parser.add_option("-f", "--file", dest="file", metavar="NAME", action="store", default="",
                      help='File name.')
    parser.add_option("-d", "--dir", dest="dir", metavar="NAME", action="store", default="",
                      help='Dir name.')
    options, args = parser.parse_args()
    return options
    
def GetFileLines(filename):
    str_stdout = subprocess.check_output("wc -l " + filename, shell=True)
    return int(str_stdout.strip().split()[0])

def AnalyzeOneSortedNoWrapFile(filename, destfile):
    if not os.path.exists(filename):
        print "ERROR: ", filename, "does not exist!"
        return
    rec_num = 0
    lost_num = 0
    with open(destfile, 'w') as fout:
        last_seq = -1
        last_lost_seq = -1
        line_num = 0
        print >> fout, "LostSeq,  LostInterval"
        with open(filename, 'r') as f:
            for line in f:
                #print line
                line_num = line_num + 1
                cur_seq = int(line.strip())
                #print cur_seq
                if(last_seq < 0):
                    rec_num += 1
                if(last_seq >= 0 and cur_seq - last_seq < 0):
                    print >> fout,  "ERROR(line " + str(line_num) + \
                      "): it seems the file is not sorted, or it's wrapped around."
                    assert(False)
                    return
                elif(last_seq >= 0 and cur_seq - last_seq == 0):
                    pass
                    #print "WARNING(line:" + str(line_num) + "): two identical seq."
                elif(last_seq >= 0 and cur_seq - last_seq == 1):
                    rec_num += 1
                elif(last_seq >= 0 and cur_seq - last_seq >= 2):
                    rec_num += 1
                    lost_num += cur_seq - last_seq - 1
                    if cur_seq - last_seq == 2:  # lost one packet
                        print >> fout, last_seq + 1, (last_seq + 1) - last_lost_seq - 1
                    elif cur_seq - last_seq > 2: # lost >1 continous packets, the LostInterval is <=0
                        print >> fout, last_seq + 1, -(cur_seq - last_seq - 1)
                    else:
                        assert(False)
                    last_lost_seq = cur_seq - 1
                last_seq = cur_seq
    #print filename, rec_num, lost_num
    return rec_num, lost_num

def SplitOneFileToSortedFilesWhenSeqJump(filename):
    if not os.path.exists(filename):
        print "ERROR: ", filename, "does not exist!"
        return
    last_seq = -1
    split_lines = []
    line_num = 0
    packets_to_drop_after_wrapping = 0
    start_line = 1
    with open(filename, 'r') as f:
        for line in f:
            line_num = line_num + 1
            if packets_to_drop_after_wrapping > 0:
                packets_to_drop_after_wrapping -= 1
                continue
            cur_seq = int(line.strip())
            if(last_seq >=0 and abs(cur_seq - last_seq) > MIN_SEQ_JUMP_WHEN_RECONNECT):
                packets_to_drop_after_wrapping = 2 * MAX_JITTER
                split_lines.append((start_line, line_num - 1))
                start_line = line_num + packets_to_drop_after_wrapping + 1
                last_seq = -1
                continue
            last_seq = cur_seq
    if(line_num - start_line > MAX_JITTER):
        split_lines.append((start_line, line_num))
    #print split_lines
    splited_files = []
    #if(line_num < 100):
    #    return splited_files
    for i in range(len(split_lines)):
        start_line = split_lines[i][0]
        end_line = split_lines[i][1]
        #split_file = os.path.join(
        #  "output", 
        #  os.path.basename(filename) + ".split" + str(i) + "." + str(start_line) + "-" + str(end_line)
        #  )
        split_file = filename + ".split" + str(i) + "." + str(start_line) + "-" + str(end_line)
        os.system( \
          "head -n " + str(end_line) + " " + filename + " | " + \
          "tail -n " + str(end_line - start_line + 1) + " | " + \
          "sort -n > " + split_file \
          )
        splited_files.append(split_file)
        start_line = split_lines[i]
    #print splited_files
    return splited_files
    
def AnalyzeOneOrigalFile(filename):
    if not os.path.exists(filename):
        print "ERROR: ", filename, "does not exist!"
        return
    splited_files = SplitOneFileToSortedFilesWhenSeqJump(filename)
    rec_packets = 0
    lost_packets = 0
    for file in splited_files:
        packet_lost_file = file + ".packestlost"
        recv, lost = AnalyzeOneSortedNoWrapFile(file, packet_lost_file)
        print file + ", " + \
              str(recv) + ",  " + \
              str(lost) + ",  " + \
              str(lost * 100.0 / (recv + lost + 0.5))
    return

def AnalyzeOneDir(dir):
    if not os.path.exists(dir):
        print "ERROR: ", dir, "does not exist!"
        return
    for root, dirs, files in os.walk(dir):
        for f in files:
            #print os.path.join(root, f)
            filename = os.path.join(root, f)
            AnalyzeOneOrigalFile(filename)

if __name__ == '__main__':
    option = ParseCmdline()
    print "filename       ,  rec_packets,  lost_packets,  lost_rate(%)"
    if os.path.exists(option.file):
        AnalyzeOneOrigalFile(option.file)
    else:
        AnalyzeOneDir(option.dir)
