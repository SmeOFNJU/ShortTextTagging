# -*- coding: gbk -*-
import segwrapper

stopword_set = set([])

def make_stopword_set():
    stopword_file = 'D:/百度云同步盘/program/Segment/Segment/result/script/stopword3.txt'
    with open(stopword_file, 'r') as f:
        for line in f:
            line = line.strip().decode('gbk')
            stopword_set.add(line)

    stopword_file = 'D:/百度云同步盘/program/Segment/Segment/result/script/stopword1.txt'
    with open(stopword_file, 'r') as f:
        for line in f:
            line = line.strip().decode('gbk')
            stopword_set.add(line)

    stopword_file = 'D:/百度云同步盘/program/Segment/Segment/result/script/stopword2.txt'
    with open(stopword_file, 'r') as f:
        for line in f:
            line = line.strip().decode('utf-8')
            stopword_set.add(line)

def seg():
    allowPOS = ('n','ng','nr ', 'nr1', 'nr2', 'nrj', 'nrf', 'ns', 'nsf', 'nt', 'nz', 'nl', 'ng', 's', 'v', 'vn', 'an', 'b', 'bl', 'z' )
    dst = 'D:/BaiduYunDownload/extracted/simple/1000/lda/jieba/qa/lda_qa.file'

    clses = ['电影', '法律', '交通', '生物', '食物', '体育', '文学', '音乐', '游戏', '政治', '宗教']
    allowPOS = frozenset(allowPOS)
    for cls in clses:
        file_path = 'D:/BaiduYunDownload/extracted/simple/1000/question_answer/%s.file' % cls
        with open(file_path, 'r') as inf, open(dst, 'a') as outf:
            for line in inf:
                line = line.strip().decode('gbk')

                words = segwrapper.poscut(line)
                remain = []
                for w in words:
                    if w.flag not in allowPOS:
                        continue

                    if len(w.word.strip()) < 2 or w.word.lower() in stopword_set:
                        continue

                    remain.append(w.word)

                outf.write('%s\n' % ' '.join(remain).encode('gbk'))

def main():
    make_stopword_set()
    seg()

if __name__ == '__main__':
	segwrapper.open()
    main()
	segwrapper.close()
    print 'over'

                    

                
                        
                
