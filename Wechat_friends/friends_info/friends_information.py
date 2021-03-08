import itchat
from pyecharts.charts import Pie, Bar, Map
from pyecharts.faker import Faker

from Wechat_friends.friends_info.data_source import DATASOURCE
from wordcloud import STOPWORDS, WordCloud
import matplotlib.pyplot as plt
from pyecharts import options as opts


class FriendInformation:
    def __init__(self):
        self.Friends = DATASOURCE()
        # 登录wechat账号
        itchat.auto_login(hotReload=True)

    def sex_viewer(self):
        sex = self.Friends.get_friends_sex()

        sex_keys = list(sex.keys())
        sex_value = list(sex.values())
        print("sex key is : ", sex_keys, "\nsex value is : ", sex_value)

        # pie = Pie('好友性别比例', '好友总人数：%d' % self.Friends.friends_num, title_pos='center')
        # pie.add('性别比例', sex_keys, sex_value, radius=[30, 75], rosetype='area', is_label_show=True,
        #         is_legend_show=True, legend_top='bottom')

        pie = Pie()
        pie.add(series_name='性别比例',
                data_pair=[list(z) for z in zip(sex_keys, sex_value)],
                radius=["30%", "70%"],
                rosetype="area")
        pie.set_global_opts(title_opts=opts.TitleOpts(title="好友性别比例", pos_left="center"),
                            legend_opts=opts.LegendOpts(is_show=False))

        pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))

        pie.render('../view/好友性别比例.html')
        return pie

    def show_friends_city_by_bar(self):
        city_list = self.Friends.get_friends_city()
        key = list(city_list.keys())
        value = list(city_list.values())
        #
        # bar = Bar("微信好友所在城市分布图")
        # bar.add("城市分布情况", key, value, is_more_utils=True, mark_line=["min", "max"],
        #         xaxis_rotate=45, is_label_show=True)  # mark_line:设置标志线 xaxis_rotate:设置底部文字倾斜角度
        # bar.render('../view/city.html')

        bar = Bar()
        bar.add_xaxis(xaxis_data=key)
        bar.add_yaxis("城市分布情况", yaxis_data=value)
        # 系列配置设置，这里可以设置显示最大最小值，设置平均分数线
        bar.set_series_opts(
            # 是否显示标签
            label_opts=opts.LabelOpts(is_show=True),
            markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(name="average", type_="average")])
        )
        # 全局配置设置
        bar.set_global_opts(title_opts=opts.TitleOpts(title="好友城市分布图"),
                            xaxis_opts=opts.AxisOpts(name='城市名称', axislabel_opts=opts.LabelOpts(rotate=45)),
                            yaxis_opts=opts.AxisOpts(name='占有人数'))

        bar.render('../view/city.html')
        return bar

    def show_friends_provinces_by_map(self):
        provinces_list = self.Friends.get_friends_province()
        key = list(provinces_list.keys())
        value = list(provinces_list.values())

        china_map = Map("我的微信好友分布", "@OuCuirong", width=1200, height=600, title_pos='center')
        china_map.add("", key, value, maptype='china', is_visualmap=True, visual_text_color='#000')

        china_map.render('../view/china.html')

    def show_friends_signatures_wordcloud(self):
        signatures_list = self.Friends.get_friends_signature()
        # 设置屏蔽词，去除个性签名中的表情、特殊符号等
        stopwords = STOPWORDS.copy()
        stopwords.add('span')
        stopwords.add('class')
        stopwords.add('emoji')
        stopwords.add('emoji1f334')
        stopwords.add('emoji1f388')
        stopwords.add('emoji1f33a')
        stopwords.add('emoji1f33c')
        stopwords.add('emoji1f633')

        # # 导入背景图
        # path = "../data/bc.png"
        # bg_image = plt.imread(path)

        # 设置词云参数，参数分别表示：画布宽高、背景颜色、背景图形状、字体、屏蔽词、最大词的字体大小
        wc = WordCloud(width=1024,
                       height=768,
                       background_color='white',
                       stopwords=stopwords,
                       max_font_size=400,
                       random_state=50,
                       font_path='STKAITI.TTF')
        # 将分词后数据传入云图
        wc.generate_from_text(signatures_list)
        plt.imshow(wc)  # 绘制图像
        plt.axis('off')  # 不显示坐标轴
        # 保存结果到本地
        wc.to_file('../view/个性签名词云图.jpg')
        plt.show()

    def show_special_friends_by_bar(self):
        special_friends_list = self.Friends.get_special_friends()

        key = list(special_friends_list.keys())
        value = list(special_friends_list.values())

        bar = Bar("特殊好友分析", title_pos='center')
        bar.add('', key, value, is_visualmap=True, is_label_show=True)
        bar.render('../view/特殊好友分析.html')

