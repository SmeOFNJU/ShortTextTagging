# -*- coding: gbk -*-
import os
import json
import sys

def handle_one(clss, file_path):
    global old
    with open(file_path, 'r') as inf:
        for line in inf:
            line = line.strip('\n').strip().decode('gbk')
            stopword_set.add(line)
    print len(stopword_set) - old
    old = len(stopword_set)

def handle(clses):
    for cls in clses:
        file_path = 'Z:/thinkpad/program/Segment/result/tag/tags/tags/%s.file' % cls
        handle_one(cls, file_path)

def write_to():
    dst_root = 'Z:/thinkpad/program/Segment/result/tag/tag_uniq/uniq_tag'
    with open('%s.file' % (dst_root), 'w') as outf:
        for new_line in stopword_set:
            outf.write('%s\n' % (new_line.encode('gbk')))

if __name__ == '__main__':
    clses = ['电影', '法律', '交通', '生物', '食物', '体育', '文学', '音乐', '游戏', '政治', '宗教']
    global stopword_set
    global old
    old = 0
    stopword_set = set([])
    handle(clses)
    print len(stopword_set)
    write_to()
    print 'over'
