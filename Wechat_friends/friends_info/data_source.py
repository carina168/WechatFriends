import json
import itchat
import re
from collections import Counter
import jieba
from snownlp import SnowNLP

class DATASOURCE:

    def __init__(self):

        self.friends = []
        self.friends_num = 0
        self.filter_signature_list = []
        self.emotions_signature_total = 0

        # 获取好友数据
        self.get_friends()

        # 获取好友数量
        self.get_friends_num()

        # 获取过滤后的好友个性签名
        self.get_friends_filter_signature_list()

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
        sex = {'男性-Male': 0, '女性-Female': 0, '未知-Other': 0}

        for f in self.friends:
            if f['Sex'] == 1:
                sex['男性-Male'] += 1
            elif f['Sex'] == 2:
                sex['女性-Female'] += 1
            else:
                sex['未知-Other'] += 1
        # print(" male:%d\n female:%d\n other:%d\n" % (sex['Male'], sex['Female'], sex['Other']))
        return sex

    def get_friends_city(self):
        city_list = []
        for f in self.friends:
            city = f['City']
            city_list.append(city)
        # 去除微信好友中city信息为空的空白字符
        filter_city_list = filter(None, city_list)
        city_counter = dict(Counter(filter_city_list).most_common(10))  # top10

        print(city_counter)
        return city_counter

    def get_friends_province(self):
        provinces = []
        for f in self.friends:
            province = f['Province']

            res = re.compile(r'[^\u4e00-\u9fa5]')  # 清除非china省份的省份名
            provinces_1 = re.sub(res, '', province)

            provinces.append(provinces_1)

        filter_provinces = filter(None, provinces)  # 去除列表中有些微信好友没填省份信息的空字符

        provinces_count = Counter(filter_provinces)
        print(provinces_count)
        return provinces_count

    def get_friends_filter_signature_list(self):
        for f in self.friends:
            signature = f['Signature']
            sign = signature.strip()
            sub_str1 = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", sign)
            sub_str = re.sub("[A-Za-z0-9\'\：\·\—\，\。\“ \”\n\u3000\？\、\'*\',\']", "", sub_str1)
            if sub_str is not None:
                self.filter_signature_list.append(sub_str)

    def get_friends_signature(self):
        sign_list = self.filter_signature_list
        cut_words = ""
        for f in sign_list:
            seg_list = jieba.cut(f, cut_all=False)
            cut_words += (" ".join(seg_list))
        all_words = cut_words.split()
        c = Counter()
        for x in all_words:
            if len(x) > 1 and x != '\r\n':
                c[x] += 1

        signatures_dict = {}
        for (k, v) in c.items():
            signatures_dict[k] = v

        return signatures_dict

    def get_signature_emotions(self):
        signature_list = self.filter_signature_list
        emotion_list = []
        for f in signature_list:
            if f is None or f == '':
                continue
            blob = SnowNLP(f).sentiments
            emotion_list.append(blob)

        # 情感分析
        positive = len(list(i for i in emotion_list if i > 0.66))
        normal = len(list(i for i in emotion_list if i <= 0.66 and i >= 0.33))
        # normal = len(list(filter(lambda x:x>=0.33 and x<=0.66,emotions)))
        negative = len(list(i for i in emotion_list if i < 0.33))

        self.emotions_signature_total = positive + normal + negative

        emotion_dict = {'积极-Positive': positive, '中性-Normal': normal, '消极-Negative': negative}
        return emotion_dict

    def get_special_friends(self):
        # 获取特殊好友
        star_num = 0  # 星标朋友
        deny_see_num = 0  # 不让他看我的朋友圈
        no_see_num = 0  # 不看他的朋友圈
        for f in self.friends:
            if f['StarFriend'] == 1:
                star_num += 1
            elif f['ContactFlag'] in [259, 33027, 65795]:
                deny_see_num += 1
            elif f['ContactFlag'] in [65539, 65795, 65537, 98307]:
                no_see_num += 1

        print('星标好友：', star_num)
        print('不让他看我的朋友圈：', deny_see_num)
        print('不看他的朋友圈：', no_see_num)

        special_firends_dict = {'星标好友': star_num, '不让他看我的朋友圈': deny_see_num, '不看他的朋友圈': no_see_num}
        return special_firends_dict
