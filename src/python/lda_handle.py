from scipy import spatial
import heapq

def load_tags(tag_name):
    res = []
    with open(tag_name, 'r') as f:
        for line in f:
            items = line.decode('gbk').strip()
            res.append(items)
    return res

def load_train_file(train_file):
    train_res = []
    with open(train_file, 'r') as f:
        for line in f:
            train_res.append([float(i) for i in line.strip().split(' ')])
    return train_res

def handle(test_file):
    train_res = load_train_file('./result/model-final.theta')
    train_tags = load_tags('./result/rank_tag.txt')
    test_tags = load_tags('./result/new_tag.txt')
    with open(test_file, 'r') as f, open('./result/lda_res_rank.txt', 'w') as outf:
        test_cnt = 0
        for line in f:
            items = [float(i) for i in line.strip().split(' ')]
            h = []
            k = 5
            cnt = 0
            for doc in train_res:
                sim = 1 - spatial.distance.cosine(items, doc)
                heapq.heappush(h, (sim, cnt))
                if len(h) > k:
                    heapq.heappop(h)
                cnt += 1
            #candidate = '||'.join(['%s: %s' % (train_tags[i], sim) for (sim, i) in h])
            candidate = []
            for (s, i) in h:
                for tt in train_tags[i].split('||'):
                    candidate.append('%s:%s' % (tt, s))
            candidate = '||'.join(candidate)

            outf.write('%s\t%s\n' % (test_tags[test_cnt].encode('gbk'), candidate.encode('gbk')))
            test_cnt += 1

        
handle('./result/test_data.txt.theta')
