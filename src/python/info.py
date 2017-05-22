
with open('word_id_dict.txt', 'r') as inf, open('cn_word_id_dict.txt', 'w') as outf, \
     open('tw_word_id_dict.txt', 'w') as outf1, \
     open('en_word_id_dict.txt', 'w') as outf2:
    for line in inf:
        line = line.strip().decode('utf-8')
        items = line.split('\t')
        if len(items) != 2:
            print 'not correct format'
        try:
            items[0].encode('gb2312')
            try:
                outf2.write('%s\t%s\n' % (items[0].encode('utf-8'), items[1]))
            except:
                outf.write(('%s\t%s\n' % (items[0], items[1])).encode('utf-8'))
        except:
            outf1.write(('%s\t%s\n' % (items[0], items[1])).encode('utf-8'))
            continue

print 'over'
