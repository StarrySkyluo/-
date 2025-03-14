import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

import time
import pandas as pd

chrome_options = Options()
chrome_options.binary_location = r"E:\chrome\chrome.exe"
chrome_options.page_load_strategy = "eager"  # DOM 加载完就继续，不等所有资源
web = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(web, 10)


def close_login():
    try:
        login_btn = web.find_element(By.CLASS_NAME, 'close-btn')
        login_btn.click()
    except:
        pass


def save_csv(all_txts):
    all_txts_csv = pd.DataFrame(all_txts)
    all_txts_csv.to_csv("all_contents.csv", index=False, encoding='utf-8-sig')


def nextPage():
    try:
        next_page_box = web.find_element(By.CSS_SELECTOR, '.l_pager.pager_theme_5.pb_list_pager')
        next_page_box_a = next_page_box.find_elements(By.TAG_NAME, 'a')
        next_page_box_a[-2].click()
    except Exception as e:
        web.refresh()
        time.sleep(5)
        close_login()
        scrollToBottom()
        nextPage()


def scrollToBottom():
    # 滚动网页到底部，进行翻页,先滚动4-7次300-500像素，然后滚动到页面底部以加载网页
    # 滚动网页到底部，进行翻页,先滚动4-7次300-500像素，然后滚动到页面底部以加载网页
    for i in range(random.randint(4, 7)):
        scroll_distance = random.randint(300, 500)  # 生成 300~500 之间的随机滚动距离
        web.execute_script(f"window.scrollBy(0, {scroll_distance});")
        time.sleep(random.uniform(0, 1))  # 等待 随机 秒，防止页面加载不及
    web.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def spiderOneContent(title, url):
    web.get(url)
    close_login()
    time.sleep(2)
    one_all_txts = []
    one_all_txts.append(title)

    allpages_box = web.find_elements(By.XPATH, '//li[@class="l_reply_num"]')
    spans = allpages_box[0].find_elements(By.TAG_NAME, 'span')
    # spans[1].text是显示本帖有多少页
    pages_num = spans[1].text
    print("本帖共有" + pages_num + "页")
    t = 0
    for i in range(int(spans[1].text)):
        time.sleep(2)
        close_login()
        time.sleep(5)
        # 让其加载底部
        scrollToBottom()

        # 单页爬取
        # 获取一条评论的整体(多条评论集合one_alls)
        allmsg = web.find_element(By.CLASS_NAME, 'p_postlist')
        one_alls = allmsg.find_elements(By.CSS_SELECTOR, '.l_post.j_l_post.l_post_bright')

        for one_all in one_alls:
            # 获取用户姓名
            author = one_all.find_element(By.CLASS_NAME, 'd_author')
            author_name_li = author.find_element(By.XPATH, './/li[@class="d_name"]')
            author_name_a = author_name_li.find_element(By.TAG_NAME, 'a')
            author_name = author_name_a.text

            # 获取发言
            content_div = one_all.find_element(By.CSS_SELECTOR, '.d_post_content.j_d_post_content')
            content_text = content_div.text

            one_all_txts.append(author_name)
            one_all_txts.append(content_text)
        if pages_num != '1':
            nextPage()

        print("第"+str(t)+"页爬取完毕...")
        t = t + 1

    return one_all_txts


def spiderContents(csv_data):
    len_csv = len(csv_data)
    print("总共"+str(len_csv)+"个帖子...")
    t = int(input('你想爬取多少个帖子的评论：'))
    all_txts = []
    # 访问每个网页进行爬取评论
    for ((index, row), t) in zip(csv_data.iterrows(), range(t)):
        title = row['title']
        url = row['url']

        one_all_txts = spiderOneContent(title, url)
        all_txts.append(one_all_txts)
        print("第" + str(t + 1) + "个帖子爬取完毕...")
    return all_txts


def main():
    # 读入csv数据文件（title，url）
    with open('title_url.csv', 'r', encoding='utf-8') as file:
        csv_data = pd.read_csv(file)
        # print(csv_data)

    all_txts = spiderContents(csv_data)

    # 保存评论至csv

    save_csv(all_txts)
    print('全部帖子爬取完毕...')
