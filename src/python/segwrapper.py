#-*-coding:gbk-*-

import pynlpir

def open(encoding='gbk'):
    return pynlpir.open(encoding=encoding)

def close():
    return pynlpir.close()

def cut(s):
    for w, pos in pynlpir.segment(s):
        yield w
		
def poscut(s):
    for w, pos in pynlpir.segment(s):
        yield w, pos

def extract_tags(s, topK=5, weighted=False):
    return pynlpir.get_key_words(s, topK, weighted)
	

def add_word(w):
    pynlpir.nlpir.AddUserWord(w)

def del_word(w):
    pynlpir.nlpir.DelUsrWord(w)
