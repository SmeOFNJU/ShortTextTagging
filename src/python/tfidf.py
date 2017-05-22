# -*- coding: gbk -*-
import sys
import collections
from operator import itemgetter
import math
import os

class TFIDF(object):
    delim = '\t'
    def __init__(self):
        self.df= {}
        self.total_docs = 0.0

    def handle_doc(self, file_name):
        with open(file_name, 'r') as f:
            for line in f:
                self.total_docs += 1.0
                words = set(line.decode('gbk').strip().split(TFIDF.delim))
                for w in words:
                    self.df[w] = self.df.get(w, 0.0) + 1.0

    def extract_tags(self, words, topK=5, allowPOS=[]):
        if allowPOS:
            allowPOS = frozenset(allowPOS)
        
        tf = {}
        total_words = 0.0

        for w in words:
            items = w.split(':')
            if len(items) != 2:
                continue
            if len(allowPOS) != 0:
                if items[1] not in allowPOS:
                    continue
            total_words += 1.0
            tf[w] = tf.get(w, 0.0) + 1.0
            
        for k in tf:
            idf = math.log(self.total_docs / (self.df.get(k, 0.0) + 1.0), 10)
            tf[k] = (tf[k] / total_words) * idf 


        tags = sorted(tf.items(), key=lambda x:x[1], reverse=True)

        if topK:
            return tags[:topK]
        else:
            return tags


def main():
    tfidf = TFIDF()
    file_dir = 'D:\\BaiduYunDownload\\extracted\\simple\\question_answer_seg_no_stop_word\\'
    out_dir = 'D:\\BaiduYunDownload\\extracted\\simple\\question_answer_tfidf\\'
    for root, dirs, files in os.walk(file_dir):
        for file_name in files:
            path = os.path.join(root, file_name)
            tfidf.handle_doc(path)

    for root, dirs, files in os.walk(file_dir):
        for file_name in files:
            path = os.path.join(root, file_name)
            out_path = os.path.join(out_dir, file_name)
            with open(path, 'r') as inf, open(out_path, 'w') as outf:
                for line in inf:
                    words = line.decode('gbk').strip().split('\t')
                    tags = tfidf.extract_tags(words, 5)
                    out = None
                    for tag, weight in tags:
                        if out is None:
                            out = '%s|%s' % (tag.encode('gbk'), weight)
                        else:
                            out += '\t%s|%s' % (tag.encode('gbk'), weight)
                    outf.write('%s\n' % out)
                

    
    
    
if __name__ == '__main__':
    main()
    print 'over'
