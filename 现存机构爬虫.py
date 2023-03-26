# @Time : 2022/11/29 
# @Author : Lei Cong
# @File : 现存机构爬虫.py
# @Software : PyCharm


from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time
import pandas as pd


#获取已拥有公司信息及url，以便访问详细信息
def getname():
    driver = Chrome()
    driver.get(
        "http://www.pbc.gov.cn/zhengwugongkai/4081330/4081344/4081407/4081702/4081749/4081783/index.html")
    list_id = []
    list_name = []
    list_url = []
    for i in range(11):
        id_list = driver.find_elements(By.CSS_SELECTOR, 'span.xkzh')
        name_list = driver.find_elements(By.CSS_SELECTOR, 'span.jgmc a')
        for id, name in zip(id_list[1::], name_list):
            list_id.append(id.text)
            list_name.append(name.text)
            list_url.append(name.get_attribute('href'))
            dic_data = {
                'id': id.text,
                'name': name.text,
                'url': name.get_attribute('href')
            }
            print(dic_data)
        #自动翻页
        driver.find_element(By.XPATH, '//*[@id="9398ddc068334e17b5553540fa482a66"]/div[2]/span/div/a[3]').click()
    driver.close()
    return list_name, list_url, list_id

#写入机构详细信息
def writetext(str):
    with open('xiancundata.txt', encoding="utf-8", mode="a") as f:
        f.write(str)
        f.write('\n')
        f.write('\n')

#将所有机构信息列表写入csv
def writecsv(list_name, list_id, list_date):
    data = {
        '许可证编号': list_id,
        '公司名称': list_name,
        '更改日期': list_date
    }
    df = pd.DataFrame(data)
    df.to_csv('现存公司列表.csv', mode="a", encoding="utf-8-sig")

#爬取详细机构信息
def getdata(driver, url):
    driver.get(url)
    table_list = driver.find_elements(By.CSS_SELECTOR, 'tbody')
    # str_first = table_list[0].text
    str_last = table_list[-1].text
    print(str_last)
    writetext(str_last)




if __name__ == '__main__':
    start = time.time()
    list_name, list_url, list_id = getname()
    writecsv(list_name, list_id, list_url)
    driver = Chrome()
    for url in list_url:
        getdata(driver, url)
    end = time.time()
    print("耗时：{}".format(end-start))
