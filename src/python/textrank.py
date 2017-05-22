# -*- coding: gbk -*-

import sys
import collections
from operator import itemgetter
import os

class UndirectWeightedGraph:
    d = 0.85

    def __init__(self):
        self.graph = collections.defaultdict(list)

    def addEdge(self, start, end, weight):
        # use a tuple (start, end,  ) instead of a Edge object
        self.graph[start].append((start, end, weight))
        self.graph[end].append((end, start, weight))

    def rank(self):
        ws = collections.defaultdict(float)
        outSum = collections.defaultdict(float)

        wsdef = 1.0 / (len(self.graph) or 1.0)
        for n, out in self.graph.items():
            ws[n] = wsdef
            outSum[n] = sum((e[2] for e in out), 0.0)

        # this line for build stable iteration
        sorted_keys = sorted(self.graph.keys())
        for x in xrange(10):  # 10 iters
            for n in sorted_keys:
                s = 0
                for e in self.graph[n]:
                    s += e[2] / outSum[e[1]] * ws[e[1]]
                ws[n] = (1 - self.d) + self.d * s

        (min_rank, max_rank) = (sys.float_info[0], sys.float_info[3])

        for w in ws.itervalues():
            if w < min_rank:
                min_rank = w
            elif w > max_rank:
                max_rank = w

        for n, w in ws.items():
            # to unify the weights, don't *100.
            ws[n] = (w - min_rank / 10.0) / (max_rank - min_rank / 10.0)

        return ws


def textrank(words, topK=5, allowPOS=[]):
    """
    words:[(word, flag)]
    """
    pos_filt = set(allowPOS)
    g = UndirectWeightedGraph()
    cm = collections.defaultdict(int)
    span = 7    

    for i in xrange(len(words)):
        if len(pos_filt) == 0 or words[i][1] in pos_filt:
            for j in xrange(i + 1, i + span):
                if j >= len(words):
                    break
                if len(pos_filt) > 0 and words[j][1] not in pos_filt:
                    continue
                cm[(words[i][0], words[j][0])] += 1

    for terms, w in cm.items():
        g.addEdge(terms[0], terms[1], w)
    nodes_rank = g.rank()

    tags = sorted(nodes_rank.items(), key=itemgetter(1), reverse=True)

    if topK:
        return tags[:topK]
    else:
        return tags


def main():
    file_dir = 'D:\\BaiduYunDownload\\extracted\\simple\\1000\\question_answer_seg_no_stop_word\\'
    out_dir = 'D:\\BaiduYunDownload\\extracted\\simple\\1000\\question_answer_textrank\\'

    for root, dirs, files in os.walk(file_dir):
        for file_name in files:
            path = os.path.join(root, file_name)
            out_path = os.path.join(out_dir, file_name)
            with open(path, 'r') as inf, open(out_path, 'w') as outf:
                for line in inf:
                    words = line.decode('gbk').strip().split('\t')
                    wordlist = [(w, 'ns') for w in words if len(w) > 1]
                    tags = textrank(wordlist, 10)
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
