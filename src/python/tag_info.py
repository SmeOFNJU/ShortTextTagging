# -*- coding: gbk -*-
import os
import json
import sys

clses = ['电影', '法律', '交通', '生物', '食物', '体育', '文学', '音乐', '游戏', '政治', '宗教']
tag_set = set([])
info_dict = {}
count = 0

def handle_one(clss, file_path, file_name):

    global count
    with open(file_path, 'r') as inf:
        for line in inf:
            try:
                line = line.strip().decode('gbk')
                d = json.loads(line)
                subd = json.loads(d['answer'])
                answers = subd['answerlist']
                tags = subd['taglist']
                tagstr = '|'.join(tags)
                if len(answers) < 10:
                    continue
                answers = answers[:5]
                ansstr = '\t'.join(answers)
                try:
                    
                    qas = '%s\t%s' % (d['question'].encode('gbk'), ansstr.encode('gbk'))
                    q = '%s' % d['question'].encode('gbk')
                    qas = qas.replace('\n', ' ')
                    q = q.replace('\n', ' ')
                    if len(qas) > 5000 and len(q) > 40 and len(tags) > 4:

                        for t in tags:
                            tag_set.add(t)
                        
                        count += 1
                        if count >= 200:
                            return True
                    
                    
                except:
                    print sys.exc_info()
            except:
                continue
    return False


def write_set():
    dst = 'D:/BaiduYunDownload/extracted/simple/1000/tag_info/tag.file'
    min_size = 100
    max_size = 0
    avg_size = 0
    sum_size = 0
    with open(dst, 'w') as f:
        for t in tag_set:
            f.write('%s\n' % t.encode('gbk'))
            sum_size += len(t)
            min_size = min(len(t), min_size)
            max_size = max(len(t), max_size)
    avg_size = sum_size / len(tag_set)

    info_dict['min_size'] = min_size
    info_dict['max_size'] = max_size
    info_dict['avg_size'] = avg_size

def write_info():
    dst = 'D:/BaiduYunDownload/extracted/simple/1000/tag_info/info.file'
    with open(dst, 'w') as f:        
        f.write('min_size : %s\n' % (info_dict['min_size']))
        f.write('max_size : %s\n' % (info_dict['max_size']))
        f.write('avg_size : %s\n' % (info_dict['avg_size']))
        for t in tag_set:
            f.write('%s : %s\n' % (t.encode('gbk'), len(t)))

def write_dist():
    dst = 'D:/BaiduYunDownload/extracted/simple/1000/tag_info/distribute.file'
    dist_dict = {}
    
    for t in tag_set:
        dist_dict[len(t)] = dist_dict.get(len(t), 0) + 1
    with open(dst, 'w') as f:
        for k,v in dist_dict.iteritems():
            f.write('%s : %s\n' % (k, v))
        

for cls in clses:
    src_root = 'D:\BaiduYunDownload\extracted\extracted\%s' % cls
    for root, dirs, files in os.walk(src_root):
        count = 0
        for file_name in files:
            file_path = os.path.join(root, file_name)
            ret = handle_one(cls, file_path, file_name)
            if ret:
                break

write_set()
                    
write_info()

write_dist()
print 'over'
