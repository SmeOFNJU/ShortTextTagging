# -*- coding: gbk -*-
import os
import json
import sys
from multiprocessing import Process

def make_stopword_set():
    stopword_file = 'D:/百度云同步盘/program/Segment/Segment/result/script/stopword3.txt'
    with open(stopword_file, 'r') as f:
        for line in f:
            line = line.strip().decode('gbk')
            stopword_set.add(line)

    stopword_file = 'D:/百度云同步盘/program/Segment/Segment/result/script/stopword1.txt'
    with open(stopword_file, 'r') as f:
        for line in f:
            line = line.strip().decode('gbk')
            stopword_set.add(line)

    stopword_file = 'D:/百度云同步盘/program/Segment/Segment/result/script/stopword2.txt'
    with open(stopword_file, 'r') as f:
        for line in f:
            line = line.strip().decode('utf-8')
            stopword_set.add(line)

def write_stopword_set():
    stopword_file = 'D:/百度云同步盘/program/Segment/Segment/result/script/stopword.txt'
    with open(stopword_file, 'w') as f:
        for k in stopword_set:
            f.write('%s\n' % k.encode('gbk'))
        

def handle_one(clss, file_path, stopword_set):
    dst_root = 'D:/BaiduYunDownload/extracted/simple/1000/question_answer_seg_no_stop_word/%s' % clss
    with open(file_path, 'r') as inf, open('%s.file' % (dst_root), 'a') as outf:
        for line in inf:
            try:
                line = line.strip().decode('gbk')
                new_line = None
                wordtypes = line.split('\t')
                for wordtype in wordtypes:
                    wt = wordtype.split(':')
                    if len(wt) != 2:
                        continue
                    if wt[0] not in stopword_set:
                        if new_line is None:
                            new_line = wordtype
                        else:
                            new_line = '%s\t%s' % (new_line, wordtype)
                outf.write('%s\n' % (new_line.encode('gbk')))
            except:
                continue

def handle(clses, stopword_set):
    print clses
    for cls in clses:
        file_path = 'D:/BaiduYunDownload/extracted/simple/1000/question_answer_seg/%s.file' % cls
        handle_one(cls, file_path, stopword_set)

if __name__ == '__main__':
    clses = [['电影', '法律', '交通'], ['生物', '食物', '体育'], ['文学', '音乐', '游戏'], ['政治', '宗教']]
    global stopword_set
    stopword_set = set([])
    make_stopword_set()
    #write_stopword_set()
    proces = []
    for i in range(len(clses)):
        child_proc = Process(target=handle, args=(clses[i], stopword_set))
        child_proc.start()
        proces.append(child_proc)

    for p in proces:
        p.join()
    
    print 'over'
