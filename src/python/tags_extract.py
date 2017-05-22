# -*- coding: gbk -*-
import os
import json
import sys

clses = ['电影', '法律', '交通', '生物', '食物', '体育', '文学', '音乐', '游戏', '政治', '宗教']

def handle_one(clss, file_path, file_name):
    dst_root = 'D:\BaiduYunDownload\extracted\\tags\%s' % clss
    with open(file_path, 'r') as inf, open('%s.file' % (dst_root), 'a') as outf:
        for line in inf:
            try:
                line = line.strip('\n').strip().decode('gbk')
                d = json.loads(line)
                subd = json.loads(d['answer'])
                try:
                    outf.write('%s\n' % ('\n'.join(subd['taglist']).encode('gbk')))
                except:
                    print sys.exc_info()
            except:
                continue



for cls in clses:
    src_root = 'D:\BaiduYunDownload\extracted\extracted\%s' % cls
    for root, dirs, files in os.walk(src_root):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            handle_one(cls, file_path, file_name)


print 'over'
