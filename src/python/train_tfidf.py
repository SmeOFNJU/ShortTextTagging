from gensim import corpora, models, similarities

def save_tags(file_name, tags):
    with open(file_name, 'w') as f:
        for line in tags:
            f.write('%s\n' % (line.encode('gbk')))

def load_tags(file_name):
    res = []
    with open(file_name, 'r') as f:
        for line in f:
            items = line.decode('gbk').strip().split("||")
            res.append(items)
    return res

def train(file_name):
    texts = []
    tags = []
    with open(file_name, 'r') as f:
        for line in f:
            items = line.decode('gbk').strip('\n').split('\t')
            if len(items) != 2:
                print line.decode('gbk')
                raise Exception("error")
            tags.append(items[0])
            texts.append(items[1].split(' '))
    dictionary = corpora.Dictionary(texts)
    dictionary.save('./temp_tfidf/temp_dict')
    save_tags('./temp_tfidf/tags', tags)

    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize('./temp_tfidf/temp_mm', corpus)
    tfidf = models.TfidfModel(corpus)
    tfidf.save('./temp_tfidf/tfidf_value')

train_txt = './data/training_data.txt'
train(train_txt)


            
