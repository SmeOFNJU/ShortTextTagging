
def handle(file_name, data_name, tag_name):
    with open(file_name, 'r') as f, open(data_name, 'w') as dataf, open(tag_name, 'w') as tagf:
        for line in f:
            items = line.decode('gbk').rstrip('\n').split('\t')
            if len(items) != 2:
                print line
                raise Exception('error')
            if len(items[1]) == 0:
                continue
            dataf.write('%s\n' % items[1].encode('gbk'))
            tagf.write('%s\n' % items[0].encode('gbk'))
handle('./data/test_data.txt', './result/test_data.txt', './result/new_tag.txt')
handle('./data/training_data.txt', './result/training_data.txt', './result/tag_data.txt')
