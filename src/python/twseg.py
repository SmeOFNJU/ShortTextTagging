# -*- coding: gbk -*-

import segwrapper
import math
from collections import deque
import copy

segwrapper.open()

def n_gram(c='', n=2):
    words = pseg.cut(c)
    cnt = 0
    res = {}
    n_res = {}
    pos_res = {}
    wind = deque([])
    wind_pos = deque([])

    left = None
    right = None
    left_ie = {}
    right_ie = {}
    for word, flag in words:
        cnt += 1
        res[word] = res.get(word, 0) + 1
        if len(wind) < n:
            wind.append(word)
            wind_pos.append(flag[0])
        else:
            wp = ''.join(wind_pos)
            key = tuple(wind)
            pos_res[key] = wp
            n_res[key] = n_res.get(key, 0) + 1

            if left is None:
                left = copy.deepcopy(key[0])
            else:
                if key in left_ie:
                    left_ie[key][left] = left_ie[key].get(left, 0) + 1
                else:
                    left_ie[key] = {left:1}
                left = copy.deepcopy(key[0])

            wind.popleft()
            wind_pos.popleft()

            right = copy.deepcopy(word)
            if key in right_ie:
                right_ie[key][right] = right_ie[key].get(right, 0) + 1
            else:
                right_ie[key] = {right:1}

            wind.append(word)
            wind_pos.append(flag[0])
        
    wp = ''.join(wind_pos)
    key = tuple(wind)
    pos_res[key] = wp
    n_res[key] = n_res.get(key, 0) + 1
    
    return cnt, res, n_res, pos_res, left_ie, right_ie


def new_word_get(c='', pos=[], mi_limit=0, entropy_limit=0):
    cnt, res, n_res, pos_res, left_ie, right_ie = n_gram(c)
    mi = {}
    
    pos = set(pos)
    for k, v in n_res.iteritems():
        if pos_res[k] in pos:
            xy = float(v) / cnt
            x = float(res[k[0]]) / cnt
            y = float(res[k[1]]) / cnt
            mi_value = math.log( xy / (x * y), 2)
            if mi_value >= mi_limit:
                mi[k] = mi_value
    

    left_res = {}
    right_res = {}
    for k, v in left_ie.iteritems():
        if k in mi:
            s = 0
            for i, j in v.iteritems():
                s += j
            r = 0.0
            for i, j in v.iteritems():
                p = float(j) / s
                r += -1 * p * math.log(p, 2)
            if r >= entropy_limit:
                left_res[k] = r
    
    for k, v in right_ie.iteritems():
        if k in mi and k in left_res:
            s = 0
            for i, j in v.iteritems():
                s += j
            r = 0.0
            for i, j in v.iteritems():
                p = float(j) / s
                r += -1 * p * math.log(p, 2)
            if r >= entropy_limit:
                right_res[k] = r
    

    new_words = [''.join(i) for i in right_res.keys()]
    return new_words
            

def cut_again(c='', new_words=[]):
    for w in new_words:
        segwrapper.add_word(w)
    return segwrapper.cut(c)

def add_word(new_words):
    for w in new_words:
        segwrapper.add_word(w)

def del_word(new_words):
    for w in new_words:
        segwrapper.del_word(w)


def extract_again(c='', new_words=[], topK=5):
    for w in new_words:
        pass
    return segwrapper.extract_tags(c, topK=topK)


clses = ['电影', '法律', '交通', '生物', '食物', '体育', '文学', '音乐', '游戏', '政治', '宗教']
allow = ('n','ng','nr ', 'nr1', 'nr2', 'nrj', 'nrf', 'ns', 'nsf', 'nt', 'nz', 'nl', 'ng', 's', 'v', 'vn', 'an', 'b', 'bl', 'z' )

mi = [0]
en = [0]

def handle():
    precision = []
    recall = []
    for clss in clses:
        src = 'E:\data\extracted\extracted\\tags_question_content_answer_200\%s.file' % clss
        with open(src, 'r') as f:
            for line in f:
                items = line.strip().decode('gbk').split('\t')
                if len(items) < 4:
                    continue
                tags = items[0].split('||')
                if len(tags) < 3:
                    continue
                question = items[1]
                

                c = '%s %s %s' % (question, items[2], items[3])
                mi_limit = mi[0]
                entropy_limit = en[0]
                new_words = new_word_get(c, ['nn','nv','vn', 'ne', 'en'], mi_limit, entropy_limit)
                k = 5

                add_word(new_words)

                res = segwrapper.extract_tags(question, topK=k)
 
                #res = extract_again(question, new_words, k)

                del_word(new_words)

                cor = len(set(res) & set(tags))
                if len(res) == 0 or len(tags) == 0:
                    continue
                pre = float(cor) / len(tags)
                rec = float(cor) / k

                precision.append(pre)
                recall.append(rec)
    return precision, recall

def main():
    precision, recall = handle()
    p = sum(precision) / len(precision)
    r = sum(recall) / len(recall)
    f = (2 * p * r) / (p + r)
    #print 'precision: %s' % (p)
    #print 'recall: %s' % (r)
    print 'f-measure: %s' % ( (2 * p * r) / (p + r) )
    return f

res = []
for e in [0.2, 0.4, 0.6, 0.8, 1.0]:
    temp = []
    en[0] = e
    for m in [4.2, 4.3, 4.4, 4.5, 4.6]:
        mi[0] = m
        temp.append(main())
    print ' '.join(str(temp))
    #res.append(temp)

segwrapper.close()






