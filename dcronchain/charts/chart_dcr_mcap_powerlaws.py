#Calculate the Linear Regression between Market Caps
import pandas as pd
import numpy as np
import datetime as date
today = date.datetime.now().strftime('%Y-%m-%d')

from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "browser"

from checkonchain.general.coinmetrics_api import *
from checkonchain.btconchain.btc_add_metrics import *
from checkonchain.dcronchain.dcr_add_metrics import *

from checkonchain.general.regression_analysis import *

#Pull Coinmetrics Data for Coins
BTC = btc_add_metrics().btc_coin()
LTC = Coinmetrics_api('ltc',"2011-10-07",today).convert_to_pd()
BCH = Coinmetrics_api('bch',"2017-08-01",today).convert_to_pd()
DAS = Coinmetrics_api('dash',"2014-01-19",today).convert_to_pd()
DCR = dcr_add_metrics().dcr_coin()
XMR = Coinmetrics_api('xmr',"2014-04-18",today).convert_to_pd()
ZEC = Coinmetrics_api('zec',"2016-10-28",today).convert_to_pd()
ETH = Coinmetrics_api('eth',"2015-07-30",today).convert_to_pd()
XRP = Coinmetrics_api('xrp',"2013-01-01",today).convert_to_pd()

#Reduce dataset down to date and a single metric
metric="CapMrktCurUSD"
BTC2 =BTC[['date',metric]]
LTC2 =LTC[['date',metric]] 
BCH2 =BCH[['date',metric]] 
DAS2 =DAS[['date',metric]]
DCR2 =DCR[['date',metric]] 
XMR2 =XMR[['date',metric]] 
ZEC2 =ZEC[['date',metric]] 
ETH2 =ETH[['date',metric]] 
#XRP2 =XRP[['date',metric]] 

#Rename all columns
prefix = 'Cap_'
BTC2.columns =['date',prefix+'BTC'] 
LTC2.columns =['date',prefix+'LTC']
BCH2.columns =['date',prefix+'BCH']
DAS2.columns=['date',prefix+'DAS']
DCR2.columns =['date',prefix+'DCR']
XMR2.columns =['date',prefix+'XMR']
ZEC2.columns =['date',prefix+'ZEC']
ETH2.columns =['date',prefix+'ETH']
XRP2.columns =['date',prefix+'XRP']

#Compile into a single dataframe with all coins
BTC_data  = BTC2.dropna(axis=0)
BTC_data  = pd.merge_asof(BTC_data,LTC2,on='date')
BTC_data  = pd.merge_asof(BTC_data,BCH2,on='date')
BTC_data  = pd.merge_asof(BTC_data,DAS2,on='date')
BTC_data  = pd.merge_asof(BTC_data,DCR2,on='date')
BTC_data  = pd.merge_asof(BTC_data,XMR2,on='date')
BTC_data  = pd.merge_asof(BTC_data,ZEC2,on='date')
BTC_data  = pd.merge_asof(BTC_data,ETH2,on='date')
BTC_data  = pd.merge_asof(BTC_data,XRP2,on='date')

BTC_data

regression_analysis().ln_regression(BTC_data[['date',prefix+'BTC',prefix+'LTC']].dropna(axis=0),prefix+'BTC',prefix+'LTC','date')
regression_analysis().ln_regression(BTC_data[['date',prefix+'BTC',prefix+'BCH']].dropna(axis=0),prefix+'BTC',prefix+'BCH','date')
regression_analysis().ln_regression(BTC_data[['date',prefix+'BTC',prefix+'DAS']].dropna(axis=0),prefix+'BTC',prefix+'DAS','date')
regression_analysis().ln_regression(BTC_data[['date',prefix+'BTC',prefix+'DCR']].dropna(axis=0),prefix+'BTC',prefix+'DCR','date')
regression_analysis().ln_regression(BTC_data[['date',prefix+'BTC',prefix+'XMR']].dropna(axis=0),prefix+'BTC',prefix+'XMR','date')
regression_analysis().ln_regression(BTC_data[['date',prefix+'BTC',prefix+'ZEC']].dropna(axis=0),prefix+'BTC',prefix+'ZEC','date')
regression_analysis().ln_regression(BTC_data[['date',prefix+'BTC',prefix+'ETH']].dropna(axis=0),prefix+'BTC',prefix+'ETH','date')
regression_analysis().ln_regression(BTC_data[['date',prefix+'BTC',prefix+'XRP']].dropna(axis=0),prefix+'BTC',prefix+'XRP','date')



x_data = [
    BTC_data[prefix+'DCR'],BTC_data[prefix+'LTC'],
    BTC_data[prefix+'BCH'],BTC_data[prefix+'DAS'],
    BTC_data[prefix+'XMR'],BTC_data[prefix+'ZEC'],
    BTC_data[prefix+'ETH'],BTC_data[prefix+'XRP']
    ]
y_data = [
    BTC_data[prefix+'BTC'],BTC_data[prefix+'BTC'],
    BTC_data[prefix+'BTC'],BTC_data[prefix+'BTC'],
    BTC_data[prefix+'BTC'],BTC_data[prefix+'BTC'],
    BTC_data[prefix+'BTC'],BTC_data[prefix+'BTC']
    ]
name_data = [
    'DCR','LTC',
    'BCH','DAS',
    'XMR','ZEC',
    'ETH','XRP'
]
width_data = [
    2,2,
    2,2,
    2,2,
    2,2
]
opacity_data = [
    1,1,
    1,1,
    1,1,
    1,1
]
color_data = [
    'rgb(255, 153, 0)','rgb(214, 214, 194)',
    'rgb(0, 153, 51)','rgb(51, 204, 255)',
    'rgb(255, 102, 0)','rgb(255, 255, 0)',
    'rgb(153, 51, 255)','rgb(51, 102, 255)'
]
dash_data = [
    'solid','solid',
    'solid','solid',
    'solid','solid',
    'solid','solid'
]


fig = make_subplots(specs=[[{"secondary_y": False}]])
for i in range(0,8):
    fig.add_trace(go.Scatter(
        x=x_data[i], y=y_data[i],
        mode='markers',
        name=name_data[i],
        opacity=opacity_data[i],
        marker=dict(
            width=width_data[i],
            color=color_data[i]#,
            #dash=dash_data[i]
            )),
        secondary_y=False)



"""$$$$$$$$$$$$$$$ FORMATTING $$$$$$$$$$$$$$$$"""
# Add figure title
fig.update_layout(title_text="Compare Value Metrics")
fig.update_xaxes(
    title_text="<b>Coin MCap</b>",
    type = 'log'
    )
fig.update_yaxes(
    title_text="<b>Bitcoin MCap</b>",
    type="log",
    #range=[8,12],
    secondary_y=False)
fig.update_layout(template="plotly_dark")
fig.show()
