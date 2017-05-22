

word_set = set([])
def simply():
    num = 0
    with open('wordmap.txt', 'r') as f:
        for line in f:
            line = line.strip().decode('gbk')
            items = line.split(' ')
            if len(items) != 2:
                continue
            word_set.add(items[0])

    with open('word_topic_distribution.file', 'r') as inf, \
        open('word_topic_distribution.simple', 'w') as outf:
        for lin in inf:
            line = lin.strip().decode('utf-8')
            items = line.split('\t')
            if len(items) != 2:
                continue
            if items[0] in word_set:
                outf.write(lin)
                num += 1

    print num

simply()

print 'over'
