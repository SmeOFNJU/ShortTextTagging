from gensim import corpora, models, similarities
from gensim import matutils
import heapq

stop_word_set = set([])

def stop_word(file_name):
    with open(file_name) as f:
        for line in f:
            stop_word_set.add(line.decode('gbk'))
    stop_word_set.add(' ')
    stop_word_set.add('\t')
    stop_word_set.add('\n')
            

def load_tags(file_name):
    res = []
    with open(file_name, 'r') as f:
        for line in f:
            items = line.decode('gbk').strip()
            res.append(items)
    return res


def test(file_name):
    dictionary = corpora.Dictionary.load('./temp_tfidf/temp_dict')
    corpus = corpora.MmCorpus('./temp_tfidf/temp_mm')
    tfidf = models.TfidfModel.load('./temp_tfidf/tfidf_value')
    tags = load_tags('./temp_tfidf/tags')

    with open(file_name, 'r') as f, open('./result/tfidf_res', 'w') as outf:
        corpus_tfidf = tfidf[corpus]
        for line in f:
            items = line.decode('gbk').strip().split('\t')
            if len(items) != 2:
                raise Exception('error')
            qes = items[1].split(' ')
            new_vec = dictionary.doc2bow(qes)
            new_tfidf = tfidf[new_vec]
            h = []
            k = 10
            cnt = 0
            for dic in corpus_tfidf:
                s = matutils.cossim(new_tfidf, dic)
                heapq.heappush(h, (s, cnt))
                if len(h) > k:
                    heapq.heappop(h)
                cnt += 1
            candidate = '&&'.join(['%s:%s' % (tags[i], s) for (s, i) in h])
            outf.write('%s\t%s\n' % (items[0].encode('gbk'), candidate.encode('gbk')))

test('./data/test_data.txt')
