import json
import itchat
import re
from collections import Counter


class DATASOURCE:

    def __init__(self):

        self.friends = []
        self.friends_num = 0

        # 获取好友数据
        self.get_friends()

        # 获取好友数量
        self.get_friends_num()

    def filter_data(self, desstr=None, restr=''):
        # 过滤表情
        res = re.compile(u'[\U00010000-\U0010ffff\\uD800-\\uDBFF\\uDC00-\\uDFFF]')
        # 过滤html标签
        res1 = res.sub(restr, desstr)
        res = re.compile('</?\w+[^>]*>')
        res2 = res.sub(restr, res1)
        return res2.replace(u'\xa0', u'').replace(u'\u3000', u'').replace(u'\u2003', u'')

    def get_friends(self):
        friends = itchat.get_friends(update=True)[1:]
        for item in friends[1:]:
            friend = {
                'NickName': self.filter_data(item['NickName'].strip(), ''),
                'RemarkName': self.filter_data(item['RemarkName'].strip().replace('\n', ''), ''),  # 备注名
                'Sex': item['Sex'],  # 性别：1男，2女，0未设置
                'Province': item['Province'],  # 省份
                'City': item['City'],  # 城市
                'Signature': self.filter_data(item['Signature'].strip().replace('\n', ''), ''),  # 个性签名（处理签名内容换行的情况）
                'StarFriend': item['StarFriend'],  # 星标好友：1是，0否
                'ContactFlag': item['ContactFlag']  # 好友类型及权限：1和3好友，259和33027不让他看我的朋友圈，65539不看他的朋友圈，65795两项设置全禁止
            }

            if friend['NickName'] == '':
                friend['NickName'] = 'Unknown'

            self.friends.append(friend)
            print(friend, "\n")

        # 把json对象转成字符串并保存在本地
        # indent:参数根据数据格式缩进显示，读起来更加清晰
        with open("../data/friends_data.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(self.friends, indent=2, ensure_ascii=False))

    def get_friends_num(self):
        for f in self.friends:

            self.friends_num += 1

        return self.friends_num

    def get_friends_sex(self):
        sex = {'Male': 0, 'Female': 0, 'Other': 0}

        for f in self.friends:
            if f['Sex'] == 1:
                sex['Male'] += 1
            elif f['Sex'] == 2:
                sex['Female'] += 1
            else:
                sex['Other'] += 1
        # print(" male:%d\n female:%d\n other:%d\n" % (sex['Male'], sex['Female'], sex['Other']))
        return sex

    def get_friends_city(self):
        city_list = []
        for f in self.friends:
            city = f['City']
            city_list.append(city)
        # 去除微信好友中city信息为空的空白字符
        filter_city_list = filter(None, city_list)
        city_counter = Counter(filter_city_list)
        for key in list(city_counter.keys()):
            if city_counter.get(key) < 5:  # 人数小于3的city
                del city_counter[key]
        print(city_counter)
        return city_counter


    def get_friends_province(self):
        provinces = []
        for f in self.friends:
            province = f['Province']
            provinces.append(province)

        filter_provinces = filter(None, provinces)  # 去除列表中有些微信好友没填省份信息的空字符
        provinces_count = Counter(filter_provinces)
        print(provinces_count)
        return provinces_count