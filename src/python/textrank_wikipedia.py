#-*-coding:gbk-*-
import nltk
import networkx as nx
import numpy as np
import segwrapper
import collections
import json
import math
import sys

clses = ['电影', '法律', '交通', '生物', '食物', '体育', '文学', '音乐', '游戏', '政治', '宗教']
#clses = ['宗教']
textrank_value = []

id_topic = collections.defaultdict(dict)

def make_dict():
    src = 'D:/BaiduYunDownload/extracted/simple/1000/wikipedia/word_topic_distribution.simple'
    with open(src, 'r') as f:
        for line in f:
            line = line.strip().decode('utf-8')
            items = line.split('\t')
            if len(items) != 2:
                print 'not correct format'
                continue
            word = items[0]
            topic = json.loads(items[1])
            id_topic[word] = topic
            
def cosin(topic1, topic2):
    dot = 0.0
    s1 = 0.0
    s2 = 0.0
    for doc, tfidf in topic1.iteritems():
        s1 += tfidf * tfidf
        if doc in topic2:
            dot += tfidf * topic2[doc]
    for doc, tfidf in topic2.iteritems():
        s2 += tfidf * tfidf
        
    return dot / math.sqrt(s1 * s2)
              
def build_graph(word_list):
    
    #print len(id_topic)
    word_list = [x for x in word_list if x in id_topic]
    s = list(set(word_list))
    word_id = {}
    id_word = {}
    num = len(s)
    for i in range(len(s)):
        word_id[s[i]] = i
        id_word[i] = s[i]
        
    graph = np.zeros((num, num))
    for i in range(len(word_list)):
        for j in range(len(word_list)):
            idi = word_id[word_list[i]]
            idj = word_id[word_list[j]]
            sim = 0
            if idi == idj:
                sim = 1
            elif word_list[idi] in id_topic and word_list[idj] in id_topic:
                sim = cosin(id_topic[word_list[idi]], id_topic[word_list[idj]])
            else:
                sim = 0        
            graph[idi][idj] = sim

    return (graph, id_word)

def textrank_by_wikipedia(s):
    allowPOS = ('n','ng','nr ', 'nr1', 'nr2', 'nrj', 'nrf', 'ns', 'nsf', 'nt', 'nz', 'nl', 'ng', 's', 'v', 'vn', 'an', 'b', 'bl', 'z' )
    allowPOS = frozenset(allowPOS)
    wt = segwrapper.poscut(s)
    word_flag_dict = {}
    word_list = []
    for w, f in wt:
        word_flag_dict[w] = f
        word_list.append(w)

    graph, id_word = build_graph(word_list)
    #print len(graph)
    #print graph
    nx_graph = nx.from_numpy_matrix(graph)
    scores = nx.pagerank(nx_graph, alpha=0.85)
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    recall = 5
    tags = sorted_scores
    ret = []

    for i, f in tags:
        if word_flag_dict[id_word[i]] in allowPOS and len(id_word[i]) > 1:
            ret.append((id_word[i], f))

    return ret[:recall]

def make_doc_id_tag_dict(clss):
    dst_root = 'D:/BaiduYunDownload/extracted/simple/1000/tags/%s.file' % clss
    doc_id_tag_dict = collections.defaultdict(list)
    with open(dst_root, 'r') as f:
        doc_id = 0
        for line in f:
            doc_id += 1
            items = line.strip().decode('gbk').split('|')
            doc_id_tag_dict[doc_id] = items

    return doc_id_tag_dict

def handle_one(clss, file_path):
    doc_id_tag_dict = make_doc_id_tag_dict(clss)

    dst_root = 'D:/BaiduYunDownload/extracted/simple/1000/textrank_wikipedia/%s' % clss
    recall = 5
    with open(file_path, 'r') as inf, open('%s.file' % (dst_root), 'w') as outf:
        doc_id = 0
        for line in inf:
            doc_id += 1
            line = line.strip().decode('gbk')

            s = line
            ret = textrank_by_wikipedia(s)
            textrank = [w for w, f in ret]
            
            tagset = set(doc_id_tag_dict[doc_id])

            textrank_right = len(tagset & set(textrank))
            
            textrank_value.append((float(textrank_right) / len(tagset), float(textrank_right) / recall))

            outf.write('%s\t%s\t%s\n' % (textrank_right, '|'.join(doc_id_tag_dict[doc_id]).encode('gbk'), '%'.join(textrank).encode('gbk')))

            #sys.exit(0)

def print_value():
    precise = 0.0
    recall = 0.0
    for k, v in textrank_value:
        precise += k
        recall += v
    print 'textrank precise: %s' % (precise / len(textrank_value))
    print 'textrank recall: %s' % (recall / len(textrank_value))

def main():
    make_dict()
    for cls in clses:
        src_root = 'D:/BaiduYunDownload/extracted/simple/1000/question/%s.file' % cls
        handle_one(cls, src_root)
    print_value()
        
if __name__ == '__main__':
    main()
 
