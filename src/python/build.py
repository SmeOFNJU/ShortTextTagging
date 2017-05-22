import json
import collections
part0 = 'tfidf_matrix.part0'
part1 = 'tfidf_matrix.part1'

def part():
    src = 'tfidf_matrix.txt'

    with open(src, 'r') as inf, \
         open(part0, 'w') as outf, \
         open(part1, 'w') as outf1:

        cnt = 0
        for line in inf:
            if cnt <= 100000:
                outf.write(line)
            else:
                outf1.write(line)
            cnt += 1

def cal(part_num):
    src = 'cn_word_id_dict.txt'
    word_id_dict = {}
    with open(src, 'r') as inf:
        for line in inf:
            line = line.strip().decode('utf-8')
            items = line.split('\t')
            if len(items) != 2:
                print 'not correct format'
                continue
            word_id_dict[items[0]] = int(items[1])

    tfidf_matrix = []
    with open('tfidf_matrix.%s'% part_num, 'r') as inf:
        for line in inf:
            line = line.strip().decode('utf-8')
            items = line.split('\t')
            word_tfidf_dict = {}
            for item in items:
                w_id_tfidf = item.split(':')
                if len(w_id_tfidf) != 2:
                    print 'not correct format word'
                    continue
                w_id = int(w_id_tfidf[0])
                tfidf = float(w_id_tfidf[1])
                word_tfidf_dict[w_id] = tfidf
            tfidf_matrix.append(word_tfidf_dict)

    with open('word_topic_distribution.%s' % part_num, 'w') as outf:
        for w, w_id in word_id_dict.iteritems():
            doc_id = 100001
            doc_tfidf_dict = {}
            for word_tfidf_dict in tfidf_matrix:
                if w_id in word_tfidf_dict:
                    doc_tfidf_dict[doc_id] = word_tfidf_dict[w_id]
                doc_id += 1

            outf.write(('%s\t%s\n' % (w, json.dumps(doc_tfidf_dict))).encode('utf-8'))

        print doc_id
                    
            
cal('part1')
print 'over'
