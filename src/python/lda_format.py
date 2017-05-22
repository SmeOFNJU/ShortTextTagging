# -*- coding: gbk -*-
import os
import json
import sys

dst_root = 'D:/BaiduYunDownload/extracted/simple/1000/lda/question/question.file'
dst_root = 'D:/BaiduYunDownload/extracted/simple/1000/lda/question_answer/question_answer.file'

def write_num():
    with open(dst_root, 'a') as outf:
        outf.write('11000\n')

def make_tag(clses):
    dst = 'D:/BaiduYunDownload/extracted/simple/1000/lda/tags/tags.file'
    with open(dst, 'w') as outf:
        for cls in clses:
            file_name = 'D:/BaiduYunDownload/extracted/simple/1000/tags/%s.file' % (cls)
            with open(file_name, 'r') as inf:
                for line in inf:
                    outf.write(line)

def handle_one(clss, file_path):
    with open(file_path, 'r') as inf, open(dst_root, 'a') as outf:
        
        for line in inf:
            line = line.strip().decode('gbk')
            wordtypes = line.split('\t')
            if len(wordtypes) == 0:
                continue
            new_line = None
            for wordtype in wordtypes:
                wt = wordtype.split(':')
                if len(wt) != 2:
                    continue
                if new_line is None:
                    new_line = wt[0]
                else:
                    new_line = '%s %s' % (new_line, wt[0])

            if new_line is not None:
                outf.write('%s\n' % new_line.encode('gbk'))
            else:
                outf.write('a\n')
                

def handle(clses):
    for cls in clses:
        file_path = 'D:/BaiduYunDownload/extracted/simple/1000/question_answer_with_tag_info/%s.file' % cls
        handle_one(cls, file_path)

if __name__ == '__main__':
    clses = ['电影', '法律', '交通', '生物', '食物', '体育', '文学', '音乐', '游戏', '政治', '宗教']

    #write_num()
    
    make_tag(clses)

    print 'over'



