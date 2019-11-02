#Permabulls Charts
from checkonchain.general.standard_charts import *
from checkonchain.dcronchain.dcr_add_metrics import *

DCR_real = dcr_add_metrics().dcr_pricing_models()#

loop_data = [[0,1,2,3,4],[5]]
x_data = [
    DCR_real['date'],DCR_real['date'],DCR_real['date'],DCR_real['date'],
    DCR_real['date'],DCR_real['date']
    ]
y_data = [
    DCR_real['PoW_income_usd'].cumsum()/DCR_real['SplyCur'],
    DCR_real['PoS_income_usd'].cumsum()/DCR_real['SplyCur'],
    DCR_real['Fund_income_usd'].cumsum()/DCR_real['SplyCur'],
    DCR_real['Total_income_usd'].cumsum()/DCR_real['SplyCur'],
    DCR_real['CapMrktCurUSD']/DCR_real['SplyCur'],
    DCR_real['DiffMean']
    ]
name_data = [
    'POW','POS','Treasury','Total',
    'Market Cap','Difficulty Ribbon'
    ]
color_data = [
    'rgb(250, 38, 53)' ,'rgb(114, 49, 163)','rgb(255, 192, 0)',
    'rgb(20, 169, 233)','rgb(239, 125, 50)','rgb(156,225,143)']
dash_data = ['solid','solid','solid','solid','solid','solid']
width_data = [2,2,2,2,2,1]
opacity_data = [1,1,1,1,1,1]
legend_data = [True,True,True,True,True,True]#
title_data = ['Decred Block Subsidy Paid Valuations','Date','Network Valuation','Difficulty']
range_data = [['01-02-2016','01-02-2020'],[-2,3],[0,1]]
autorange_data = [True,False,True]
type_data = ['date','log','log']#
fig = check_standard_charts(
    title_data,range_data,type_data,autorange_data    
    ).subplot_lines_doubleaxis(
        loop_data,
        x_data,
        y_data,
        name_data,
        color_data,
        dash_data,
        width_data,
        opacity_data,
        legend_data
    )

for i in [9,14,25,40,60,90,128,200]:
    fig.add_trace(go.Scatter(
        mode='lines',
        x=DCR_real['date'], 
        y=DCR_real['DiffMean'].rolling(i).mean(),
        name='Difficulty '+str(i),
        opacity=0.5,
        showlegend=False,
        line=dict(
            width=i/200*2,
            color='rgb(156,225,143)',
            dash='solid'
            )),
        secondary_y=True)

fig.show()





loop_data = [[0,1,2,3,4],[5]]
x_data = [
    DCR_real['date'],DCR_real['date'],DCR_real['date'],DCR_real['date'],
    DCR_real['date'],DCR_real['date']
    ]
y_data = [
    DCR_real['PoW_income_usd'].cumsum()/DCR_real['SplyCur'],
    DCR_real['PoS_income_usd'].cumsum()/DCR_real['SplyCur'],
    DCR_real['Fund_income_usd'].cumsum()/DCR_real['SplyCur'],
    DCR_real['Total_income_usd'].cumsum()/DCR_real['SplyCur'],
    DCR_real['CapMrktCurUSD']/DCR_real['SplyCur'],
    DCR_real['ticket_pool_value']
    ]
name_data = [
    'POW','POS','Treasury','Total',
    'Market Cap','Ticket Pool Value'
    ]
color_data = [
    'rgb(250, 38, 53)' ,'rgb(114, 49, 163)','rgb(255, 192, 0)',
    'rgb(20, 169, 233)','rgb(239, 125, 50)','rgb(156,225,143)']
dash_data = ['solid','solid','solid','solid','solid','solid']
width_data = [2,2,2,2,2,2]
opacity_data = [1,0.5,0.5,0.5,0.5,1]
legend_data = [True,True,True,True,True,True]#
title_data = ['Decred Security Resilience','Date','Network Valuation','Total DCR in Tickets']
range_data = [['01-02-2016','01-02-2020'],[-2,3],[0,1]]
autorange_data = [True,False,True]
type_data = ['date','log','linear']#
fig = check_standard_charts(
    title_data,range_data,type_data,autorange_data    
    ).subplot_lines_doubleaxis(
        loop_data,
        x_data,
        y_data,
        name_data,
        color_data,
        dash_data,
        width_data,
        opacity_data,
        legend_data
    )

fig.show()
