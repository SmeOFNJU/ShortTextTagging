import segwrapper
import heapq

segwrapper.open()

def stop_word(stop_word_file):
    stop_word_set = set([])
    with open(stop_word_file, 'r') as f:
        for line in f:
            line = line.decode('gbk').strip('\n')
            stop_word_set.add(line)
    return stop_word_set

def load_tags(tag_name):
    res = []
    with open(tag_name, 'r') as f:
        for line in f:
            items = line.decode('gbk').strip().split('||')
            res.append(items)
    return res

def load_word_map(word_map_file):
    word_map = {}
    with open(word_map_file, 'r') as f:
        for line in f:
            items = line.decode('gbk').strip().split(' ')
            if len(items) != 2:
                continue
            word_map[items[0]] = int(items[1])
    return word_map

def load_topic_doc(theta_file):
    topic_doc = []
    with open(theta_file, 'r') as f:
        for line in f:
            topic_doc.append([float(i) for i in line.decode('gbk').strip().split(' ')])
        return topic_doc

def load_word_topic(phi_file):
    word_topic = []
    with open(phi_file, 'r') as f:
        for line in f:
            word_topic.append([float(i) for i in line.decode('gbk').strip().split(' ')])
        return word_topic

stop_word_set = stop_word('../stopword.txt')
tags = load_tags('./result/tag_data.txt')
topic_doc = load_topic_doc('./result/model-final.theta')
word_topic = load_word_topic('./result/model-final.phi')
word_map = load_word_map('./result/wordmap.txt')


def sim(term, i):
    if term not in word_map:
        return 0.0
    topics = topic_doc[i]
    s = 0.0
    for j in xrange(len(topics)):
        s += word_topic[j][word_map[term]] * topics[i]
    return s

def handle():
    cnt = 0
    with open('./result/rank_tag.txt', 'w') as outf:
        for doc_tags in tags:
            res = []
            for tag in doc_tags:
                terms = segwrapper.cut(tag)
                s = 0.0
                c = 0
                for term in terms:
                    s += sim(term, cnt)
                    c += 1
                if c != 0:
                    s /= c
                else:
                    s = 0.0
                res.append('%s:%s' % (tag.encode('gbk'), s))
            outf.write('%s\n' % ('||'.join(res)))

handle()

segwrapper.close()
