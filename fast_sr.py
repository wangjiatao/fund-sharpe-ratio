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
import time

timew=100 # time window of single fund
start='20200101' #start date of time window
end='20201231' #end date of time window
pro = ts.pro_api()

funddf=pro.fund_basic(market='O',status='L')
funddf1=funddf[funddf['fund_type'].isin(['股票型'])]

def ranksr(fundsr):
    fundsr=fundsr.sort_values(by=['sr'], ascending=False)
    return fundsr



def navp(fundcode,timew):
    navptemp1=pro.fund_nav(ts_code=fundcode)
    navptemp2=navptemp1.iloc[0:timew,3]
    navptmep2=pd.DataFrame(navptemp2)
    return navptemp2


def rp(navp):
    idx_rp=0
    rp_temp=pd.Series(np.zeros((len(navp))))
    for idx_rp in range(len(navp)-1):
        pcttemp=navp.iloc[idx_rp]/navp.iloc[idx_rp+1]-1
        rp_temp.iloc[idx_rp]=pcttemp
        idx_rp=idx_rp+1
    rpdf1=rp_temp
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
    sr=(rpmean-(rf/100))/(sigp+0.000000000001)# used for data correction: zero division
    return sr

    

amount=80 # fund amout, because of api limitation, the maximum is eighty
begin=1 # the first fund's serial number
rfdf=math.pow((1+rf(start,end)),(1/250))-1



def batch_sr(fund_code,timew,rfdf):
    idxsr=0
    sr_list=pd.DataFrame(np.zeros((amount,1)),index=fund_code)#80 fund code&sr temp cache
    for idxsr in range(len(fund_code)):
        fcode=fund_code.iloc[idxsr]
        navpdf=navp(fcode,timew)
        rpdf=rp(navpdf)
        sigpdf=sigp(rpdf)
        srtemp=sr(rpdf,sigpdf,rfdf)
        sr_list.iloc[idxsr,0]=srtemp
        idxsr=idxsr+1;
    sr_list=sr_list.rename(columns={0:'sr'})
    srlistmax=ranksr(sr_list)
    return srlistmax

fund_wl_sr=pd.DataFrame()
lenfund=len(funddf1)
idx_dl_stop=round(lenfund/80)
idx_dl=0
i=0

for i in range(idx_dl_stop):
    fund_code_temp=funddf1.iloc[begin*(i+1):(begin*(i+1))+amount,0]# batch fund code list
    flist_temp=batch_sr(fund_code_temp,timew, rfdf)
    fund_wl_sr=fund_wl_sr.append(flist_temp)
    time.sleep( 70 )
    i=i+1;

print(fund_wl_sr)

