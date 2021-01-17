#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 19:54:13 2021

@author: wangjiatao
"""
import tushare as ts
import pandas as pd
import numpy as np
import math 

time=100 # time window
start='20200101' #time window begining date
end='20201231' #time window end date
pro = ts.pro_api()

funddf=pro.fund_basic(market='O',status='L')
funddf1=funddf[funddf['fund_type'].isin(['股票型'])]

def ranksr(fundsr):
    fundsr=fundsr.sort_values(by=['sr'], ascending=False)
    return fundsr

def rp(navp):
    rpdf1=navp.pct_change()
    return rpdf1
            
                
def sigp(rp):
    sigmp=np.std(rp)
    return sigmp

def rf(start,end):
    rfdf1=pro.shibor(start_date=start,end_date=end)
    rfdf2=rfdf1.iloc[:,8]
    rf=np.mean(rfdf2)
    return rf


def sr (rp, sigp,rf):
    rpmean=np.mean(rp)
    sr=(rpmean-(rf/100))/sigp
    return sr

def navp(fundcode,time):
    navptemp1=pro.fund_nav(ts_code=fundcode)
    navptemp2=navptemp1.iloc[0:time,3]
    return navptemp2
    

amount=80 # fund amout, because of api limitation, the maximum is eighty
begin=100 # the first fund's serial number
fund_code=funddf1.iloc[begin:begin+amount,0]
sr_list=pd.DataFrame(np.zeros((amount,1)),index=fund_code)
rfdf=math.pow((1+rf(start,end)),(1/250))-1
idxsr=0
for idxsr in range(len(fund_code)):
    fcode=fund_code.iloc[idxsr]
    navpdf=navp(fcode,time)
    rpdf=rp(navpdf)
    sigpdf=sigp(rpdf)
    srtemp=sr(rpdf,sigpdf,rfdf)
    sr_list.iloc[idxsr,0]=srtemp
    idxsr=idxsr+1;
sr_list=sr_list.rename(columns={0:'sr'})
srlistmax=ranksr(sr_list)
print(srlistmax)
    

