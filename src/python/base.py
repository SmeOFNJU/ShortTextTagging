# -*- coding: gbk -*-

import math
from collections import deque
import copy
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


def pointwise_mutual_information_get(cnt=0, res={}, nres={}, pos_res={}, pos=[]):
    #cnt, res, nres, pos_res = n_gram_mi(c, 2)
    mi = {}
    
    for k, v in nres.iteritems():
        if pos_res[k] in set(pos):
            xy = float(v) / cnt
            x = float(res[k[0]]) / cnt
            y = float(res[k[1]]) / cnt
            mi_value = math.log( xy / (x * y), 2)
            mi[k] = mi_value
    return sorted(mi.items(), key=lambda x:x[1], reverse=True)

def information_entropy_get(pos_res={}, left_ie={}, right_ie={}, pos=[]):
    pos = set(pos)
    left_res = {}
    right_res = {}
    for k, v in left_ie.iteritems():
        if pos_res[k] in pos:
            s = 0
            for i, j in v.iteritems():
                s += j
            r = 0.0
            for i, j in v.iteritems():
                p = float(j) / s
                r += -1 * p * math.log(p, 2)
            left_res[k] = r
    
    for k, v in right_ie.iteritems():
        if pos_res[k] in pos:
            s = 0
            for i, j in v.iteritems():
                s += j
            r = 0.0
            for i, j in v.iteritems():
                p = float(j) / s
                r += -1 * p * math.log(p, 2)
            right_res[k] = r
    
    left = sorted(left_res.items(), key = lambda x:x[1], reverse=True)
    right = sorted(right_res.items(), key = lambda x:x[1], reverse=True)
    return left, right
            





