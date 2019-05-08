from bs4 import BeautifulSoup
import requests
import pandas as pd


class data:
    def __init__(self, id, name, ver, rate, etype):
        self.id = id
        self.name = name
        self.ver = ver
        self.rate = rate
        self.etype = etype

    def __str__(self):
        return "%s %s %s %s %s" % (self.id, self.name, self.ver, self.rate, self.etype)


def get_data(version):
    # with open(r'C:\Users\ccc\Desktop\111.txt', 'r', encoding='UTF-8') as file:
    #     content = file.read()
    bug_data = []
    error_bug = []
    num = 1
    frequency, result = 0, 0
    cookie = dict(zentaosid='m5r5dk62rcqq3ke9frr0eo45u1', lang='zh-cn')
    for i in range(15):
        loginUrl = 'http://192.168.9.138:30085/zentao/bug-browse-1-0-all-0--1000-20-' + str(num) + '.html'
        content = requests.get(loginUrl, cookies=cookie).text
        soup = BeautifulSoup(content, 'html.parser')
        b = soup.select('#bugList > tbody > tr')
        for b in b:
            w = b.find('a', href=True, title=True)['title']
            if w not in version:
                continue
            q = b.find(class_='c-resolvedBy').text.strip()
            e = b.find(class_='label-severity')['title']
            r = b.find(class_='c-type').text
            t = b.attrs['data-id']
            if q == '' or (r != '代码错误' and r != '界面优化'):
                error_bug.append(data(t, q, w, e, r))
                continue
            bug_data.append(data(t, q, w, e, r))
        if result == len(bug_data):
            frequency += 1
        if frequency == 4:
            break
        result = len(bug_data)
        num += 1
    return bug_data, error_bug


if __name__ == '__main__':
    q = []
    ver = ['V3.7验收','V3.7第三轮','V3.7第二轮','V3.7第一轮']
    bug_data, error_bug = get_data(ver)
    df = pd.DataFrame({'version': [i.ver for i in bug_data],
                       'name': [i.name for i in bug_data ],
                       'rate': [i.rate for i in bug_data],
                       'etype': [i.etype for i in bug_data]
                       })
    gro = df.groupby(['version', 'name', 'rate'], as_index=False).count()
    for i in ver:
        q.append(gro[gro['version'].isin([i])])
    for i in q[0].values.tolist():
        print(i)
    #q[0]['etype'].sum() #汇总
    # for i in error_bug:
    #     print(i)





