import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

chrome_options = Options()
chrome_options.binary_location = r"E:\chrome\chrome.exe"
chrome_options.page_load_strategy = "eager"  # DOM 加载完就继续，不等所有资源
web = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(web, 10)

def close_login():
    try:
        login_btn = web.find_element(By.CLASS_NAME,'close-btn')
        login_btn.click()
    except:
        pass

def scrollToBottom():
    # 滚动网页到底部，进行翻页,先滚动4-7次300-500像素，然后滚动到页面底部以加载网页
    # 滚动网页到底部，进行翻页,先滚动4-7次300-500像素，然后滚动到页面底部以加载网页
    for i in range(random.randint(4,7)):
        scroll_distance = random.randint(300, 500)  # 生成 300~500 之间的随机滚动距离
        web.execute_script(f"window.scrollBy(0, {scroll_distance});")
        time.sleep(random.uniform(0,1))  # 等待 随机 秒，防止页面加载不及
    web.execute_script("window.scrollTo(0, document.body.scrollHeight);")

def nextPage():
    # 滚动网页到底部，进行翻页,先滚动4-7次300-500像素，然后滚动到页面底部以加载网页
    scrollToBottom()
    change_page_box = web.find_element(By.ID,'frs_list_pager')
    # next_page_box = change_page_box.find_element(By.CSS_SELECTOR,'.next.pagination-item ')
    next_page_box = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.next.pagination-item ')))
    next_page_box.click()

def save_csv(items_all):
    one_page_csv = pd.DataFrame(items_all, columns=['title', 'url'])
    one_page_csv.to_csv("title_url.csv", index=False)

def spider(items_one_page):
    ul_one_page = web.find_element(By.ID, 'thread_list')
    li_one_page_all = ul_one_page.find_elements(By.XPATH, "//li[@class=' j_thread_list clearfix thread_item_box']")
    for li in li_one_page_all:
        item_div = li.find_element(By.CSS_SELECTOR, ".threadlist_title.pull_left.j_th_tit ")
        item_a = item_div.find_element(By.TAG_NAME, "a")
        title = item_a.get_attribute("title")
        href = item_a.get_attribute("href")
        items_one_page.append((title, href))
    return items_one_page

def main():
    # 打开贴吧网页
    url = r"https://tieba.baidu.com/"
    web.get(url)
    time.sleep(2)
    close_login()
    # 输入要爬取的贴吧并进入该贴吧
    searchIn = input('请输入要爬取的贴吧：')

    search_in = web.find_element(By.ID,'wd1')
    search_in.send_keys(searchIn)
    search_box = web.find_element(By.NAME,'f1')
    search_btn = search_box.find_element(By.CLASS_NAME,'search_btn_wrap')
    search_btn.click()
    time.sleep(2)
    # 点搜索和弹出来一次，跳转网页后弹出来一次
    close_login()
    close_login()

    # 进行爬取
    items_all = []
    page = int(input('你要爬取多少页：'))
    for i in range(page):
        time.sleep(2)
        close_login()
        items_all = spider(items_all)
        # 翻页继续爬取
        nextPage()
        print("第"+str(i+1)+"爬取完毕...")


    print("所有页面爬取完毕...")
    # 保存
    save_csv(items_all)
    print("保存完毕...")



