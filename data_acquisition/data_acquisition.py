# 爬取哔哩哔哩上所需的数据
import re
import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options

import openpyxl
import os


# 优化方向：
# 1.自定义存储路径和文件名，而不是固定存储到data/data_raw.xlsx
# 2.爬取视频的网站名字作为文件名,不需要手动输入
# 3.改成多线程，一次进行多个视频评论的爬取，然后数据分别对应存储到不同的表格中

# 错误:
# 1.查看分页回复不能直接点击对应的分页按钮,会疏忽很多回复页面的内容,要点下一页按钮,没有下一页按钮,那就说明到底了

def login(webdriver, url):
    """
    登录
    :param webdriver: 驱动
    :param url: 目标网页地址
    :return:
    """
    # 打开目标链接
    webdriver.get(url)
    time.sleep(5)
    # 登录
    print(">>>进行登录")
    header_login_entry = webdriver.find_element(By.CSS_SELECTOR, 'div.header-login-entry')
    header_login_entry.click()
    time.sleep(5)
    # 账号输入框
    print(">>>输入账号")
    account = webdriver.find_element(By.XPATH, '/html/body/div[8]/div/div[4]/div[2]/form/div[1]/input')
    account.send_keys('15347602198')
    # 密码输入框
    print(">>>输入密码")
    password = webdriver.find_element(By.XPATH, '/html/body/div[8]/div/div[4]/div[2]/form/div[3]/input')
    password.send_keys('zhuyulin1015')
    # 登录按钮
    print(">>>点击登录")
    login_btn = webdriver.find_element(By.CSS_SELECTOR, 'body .bili-mini-mask .btn_wp div:nth-child(2)')
    login_btn.click()
    time.sleep(30)


def save_comments(file_path, comments):
    if os.path.exists(file_path):
        # 如果文件存在，打开
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active
    else:
        # 如果文件不存在，则创建新的工作薄和工作表
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        # 新文件，写入表头信息
        sheet.append(['id', 'contents', 'parent_id', 'pubdate', 'like_count'])

    # 遍历存入评论数据
    for comment in comments:
        sheet.append(comment)

    print(">>>一条父评论及其子评论数据已存入")
    # 保存文件
    workbook.save(file_path)
    print(">>>文件已保存")


