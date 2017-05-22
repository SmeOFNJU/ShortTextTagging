from collections import defaultdict

def handle(file_name):
    precision = []
    recall = []
    with open(file_name, 'r') as f:
        for line in f:
            items = line.decode('gbk').strip('\n').split('\t')
            if len(items) != 2:
                raise Exception('error')
            target = set(items[0].split('||'))
            rec = defaultdict(int)
            for i in items[1].split('&&'):
                ii = i.split(':')
                if len(ii) != 2:
                    continue
                iii = ii[0].split('||')
                for iiii in iii:
                    rec[iiii] += float(ii[1])
            k = 5
            final = sorted(rec.items(), key=lambda x:x[1], reverse=True)
            final = final[:k]
            cor = 0.0
            for (i, cnt) in final:
                if i in target:
                    cor += 1
            precision.append(cor / len(target))
            recall.append(cor / len(final))
    print 'precision: %s' % (sum(precision) / len(precision))
    print 'recall: %s' % (sum(recall) / len(recall))

handle('./result/tfidf_res')


