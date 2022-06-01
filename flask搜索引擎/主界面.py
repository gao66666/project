from flask import Flask, render_template, request
from flask import g
import jieba
from elasticsearch import Elasticsearch
es = Elasticsearch()
app = Flask(__name__)

def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False
def sort2(data,key):
    ind={}
    td=0
    stopwords=[]
    with open('stopwords.txt', 'r', encoding='utf-8') as f:
        stopwords = f.read().split('\n')

    for d in data:
        cnt=0
        ind[f'{td}']=0
        for k in key:
            if k in stopwords:
                continue
            s=d['passage']+d['title']+d['zy']+d['keywords']
            cnt+=s.count(k)
        ind[f'{td}']+=cnt
        td+=1
    ind=sorted(ind.items(),key=lambda x :x[1],reverse=True)
    ind=dict(ind)
    data2=[]
    for index in ind.keys():
        data2.append(data[int(index)])
    return data2







def get_data(key):
    key = list(jieba.cut(key))
    d={}
    es = Elasticsearch()
    data = []
    for k in key:
        if k not in ['', ',', '。', '!']:
            dsl = {
                'match': {
                    'title': k
                }
            }
            result = es.search(index='sina', query=dsl)
            L = result['hits']['hits']
            data.extend([r['_source'] for r in L])
    d['data']=data
    data = sorted(data, key=lambda x: x['PR'], reverse=True)
    data=sort2(data,key)
    print('获取数据成功')
    return data


@app.route('/')  # 主页地址,“装饰器”
def news():
    return render_template('开始界面.html')


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == "POST":
        keywords = request.form.get('query')
        pa = 1
        ori_key = ''
        if keywords is None:
            pa = int(request.form.get('page'))
            print('页码', pa)
            keywords = request.form.get('key')
        ori_key = ''.join(keywords.split(','))
        data = get_data(keywords)
        L = len(data)
        page_num = 7
        if pa > int(L / page_num):
            pa = int(L / page_num)
        data = data[(pa - 1) * page_num:(pa - 1) * page_num + page_num]
    else:
        g.data = []
        keywords = 'what'
    k2 = []
    for l in jieba.cut(keywords):
        if is_Chinese(l):
            k2.append(l)
    keywords = ','.join(k2)

    if pa >= 4:
        edge = range(pa - 3, pa + 7)
    else:
        edge = range(1, 10)
    return render_template('test.html', data=data, keywords=keywords, length=L, pages=edge, now_page=pa,
                           ori_key=ori_key)


if __name__ == '__main__':
    app.run(debug=True)
