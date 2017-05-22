import json
name = 'word_topic_distribution'
with open('%s.part0' % name, 'r') as p0, \
     open('%s.part1' % name, 'r') as p1, \
     open('%s.file' % name, 'w') as outf:
    for line in p0:
        line = line.strip().decode('utf-8')
        other_line = next(p1)
        other_line = other_line.decode('utf-8')

        items_p0 = line.split('\t')
        items_p1 = other_line.split('\t')
        if items_p0[0] != items_p1[0]:
            print 'not equal line'
            continue
        dict_p0 = json.loads(items_p0[1])
        dict_p1 = json.loads(items_p1[1])
        for k, v in dict_p1.iteritems():
            dict_p0[k] = v

        outf.write(('%s\t%s\n' % (items_p0[0], json.dumps(dict_p0))).encode('utf-8'))

print 'over'
        
