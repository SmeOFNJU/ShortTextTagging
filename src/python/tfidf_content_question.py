# -*- coding: gbk -*-

import segwrapper

clses = ['电影', '法律', '交通', '生物', '食物', '体育', '文学', '音乐', '游戏', '政治', '宗教']

def handle():
    precision = []
    recall = []
    for clss in clses:
        src = 'E:\data\extracted\extracted\\tags_question_content_answer_200\%s.file' % clss
        with open(src, 'r') as f:
            for line in f:
                items = line.strip().decode('gbk').split('\t')
                if len(items) < 4:
                    continue
                tags = items[0].split('||')
                if len(tags) < 3:
                    continue
                question = '%s %s %s' % (items[1], items[2], items[3])
                res = segwrapper.extract_tags(question, 5)
                cor = len(set(res) & set(tags))
                if len(res) == 0 or len(tags) == 0:
                    continue
                pre = float(cor) / len(res)
                rec = float(cor) / len(tags)

                precision.append(pre)
                recall.append(rec)
    return precision, recall

def main():
    precision, recall = handle()
    print 'precision: %s' % (sum(precision) / len(precision))
    print 'recall: %s' % (sum(recall) / len(recall))

segwrapper.open()
main()
segwrapper.close()


