
src = './title_map.txt'
dst = './title_map_cn.txt'

with open(src, 'r') as inf, open(dst, 'w') as outf:
    for line in inf:
        line = line.strip().decode('utf-8')
        try:
            tmp = line.encode('gb2312')
            outf.write('%s\n' % line.encode('utf-8'))
        except:
            continue
