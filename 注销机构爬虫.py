# @Time : 2022/11/29 
# @Author : Lei Cong
# @File : 注销机构爬虫.py
# @Software : PyCharm

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time
import pandas as pd

#获得公司列表及URL
def getname():
    driver = Chrome()
    driver.get(
        "http://www.pbc.gov.cn/zhengwugongkai/4081330/4081344/4081407/4081702/4081749/4081786/63ead9a6/index1.html")
    list_id = []
    list_name = []
    list_url = []
    list_data = []
    for i in range(11):
        id_list = driver.find_elements(By.CSS_SELECTOR, 'span.xkzh')
        name_list = driver.find_elements(By.CSS_SELECTOR, 'span.jgmc a')
        date_list = driver.find_elements(By.CSS_SELECTOR, 'span.date')
        for id, name, date in zip(id_list[1::], name_list, date_list[1::]):
            list_id.append(id.text)
            list_name.append(name.text)
            list_url.append(name.get_attribute('href'))
            list_data.append(date.text)
            dic_data = {
                'id': id.text,
                'name': name.text,
                'url': name.get_attribute('href'),
                'date': date.text
            }
            print(dic_data)
        #实现自动翻页
        driver.find_element(By.XPATH, '//*[@id="63ead9a6bb4b42c3a55d82eb9da4383e"]/div[2]/span/div/a[3]').click()
    driver.close()
    return list_name, list_url, list_id, list_data

#写入详细公司信息
def writetext(str):
    with open('zhuxiaodata.txt', encoding="utf-8", mode="a") as f:
        f.write(str)
        f.write('\n')
        f.write('\n')

#将公司列表写入
def writecsv(list_name, list_id, list_date, list_url):
    data = {
        '许可证编号': list_id,
        '公司名称': list_name,
        '注销日期': list_date,
        'url': list_url
    }
    df = pd.DataFrame(data)
    df.to_csv('注销公司列表.csv', mode="a", encoding="utf-8-sig")

#爬取公司详细信息
def getdata(driver, url):
    driver.get(url)
    table_list = driver.find_elements(By.CSS_SELECTOR, 'tbody')
    str_first = table_list[0].text
    writetext(str_first)
    print(str_first)


if __name__ == '__main__':
    #计时函数
    start = time.time()
    list_name, list_url, list_id, list_date = getname()
    writecsv(list_name, list_id, list_date, list_url)
    driver = Chrome()
    for url in list_url:
        getdata(driver, url)
    end = time.time()
    print("耗时：{}".format(end - start))
