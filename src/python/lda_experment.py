import collections
import sys
import math

word_id_dict = {}
word_topic_dict = collections.defaultdict(list)
doc_topic_dict = collections.defaultdict(list)
doc_tag_dict = collections.defaultdict(list)
topic_word_dict = collections.defaultdict(list)

precise_value = []
recall_value = []

num = 125

def make_word_id_dict():
    src = 'D:/BaiduYunDownload/extracted/simple/1000/lda/jieba/%s/wordmap.txt' % num
    with open(src, 'r') as f:
        for line in f:
            items = line.strip().decode('gbk').split(' ')
            if len(items) != 2:
                continue
            word_id_dict[items[0]] = int(items[1])


def make_word_topic_dict():
    src = 'D:/BaiduYunDownload/extracted/simple/1000/lda/jieba/%s/model-final.phi' % num
    with open(src, 'r') as f:
        for line in f:
            items = line.strip().split(' ')
            for i in range(len(items)):
                if i not in word_topic_dict:
                    word_topic_dict[i] = [float(items[i])]
                else:
                    word_topic_dict[i].append(float(items[i]))
    
    for k, v in word_topic_dict.iteritems():
        all = sum(v) + 50 * 0.1
        word_topic_dict[k] = [(x + 0.1) / all for x in v]


def make_topic_word_dict():
    src = 'D:/BaiduYunDownload/extracted/simple/1000/lda/jieba/%s/model-final.phi' % num
    with open(src, 'r') as f:
        topic_id = 0
        for line in f:
            items = line.strip().split(' ')
            items_dict = {}
            for i in range(len(items)):
                items_dict[i] = float(items[i])

            wd = sorted(items_dict.items(), key=lambda x: x[1], reverse = True)
            
            recall = 0
            wd = wd[:recall]
            topic_word_dict[topic_id] = [x for (x, y) in wd]

            topic_id += 1

def make_doc_topic_dict():
    src = 'D:/BaiduYunDownload/extracted/simple/1000/lda/jieba/%s/model-final.theta' % num
    doc_id = 0
    with open(src, 'r') as f:
        for line in f:
            doc_id += 1
            items = line.strip().split(' ')
            doc_topic_dict[doc_id] = [float(x) for x in items]

def make_doc_tag_dict():
    src = 'D:/BaiduYunDownload/extracted/simple/1000/lda/tags/tags.file'
    doc_id = 0
    with open(src, 'r') as f:
        for line in f:
            doc_id += 1
            items = line.strip().decode('gbk').split('|')
            doc_tag_dict[doc_id] = items
    
            
def cosine(list1, list2):
    
    if len(list1) != len(list2):
        raise Exception('two list length must be equal')
    
    dot = 0.0
    s1 = 0.0
    s2 = 0.0
    for i in range(len(list1)):
        dot += list1[i] * list2[i]
        s1 += list1[i] * list1[i]
        s2 += list2[i] * list2[i]

    if s1 == 0 or s2 == 0:
        raise Exception('vector length can not to be zero')
    
    return dot / (math.sqrt(s1 * s2))
    

def add_topic_word(doc_topic):
    m = 0
    index = -1
    for i in range(len(doc_topic)):
        if doc_topic[i] > m:
            m = doc_topic[i]
            index = i

    if index not in topic_word_dict:
        print '%s not in topic_word_dict' % index
        sys.exit(1)

    return topic_word_dict[index]
            
   
            
def main():
    
    src = 'D:/BaiduYunDownload/extracted/simple/1000/lda/jieba/qa/lda_qa.file'
    dst = 'D:/BaiduYunDownload/extracted/simple/1000/lda/tags/recom_tags.file'
    with open(src, 'r') as f, open(dst, 'w') as outf:
        doc_id = 0
        first = False
        for line in f:
            if first is False:
                first = True
                continue
            doc_id += 1
            
            doc_topic = doc_topic_dict[doc_id]
            words = line.strip().decode('gbk').split(' ')
            word_sim_dict = {}

            word_ids = []
            for word in words:
                if len(word) < 2:
                    continue
                if word not in word_id_dict:
                    print '%s not in word_id_dict' % word.encode('utf-8')
                    continue
                word_id = word_id_dict[word]
                if word_id not in word_topic_dict:
                    print '%s not in word_topic_dict' % word_id
                    continue
                word_topic = word_topic_dict[word_id]

                sim = cosine(doc_topic, word_topic)
                word_sim_dict[word] = sim

            add_words = add_topic_word(doc_topic)
            for word_id in add_words:
                if word_id not in word_topic_dict:
                    print '%s not in word_topic_dict' % word_id
                    continue
                word_topic = word_topic_dict[word_id]

                sim = cosine(doc_topic, word_topic)
                word_sim_dict[word] = sim
                
                
                
            keywords = doc_tag_dict[doc_id]


            
            recall = 5
            tagweights = sorted(word_sim_dict.items(), key=lambda x : x[1], reverse=True)
            tagweights = tagweights[:recall]
            tags = [x for (x, y) in tagweights]
      
            exact = float(len(set(keywords) & set(tags)))
            precise_value.append(exact / len(keywords))
            recall_value.append(exact / recall)

            outf.write('%s\t%s\t%s\n' % (exact, '|'.join(keywords).encode('gbk'), '%'.join(tags).encode('gbk')))

def print_value():
    print 'lda precise: %s' % (sum(precise_value) / len(precise_value))
    print 'lda recall: %s' % (sum(recall_value) / len(recall_value))
        
if __name__ == '__main__':
    print 'start'
    make_word_id_dict()
    make_word_topic_dict()
    make_doc_topic_dict()
    make_doc_tag_dict()
    make_topic_word_dict()
    main()
    print_value()
    print 'over'
