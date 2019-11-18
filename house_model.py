from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class House_detail(Base):
    #房屋明细信息
    __tablename__ = 'house_detail'

    id = Column(String(32), primary_key=True)
    house_style = Column(String(20),)
    house_floor = Column(String(20))
    house_area = Column(String(20)) 
    house_type = Column(String(20)) 
    area_in = Column(String(20))
    build_type = Column(String(20)) 
    house_ori = Column(String(20)) 
    build_year = Column(String(20)) 
    house_dec = Column(String(20)) 
    build_struct = Column(String(20))
    warm_type = Column(String(20)) 
    elevator_prop = Column(String(20))
    property_year = Column(String(20))
    elevator = Column(String(20))  
    elevator_prop = Column(String(20))
    property_year = Column(String(20))
    elevator = Column(String(20))
    house_code = Column(String(20))
    tran_type = Column(String(20))
    hang_date = Column(String(20))
    house_use = Column(String(20))
    bought_year = Column(String(20))
    own_type = Column(String(20))
    trans_amount = Column(String(20))
    trans_unit = Column(String(20))
    trans_date = Column(String(20))
    url = Column(String(20))
    remark = Column(String(20))

class House_url(Base):
    url = Column(String(50), primary_key=True)

class House_base(Base):
    #房屋基本信息
    __tablename__ = 'house_base'

    id = Column(String(32), primary_key=True)
    agent_id = Column(String(20))
    agent_name = Column(String(20))
    aver_price = Column(String(20))
    aver_price_unit = Column(String(20))
    deal_date = Column(String(20))
    deal_period = Column(String(20))
    house_area = Column(String(20))
    house_code = Column(String(20))
    house_create = Column(String(20))
    house_deco = Column(String(20))
    house_floor = Column(String(20))
    house_info = Column(String(20))
    house_name = Column(String(20))
    house_ori = Column(String(20))
    house_type = Column(String(20))
    list_price = Column(String(20))
    remark = Column(String(20))
    totle_price = Column(String(20))
    totle_price_unit = Column(String(20))

def init_db():
    engine = create_engine('sqlite:///house.db', echo=True)
    DBSession = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    #session = DBSession()