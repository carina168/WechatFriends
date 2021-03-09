import itchat
from bs4 import BeautifulSoup
from pyecharts.charts import Page

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
             friends_info.show_friends_city_by_bar(),
             friends_info.show_friends_provinces_by_map(),
             friends_info.show_friends_signatures_wordcloud(),
             friends_info.show_special_friends_by_bar()
             )
    page.render(index_html_location)

    # with open(index_html_location, "r+", encoding='utf-8') as html:
    #     html_bf = BeautifulSoup(html, "lxml")  # 创建 beautifulsoup 对象，Beautiful Soup是python的一个库，最主要的功能是从网页抓取数据
    #     divs = html_bf.find_all("div")  # find_all()找到所有匹配结果出现的地方，找到所有匹配div的地方
    #     divs[0]["style"] = "width:600px;height:350px;position:absolute;top:70px;left:0px;border-style:solid;border-color:#444444;border-bottom-width:0px;border-top-width:1px;border-left-width:0.5px;border-right-width:0.5px;"
    #     divs[1]["style"] = "width:600px;height:350px;position:absolute;top:70px;left:600px;border-style:solid;border-color:#444444;border-bottom-width:0px;border-top-width:1px;border-left-width:0.5px;border-right-width:0.5px;"
    #
    #     body = html_bf.find("body")
    #     body["style"] = "background-color:#FFFFFF"
    #     div_title = "<div align=\"center\" style=\"width:3000px;left:0px;\">\n<span style=\"font-size:32px;font face=\'黑体\';color:#000\"><b>BI看板test</b></div>"  # 修改页面背景色、添加看板标题，以及标题的宽度等。注：需根据看板整体宽度调整标题的宽度，使标题呈现居中效果。
    #     body.insert(0, BeautifulSoup(div_title, "lxml").div)
    #     html_new = str(html_bf)
    #     html.seek(0, 0)
    #     html.truncate()
    #     html.write(html_new)
    #     html.close()
