#爬取链家成交数据
import time
import math
import uuid
import requests
import pandas as pd

from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base

from bs4 import BeautifulSoup

from house_model import House_base, House_detail

headers = {
    'Host':'hf.lianjia.com',
    'Connection':'keep-alive',
    #'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
    #'Sec-Fetch-User':'?1',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    #'Sec-Fetch-Mode':'navigate',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
}

engine = create_engine('sqlite:///house.db', echo=False)
Base = declarative_base()
DBSession = sessionmaker(bind=engine)
session = DBSession()
session_times = 0

def get_deal():
    global session, session_times, headers
    url_base = 'http://hf.lianjia.com'
    url_chengjiao_index = url_base + '/chengjiao'
    #pd_house_deal = pd.DataFrame()
    #pd_house_detail = pd.DataFrame()

    r = requests.get(url_chengjiao_index, headers=headers)
    soup_index = BeautifulSoup(r.text,'lxml')
    #获取区域信息
    for region in soup_index.find(attrs={'data-role':'ershoufang'}).find_all('a'):
        url_region = url_base + region['href']
        page_num = get_page_num(url=url_region)
        print(url_region)
        print(page_num)
        for i in range(1,page_num + 1):
            print(i)
            url_page = url_region + 'pg' + str(i)
            get_house(url_page)

    if session_times > 0:
        session.commit()
    session.close()
    
def get_page_num(url):
    global headers
    r = requests.get(url, headers=headers)
    bs = BeautifulSoup(r.text, 'lxml')
    page_num = math.ceil(int(bs.find(attrs={'class':'total fl'}).span.string.strip())/30)
    return page_num

def get_house(url):
    global headers
    r = requests.get(url, headers=headers)
    #print(r.status_code)
    #print(r.text)
    soup = BeautifulSoup(r.text, 'lxml')
    #list_content = soup.find_all(attrs={'class': 'listContent'})
    for content in soup.find(attrs={'class': 'listContent'}).contents:
        house_base = House_base()
        house_base.id = str(uuid.uuid4())
        house_base.house_name = content.find(attrs={'class':'title'}).string.split(' ')[0]
        house_base.remark = ''
        try:  
            #print(house_base.house_name)
            house_base.house_type = content.find(attrs={'class':'title'}).string.split(' ')[1]
            house_base.house_area = content.find(attrs={'class':'title'}).string.split(' ')[2]
        
            house_base.house_ori = content.find(attrs={'class':'houseInfo'}).contents[1].split(' | ')[0]
            house_base.house_deco = content.find(attrs={'class':'houseInfo'}).contents[1].split(' | ')[1]

            house_base.deal_date = content.find(attrs={'class':'dealDate'}).string

            house_base.totle_price = content.find(attrs={'class':'totalPrice'}).contents[0].string
            house_base.totle_price_unit = content.find(attrs={'class':'totalPrice'}).contents[1].string

            house_base.aver_price = content.find(attrs={'class':'unitPrice'}).contents[0].string
            house_base.aver_price_unit =  content.find(attrs={'class':'unitPrice'}).contents[1].string

            house_base.house_floor = content.find(attrs={'class':'positionInfo'}).contents[1].split(' ')[0]
            house_base.house_create = content.find(attrs={'class':'positionInfo'}).contents[1].split(' ')[1]

            house_base.house_info = ''
            if content.find(attrs={'class':'dealHouseTxt'}):
                house_base.house_info = '|'.join([i.string for i in content.find(attrs={'class':'dealHouseTxt'}).contents])

            house_base.list_price = content.find(attrs={'class':'dealCycleTxt'}).contents[0].string
            house_base.deal_period = content.find(attrs={'class':'dealCycleTxt'}).contents[1].string
            if content.find(attrs={'class':'agent_chat_btn'}):
                house_base.house_code = content.find(attrs={'class':'agent_chat_btn'}).attrs['data-lj_action_house_code']
                house_base.agent_id = content.find(attrs={'class':'agent_chat_btn'}).attrs['data-lj_action_agent_id']
                house_base.agent_name = content.find(attrs={'class':'agent_chat_btn'}).attrs['data-lj_action_agent_name']
            #pd_house_deal = pd_house_deal.append(dict_cur_house,ignore_index=True)
        
        except IndexError as e:
            house_base.remark = 'IndexError'

        save_house(house_base)

        get_house_detail(content.find(attrs={'class':'title'}).a['href'])
           
    return 


def get_house_detail(url):
    global headers
    r = requests.get(url,headers=headers)
    bs = BeautifulSoup(r.text,'lxml')
    base_content = bs.find(attrs={'class':'base'}).ul.contents
    house_detail = House_detail()
    house_detail.id = str(uuid.uuid4())
    house_detail.url = url
    house_detail.remark = ''
    
    try:
        house_detail.house_style = base_content[0].contents[1].string.strip()
        house_detail.house_floor = base_content[1].contents[1].string.strip()
        house_detail.house_area = base_content[2].contents[1].string.strip()
        house_detail.house_type = base_content[3].contents[1].string.strip()
        house_detail.area_in = base_content[4].contents[1].string.strip()
        house_detail.build_type = base_content[5].contents[1].string.strip()
        house_detail.house_ori = base_content[6].contents[1].string.strip()
        house_detail.build_year = base_content[7].contents[1].string.strip()
        house_detail.house_dec = base_content[8].contents[1].string.strip()
        house_detail.build_struct = base_content[9].contents[1].string.strip()
        house_detail.warm_type = base_content[10].contents[1].string.strip()
        house_detail.elevator_prop = base_content[11].contents[1].string.strip()
        house_detail.property_year = base_content[12].contents[1].string.strip()
        house_detail.elevator = base_content[13].contents[1].string.strip()

        tran_content = bs.find(attrs={'class':'transaction'}).ul.contents
        house_detail.house_code = tran_content[0].contents[1].string.strip()
        house_detail.tran_type = tran_content[1].contents[1].string.strip()
        house_detail.hang_date = tran_content[2].contents[1].string.strip()
        house_detail.house_use = tran_content[3].contents[1].string.strip()
        house_detail.bought_year = tran_content[4].contents[1].string.strip()
        house_detail.own_type = tran_content[5].contents[1].string.strip()

        house_detail.trans_amount = bs.find(attrs={'class':'record_price'}).string
        house_detail.trans_unit = bs.find(attrs={'class':'record_detail'}).string.split(',')[0]
        house_detail.trans_date = bs.find(attrs={'class':'record_detail'}).string.split(',')[1]

    except IndexError as e:
        house_detail.remark = 'IndexError'
    
    save_house(house_detail)

    return

def save_house(house):
    global session, session_times
    session.add(house)
    session_times += 1
    if session_times == 60:
        session.commit()
        session_times = 0

if __name__ == '__main__':
    get_deal()
