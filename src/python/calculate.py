import math
import collections
import re
def make_word_id_and_idf_dict():
    word_id_dict = {}
    word_idf_dict = {}
    src = './wiki_idf_dict.txt'
    with open(src, 'r') as f:
        w_id = 0
        for line in f:
            items = line.strip().decode('utf-8').split('\t')
            if len(items) != 2:
                continue
            word_id_dict[items[0]] = w_id
            w_id += 1
            word_idf_dict[items[0]] = int(items[1])
    return word_id_dict, word_idf_dict

def make_article_id_dict():
    article_id_dict = {}
    src = './title_map.txt'
    with open(src, 'r') as f:
        a_id = 0
        for line in f:
            line = line.strip().decode('utf-8')
            article_id_dict[line] = a_id
            a_id += 1
    return article_id_dict

def make_tfidf_matrix():
    word_topic_distr_dict = collections.defaultdict(dict)
    word_id_dict, word_idf_dict = make_word_id_and_idf_dict()
    with open('./word_id_dict.txt', 'w') as f:
        for w, id in word_id_dict.iteritems():
            f.write('%s\t%s\n' % (w.encode('utf-8'), id))
    article_id_dict = make_article_id_dict()
    for k, v in word_idf_dict.iteritems():
        idf = math.log(len(article_id_dict) / (word_idf_dict.get(k, 0.0) + 1.0), 10)
        word_idf_dict[k] = idf

    src = 'seg_wiki_doc.txt'
    pattern = re.compile('#Article: (.+)#Type: regular article(.+)')
    dst = 'tfidf_matrix.txt'
    with open(src, 'r') as f, open(dst, 'w') as fd:
        doc_id = 0
        for line in f:
            line = line.strip().decode('utf-8')
            m = pattern.match(line)
            word_list = []
            if m:
                word_list = m.group(2).split(' ')
            else:
                print 'doc_id: %s not correct format' % doc_id
                continue

            tf_dict = {}
            tfidf_dict = {}
            for w in word_list:
                if len(w) == 0:
                    continue
                tf_dict[w] = tf_dict.get(w, 0.0) + 1.0
            for w in tf_dict:
                if w not in word_id_dict or w not in word_idf_dict:
                    print '%s not in word_id_dict or word_idf_dict' % w.encode('utf-8')
                    continue
                w_id = word_id_dict[w]
                idf = word_idf_dict[w]
                tf = tf_dict[w] / len(tf_dict)

                tfidf_dict[w_id] = tf * idf

            strlist = ['%s:%s' % (w_id, tfidf) for w_id, tfidf in tfidf_dict.items()]
            fd.write('%s\n' % ('\t'.join(strlist).encode('utf-8')))
                
if __name__ == '__main__':
    make_tfidf_matrix()
    print 'over'

