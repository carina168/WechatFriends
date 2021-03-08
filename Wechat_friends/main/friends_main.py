import itchat
from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line, Liquid, Page, Pie

from Wechat_friends.friends_info.friends_information import FriendInformation

index_html_location = f'../view/wechat_visualization_system.html'

if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    friends_info = FriendInformation()

    # friends_info.sex_viewer()
    # friends_info.show_friends_city_by_bar()
    # friends_info.show_friends_provinces_by_map()
    # friends_info.show_friends_signatures_wordcloud()
    # friends_info.show_special_friends_by_bar()

    page = Page(layout=Page.DraggablePageLayout, page_title="微信朋友圈可视化分析")
    page.add(friends_info.sex_viewer(),
             friends_info.show_friends_city_by_bar())
    # page.add(friends_info.show_friends_provinces_by_map())
    # page.add(friends_info.show_friends_signatures_wordcloud())
    # page.add(friends_info.show_friends_signatures_wordcloud())
    # page.add(friends_info.show_special_friends_by_bar())
    page.render(index_html_location)

    # with open(index_html_location, "r+", encoding='utf-8')