# 1.使用By.TAG_NAME获取元素时，只能查找当前元素的直接子元素
# 2.运行js脚本，让页面滚动到指定元素的位置
# 3.使用 find_element() 或 find_elements() 获取元素时，Selenium 返回的是该 DOM 元素的引用（指向该元素的对象）。这个引用会保持同步，并且它与页面中的真实元素保持一致。
# 4.如果不是使用Selenium接口中相关方法，不会与页面中元素实时保持同步如len(元素)，而是元素当前快照时的状态（即初始获取这个元素时候的状态）
def get_comments(webdriver):
    """
    获取评论内容、二级评论内容、评论发布时间、评论点赞数
    :param webdriver: 驱动
    :return:
    """
    # 评论区
    # print(">>>评论区")
    comment_app = webdriver.find_element(By.ID, 'commentapp')
    bili_comments = comment_app.find_element(By.TAG_NAME, 'bili-comments')
    bili_comments_shadow = bili_comments.shadow_root  # 获取shadow DOM

    # 将页面滚动到指定元素的位置
    # print(">>>将页面滚动到指定元素的位置")
    webdriver.execute_script('arguments[0].scrollIntoView()', comment_app)

    time.sleep(0.5)
    # 所以评论id
    comment_id = 1
    # 父评论索引
    parent_comments_index = 0
    # 父评论id
    parent_comment_id = 0
    while True:
        # 评论与二级评论
        # print(">>>评论与二级评论")
        feed = bili_comments_shadow.find_element(By.ID, 'feed')
        bili_comment_thread_renderers = feed.find_elements(By.TAG_NAME, 'bili-comment-thread-renderer')
        # print(f">>>评论数量 {len(bili_comment_thread_renderers)}")

        # 评论全部加载完毕，退出循环
        if parent_comments_index >= len(bili_comment_thread_renderers):
            # print(">>>评论全部加载并爬取完毕，退出循环")
            # print(f">>>共爬取父评论数 {parent_comments_index}")
            break
        while parent_comments_index < len(bili_comment_thread_renderers):
            # 存储一条父评论，及其子评论
            comments = []
            # 获取shadow DOM
            bili_comment_thread_renderer_shadow = bili_comment_thread_renderers[parent_comments_index].shadow_root

            # 将页面滚动到该条评论的位置
            # print(">>>滚动到评论的位置")
            webdriver.execute_script('arguments[0].scrollIntoView()',
                                     bili_comment_thread_renderers[parent_comments_index])
            time.sleep(0.5)

            # 获取父评论的内容、发布时间、点赞数
            # 内容
            bili_comment_renderer = bili_comment_thread_renderer_shadow.find_element(By.ID,
                                                                                     'comment')
            bili_comment_renderer_shadow = bili_comment_renderer.shadow_root
            content = bili_comment_renderer_shadow.find_element(By.ID, 'content')
            bili_rich_text = content.find_element(By.TAG_NAME, 'bili-rich-text')
            bili_rich_text_shadow = bili_rich_text.shadow_root
            contents = bili_rich_text_shadow.find_element(By.ID, 'contents')
            parent_comment_text = contents.text  # 获取该元素及其所有子元素的文本内容
            # print(f">>>父评论内容\n {parent_comment_text}")
            # 发布时间
            footer = bili_comment_renderer_shadow.find_element(By.ID, 'footer')
            bili_comment_action_buttons_renderer = footer.find_element(By.TAG_NAME,
                                                                       'bili-comment-action-buttons-renderer')
            bili_comment_action_buttons_renderer_shadow = bili_comment_action_buttons_renderer.shadow_root
            pubdate = bili_comment_action_buttons_renderer_shadow.find_element(By.ID, 'pubdate')
            parent_comment_pubdate = pubdate.text
            # print(f">>>父评论发布时间 {parent_comment_pubdate}")
            # 点赞数
            count = bili_comment_action_buttons_renderer_shadow.find_element(By.ID, 'count')
            parent_comment_like = count.text
            # print(f">>>父评论点赞数 {parent_comment_like}")

            # 存储父评论
            comments.append([comment_id, parent_comment_text, 'null', parent_comment_pubdate, parent_comment_like])

            # 评论数+1
            parent_comments_index = parent_comments_index + 1
            # 父评论id
            parent_comment_id = comment_id
            # 评论id 自增1
            comment_id = comment_id + 1

            print(f">>>爬取父评论数 {parent_comments_index}")
            replies_num = 0  # 每条评论回复评论的数量
            try:
                # 查看回复按钮
                print(">>>查看回复按钮")
                replies = bili_comment_thread_renderer_shadow.find_element(By.ID, 'replies')
                bili_comment_replies_renderer = replies.find_element(By.TAG_NAME, 'bili-comment'
                                                                                  '-replies-renderer')
                bili_comment_replies_renderer_shadow = bili_comment_replies_renderer.shadow_root  # 获取shadow DOM
                view_more = bili_comment_replies_renderer_shadow.find_element(By.ID, 'view-more')
                # 查看有多少台回复内容
                span = view_more.find_element(By.TAG_NAME, 'span')
                span_text = span.text
                # print(f">>>{span_text}")
                # 正则 匹配数字
                pattern = r'(\d+)'  # r是原始字符串(raw string)标记符号，表明不要对字符串中的反斜杆进行转义
                match = re.search(pattern, span_text)
                if match:
                    replies_num = match.group(1)

                bili_text_button = view_more.find_element(By.TAG_NAME, 'bili-text-button')
                bili_text_button_shadow = bili_text_button.shadow_root
                button = bili_text_button_shadow.find_element(By.CLASS_NAME, 'button')
                # 将页面滚动对应位置，在屏幕中能够显示，才能够被点击
                webdriver.execute_script('arguments[0].scrollIntoView()', button)
                time.sleep(0.5)
                webdriver.execute_script('window.scrollBy(0, -100)')
                time.sleep(0.25)
                print(">>>点击查看回复按钮")
                button.click()
                time.sleep(2)  # 如果报错，很有可能是回复还没加载出来，在此处适当增加睡眠时间即可
            except NoSuchElementException:
                # 没有查看回复按钮：1.可能是回复评论很少，不用分页就直接显示了 2.没有回复评论
                # 对于第1种情况需要获取评论的信息
                print(">>>没有查看回复按钮")

            # 爬取二级评论
            paging_exist = True  # 分页按钮是否存在的标志
            # 获取分页按钮元素
            try:
                pagination_body = bili_comment_replies_renderer_shadow.find_element(By.ID, 'pagination-body')
                webdriver.execute_script('arguments[0].scrollIntoView()', pagination_body)
                time.sleep(0.5)
                webdriver.execute_script('window.scrollBy(0,-100)')
                time.sleep(0.25)
            except NoSuchElementException:
                # 没有分页按钮
                print("没有多个分页按钮")
                paging_exist = False
            while True:
                # 获取回复内容
                expander_contents = bili_comment_replies_renderer_shadow.find_element(By.ID,
                                                                                      'expander-contents')
                bili_comment_reply_renderers = expander_contents.find_elements(By.TAG_NAME,
                                                                               'bili-comment-reply-renderer')

                # 遍历每个评论
                for bili_comment_reply_renderer in bili_comment_reply_renderers:
                    bili_comment_reply_renderer_shadow = bili_comment_reply_renderer.shadow_root
                    main = bili_comment_reply_renderer_shadow.find_element(By.ID, 'main')
                    footer = bili_comment_reply_renderer_shadow.find_element(By.ID, 'footer')
                    # 评论内容
                    bili_rich_text = main.find_element(By.TAG_NAME, 'bili-rich-text')
                    bili_rich_text_shadow = bili_rich_text.shadow_root
                    contents = bili_rich_text_shadow.find_element(By.ID, 'contents')
                    son_comment_text = contents.text
                    # print(f">>>子评论内容\n {son_comment_text}")
                    # 发布时间、点赞数
                    # 发布时间
                    bili_comment_action_buttons_renderer = footer.find_element(By.TAG_NAME,
                                                                               'bili-comment-action-buttons'
                                                                               '-renderer')
                    bili_comment_action_buttons_renderer_shadow = bili_comment_action_buttons_renderer.shadow_root
                    pubdate = bili_comment_action_buttons_renderer_shadow.find_element(By.ID, 'pubdate')
                    son_comment_pubdate = pubdate.text
                    # print(f">>>子评论发布时间 {son_comment_pubdate}")
                    # 点赞数
                    count = bili_comment_action_buttons_renderer_shadow.find_element(By.ID, 'count')
                    son_comment_like = count.text
                    # print(f">>>子评论点赞数 {son_comment_like}")

                    # 存储子评论
                    comments.append([comment_id, son_comment_text, parent_comment_id, son_comment_pubdate,
                                     son_comment_like])
                    # 评论id自增1
                    comment_id = comment_id + 1

                # 获取下一页按钮
                if paging_exist:
                    # 重新获取页面按钮元素集合
                    bili_text_buttons = pagination_body.find_elements(By.TAG_NAME, 'bili-text-button')
                    # 如果有下一页，最后一个元素是“下一页”按钮
                    bili_text_button = bili_text_buttons[len(bili_text_buttons) - 1]
                    # print(f">>>最后一个分页按钮内容： {bili_text_button.text}")
                    if bili_text_button.text == '下一页':
                        # 移动页面
                        webdriver.execute_script('arguments[0].scrollIntoView()', bili_text_button)
                        time.sleep(0.5)
                        webdriver.execute_script('window.scrollBy(0, -100)')
                        time.sleep(0.25)
                        bili_text_button.click()
                        time.sleep(2)
                    else:
                        break
                else:
                    break

            try:
                pagination_foot = bili_comment_replies_renderer_shadow.find_element(By.ID, 'pagination-foot')
                bili_text_button = pagination_foot.find_element(By.TAG_NAME, 'bili-text-button')
                bili_text_button_shadow = bili_text_button.shadow_root
                button = bili_text_button_shadow.find_element(By.CLASS_NAME, 'button')
                button.click()
                print(">>>点击收起按钮")
            except NoSuchElementException:
                print(">>>没有收起按钮")

            # 将一条父评论及其回复存储到表格中
            save_comments(file_path='../data_raw/data_raw.xlsx', comments=comments)


if __name__ == '__main__':
    # 设置网页打开配置选项
    options = Options()
    options.add_argument("--start-maximized")  # 全屏打开

    # 初始化驱动
    webdriver = webdriver.Edge(options=options)

    # 目标网页链接
    url = ("https://www.bilibili.com/video/BV1r1r6YfEhv/?spm_id_from=333.934.0.0&vd_source"
           "=fa17a360ca302344f8e38fc493ad2ecd")
    # 登录
    login(webdriver=webdriver, url=url)
    # 爬取评论
    # 耗时
    start_time = time.time()
    get_comments(webdriver=webdriver)
    end_time = time.time()
    # 计算运行时间
    execution_time = end_time - start_time
    print(f">>>爬取评论耗时 {execution_time} 秒")
