import itchat
from bs4 import BeautifulSoup
from pyecharts.charts import Page
import os
from Wechat_friends.friends_info.friends_information import FriendInformation

path = os.getcwd() + "wechat_visualization_system.html"

if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    friends_info = FriendInformation()

    page = Page(layout=Page.SimplePageLayout, page_title="微信朋友圈可视化分析")
    page.add(friends_info.sex_viewer(),
             friends_info.show_special_friends_by_bar(),
             friends_info.show_friends_provinces_by_map(),
             friends_info.show_friends_city_by_bar(),
             friends_info.show_friends_signatures_wordcloud(),
             friends_info.show_emotions_signature_by_pie()
             )
    page.render(path)




    with open(path, "r+", encoding='utf-8') as html:
        html_bf = BeautifulSoup(html, "html.parser")  # 创建 beautifulsoup 对象，Beautiful Soup是python的一个库，最主要的功能是从网页抓取数据
        divs = html_bf.select('.chart-container')
        divs2 = html_bf.select('.f1-table')
        divs3 = html_bf.select('.f1-table tr:nth-child(even)')
        divs[0]["style"] = "width:600px; height:400px; position:absolute; top:100px; left:100px;"
        divs[1]["style"] = "width:650px;height:350px;position:absolute; top:500px;left:100px;"
        divs[2]["style"] = "width:900px;height:700px;position:absolute; top:100px;left:900px;"
        divs[3]["style"] = "width:650px;height:400px;position:absolute; top:900px;left:1250px;"
        divs[4]["style"] = "width:800px;height:400px;position:absolute; top:900px;left:20px;"
        divs[5]["style"] = "width:600px;height:400px;position:absolute; top:900px;left:680px;"

        body = html_bf.find("body")
        body["style"] = "background-color:#ffffff"
        div_title = "<div align=\"center\" style=\"width:1800px;left:0px;\">\n<span style=\"font-size:32px;font face=\'黑体\';color:#444444\"><b>我的微信好友分析数据</b></div>"  # 修改页面背景色、添加看板标题，以及标题的宽度等。注：需根据看板整体宽度调整标题的宽度，使标题呈现居中效果。
        body.insert(0, BeautifulSoup(div_title, "lxml").div)
        html_new = str(html_bf)
        html.seek(0, 0)
        html.truncate()
        html.write(html_new)
        html.close()
    os.startfile(path)
