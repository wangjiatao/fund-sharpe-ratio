#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 18:33:46 2021

@author: wangjiatao
"""


import tushare as ts
import pandas as pd
import numpy as np

pro = ts.pro_api("")

# In[]


def fsr (rp, sigp,rf):
    sr=(rp-rf)/sigp
    return sr

pwl=pd.DataFrame()

def rp(navp):
    rp=navp.pct_change
    return rp


def sigp(rp, time_window):
    sigp_t1=len(rp)
    sigp_t2=round(sigp_t1/time_window)+1
    idx_sigp=1
    sigp=[]
    for i in range(sigp_t2):
        sigp_temp=rp.iloc[i-1:time_window*1,:]
        sigp=sigp+sigp_temp
        i=i+1
    return sigp

def rf(govb,time_window):
    rf=govb.rolling(time_window).mean()
    return rf

def navp(fundcode):
    navp_df=pro.fund_nav(ts_code='fundcode')
    return navp_df


        
    
    
    
    
    
    
    
# In[]
#downloadling data and cleaning
time_window=90

funddf1=pro.fund_basic(market='O',status='L')

fund_code=funddf1.iloc[:,0]


navpdf=


