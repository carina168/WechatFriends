
import itchat
from pyecharts import Pie, Bar, Map
from Wechat_friends.friends_info.data_source import DATASOURCE



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

        pie = Pie('好友性别比例', '好友总人数：%d' % self.Friends.friends_num, title_pos='center')
        pie.add('性别比例', sex_keys, sex_value, radius=[30, 75], rosetype='area', is_label_show=True,
                is_legend_show=True, legend_top='bottom')
        pie.render('../view/好友性别比例.html')

    def show_friends_city_by_bar(self):
        city_list = self.Friends.get_friends_city()
        key = list(city_list.keys())
        value = list(city_list.values())

        bar = Bar("微信好友所在城市分布图")
        bar.add("城市分布情况", key, value, is_more_utils=True, mark_line=["min", "max"],
                xaxis_rotate=45, is_label_show=True)  # mark_line:设置标志线 xaxis_rotate:设置底部文字倾斜角度
        bar.render('../view/city.html')

    def show_friends_provinces_by_map(self):
        provinces_list = self.Friends.get_friends_province()
        key = list(provinces_list.keys())
        value = list(provinces_list.values())

        china_map = Map("我的微信好友分布", "@OuCuirong")
        china_map.add("", key, value, maptype='china', is_visualmap=True, visual_text_color='#000')
        china_map.render('../view/china.html')

