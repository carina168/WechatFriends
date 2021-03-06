import itchat
from Wechat_friends.friends_info.friends_information import FriendInformation


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    friends_info = FriendInformation()

    friends_info.sex_viewer()
    friends_info.show_friends_city_by_bar()
    friends_info.show_friends_provinces_by_map()



