import itchat
from pyecharts.charts import Pie, Bar, Map, WordCloud
from pyecharts.globals import SymbolType
from Wechat_friends.friends_info.data_source import DATASOURCE
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
                rosetype='area')
        pie.set_global_opts(title_opts=opts.TitleOpts(title="好友性别比例"),
                            legend_opts=opts.LegendOpts(is_show=False))

        pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))

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

        china_map = Map()
        china_map.add(series_name="省份",
                      data_pair=[list(z) for z in zip(key, value)],
                      maptype="china")
        china_map.set_global_opts(title_opts=opts.TitleOpts(title="我的微信好友分布"),
                                  visualmap_opts=opts.VisualMapOpts(min_=100, max_=300))

        china_map.render('../view/china.html')
        return china_map

    def show_friends_signatures_wordcloud(self):
        signatures_dict = self.Friends.get_friends_signature()
        key = list(signatures_dict.keys())
        value = list(signatures_dict.values())
        wc = WordCloud()
        wc.add(series_name="",
               data_pair=[list(z) for z in zip(key, value)],
               word_size_range=[20, 70],
               rotate_step=45,
               word_gap=20
               )
        wc.set_global_opts(title_opts=opts.TitleOpts(title="个性签名词云分析"),
                           tooltip_opts=opts.TooltipOpts(is_show=True))
        wc.render("../view/个性签名词云图.html")
        return wc

    def show_emotions_signature_by_pie(self):
        emotions_dict = self.Friends.get_signature_emotions()
        key = list(emotions_dict.keys())
        value = list(emotions_dict.values())

        pie = Pie()
        pie.add(series_name='分析比例',
                data_pair=[list(z) for z in zip(key, value)],
                radius=["30%", "60%"],
                rosetype="radius")
        pie.set_global_opts(title_opts=opts.TitleOpts(title="个性签名情感分析",
                                                      subtitle='总个性签名数量：%d' % self.Friends.emotions_signature_total,
                                                      pos_left="center"),
                            legend_opts=opts.LegendOpts(is_show=True,
                                                        pos_top='bottom'))

        pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}\n ({d}%)"), is_label_show=True)

        pie.render('../view/emotion.html')
        return pie

    def show_special_friends_by_bar(self):
        special_friends_list = self.Friends.get_special_friends()

        key = list(special_friends_list.keys())
        value = list(special_friends_list.values())

        bar = Bar()
        bar.add_xaxis(key)
        bar.add_yaxis("", value)
        bar.set_global_opts(title_opts=opts.TitleOpts(title="特殊好友分析"),
                            xaxis_opts=opts.AxisOpts(name='好友类别'),
                            yaxis_opts=opts.AxisOpts(name='占有人数'))
        bar.set_series_opts(label_opts=opts.LabelOpts(is_show=True),
                            markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(name="average", type_="average")]))
        bar.render('../view/特殊好友分析.html')
        return bar

