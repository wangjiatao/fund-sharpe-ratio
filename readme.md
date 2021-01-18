# readme

## 概述：
通过计算夏普比率选出优选基金。
$R_{f}$=mean of 10 year shibor quoted data
$R_{p}$:季度和年度2个时间窗口
$\sigma_{p}$: keeping same time window with return of portfolio.
in my view, the static sharpe ratio with annual time window would better than the quarterly one. 

for fast sr calculating: time window=100 trading days.

## steps
1. def sr(rp, sigp, rf) : calculating sharpe ratio
2. portfolio_watchlist.pd=\[\] : initialing blank list of watching list
3. def rp(navp): portfolio return 
4. def sigp(rp): portfolio sigma
5. def rf(govb): downloading and calculating 10 year government bond yield
6. def navp(fundcode, begin, end): download fund nav data
7. time window: setting time window period
8. filiter: fund_type=stock, status=L


-----
##log:
1. 20200118: update: breaking api download limitation and adding automatic collected module. But, the outcome of this demo have some flaw with special short term fund, whose return and sigma data are too small to make an efficient conclusion--small sample bias.
