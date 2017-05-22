#-*-coding:gbk-*-
import re
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

def make_doc():
    src = 'D:/BaiduYunDownload/wiki/articles_in_plain_text.txt'
    dst = './wiki_doc.txt'
    dst1 = './title_map.txt'
    pattern = re.compile('#Article:[\s]+(.+)')
    with open(src, 'r') as inf, open(dst, 'w') as outf,\
            open(dst1, 'w') as outf1:
        new_line = ''
        last_titile = ''
        title = ''
        for line in inf:
            line = line.strip().decode('utf-8')
            if len(line) == 0:
                continue
            m = pattern.match(line)
            if m:
                last_title = title
                title = m.group(1)
                if len(new_line) != 0:
                    try:
                        if len(new_line) > 200:
                            last_title.encode('gb2312')
                            outf.write('%s\n' % new_line.encode('utf-8'))
                    except:
                        pass
                new_line = '%s\t' % line
                continue
            new_line += line

        if len(new_line) != 0:
            new_line = new_line[len(('#Type: regular article')):]
            outf.write('%s\n' % new_line.encode('utf-8'))

def seg_wiki_doc():
    pattern = re.compile('#Article: (.+)#Type: regular article(.+)')
    make_stopword_set()
    src = './wiki_doc.txt'
    dst = './seg_wiki_doc.txt'
    with open(src, 'r') as inf, open(dst, 'w') as outf:
        for line in inf:
            line = line.strip().decode('utf-8')
            m = pattern.match(line)
            if m:
                seg_list = segwrapper.cut(m.group(2))
                seg_list = [x for x in seg_list if x not in stopword_set]
                outf.write('#Article: %s#Type: regular article%s\n' % (m.group(1).encode('utf-8'), ' '.join(seg_list).encode('utf-8')))
            else:
                print 'not correct format'
            

def make_idf():
    src = './seg_wiki_doc.txt'
    dst = './wiki_idf_dict.txt'
    dst1 = './title_map.txt'
    pattern = re.compile('#Article: (.+)#Type: regular article(.+)')
    idf_dict = {}
    with open(src, 'r') as inf, open(dst1, 'w') as outf:
        for line in inf:
            line = line.strip().decode('utf-8')
            m = pattern.match(line)
            if m:
                word_set = set(m.group(2).split(' '))
                outf.write('%s\n' % m.group(1).encode('utf-8'))
                for w in word_set:
                    idf_dict[w] = idf_dict.get(w, 0) + 1

    with open(dst, 'w') as outf:
        for k, v in idf_dict.iteritems():
            outf.write('%s\t%s\n' % (k.encode('utf-8'), v))

def test_match():
    src = './wiki_idf_dict.txt'
    src1 = './wordmap.txt'
    wiki_set = set([])
    data_set = set([])
    with open(src, 'r') as wiki:
        for line in wiki:
            line = line.strip().decode('utf-8').split('\t')
            if len(line) == 0:
                continue
            wiki_set.add(line[0])
        
    with open(src1, 'r') as data:
        for line in data:
            line = line.strip().decode('gbk')
            items = line.split(' ')
            if len(items) != 2:
                continue
            data_set.add(items[0])

    print 'wiki counts: %s' % len(wiki_set)
    print 'data counts: %s' % len(data_set)



    exact_set = wiki_set & data_set
        
    print 'exact counts: %s' % len(exact_set)

    

if __name__ == '__main__':
	segwrapper.open()
    make_idf()
	segwrapper.close()
    print 'over'
            
    
