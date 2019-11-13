#Onchain DCR Volumes
from checkonchain.general.standard_charts import *
from checkonchain.dcronchain.dcr_add_metrics import *

DCR_subs = dcr_add_metrics().dcr_ticket_models()


loop_data = [[0,1,2,3,4],[]]
x_data = [
    DCR_subs['date'],
    DCR_subs['date'],
    DCR_subs['date'],
    DCR_subs['date'],
    DCR_subs['date'],

    ]
y_data = [
    DCR_subs['PoW_income_usd'].cumsum()/DCR_subs['SplyCur'],
    DCR_subs['PoS_income_usd'].cumsum()/DCR_subs['SplyCur'],
    DCR_subs['Fund_income_usd'].cumsum()/DCR_subs['SplyCur'],
    DCR_subs['Total_income_usd'].cumsum()/DCR_subs['SplyCur'],
    DCR_subs['CapMrktCurUSD']/DCR_subs['SplyCur'],

]
name_data = [
    'POW','POS','Treasury','Total',
    'Market Cap'
    ]
color_data = [
    'rgb(250, 38, 53)' ,'rgb(114, 49, 163)','rgb(255, 192, 0)',
    'rgb(20, 169, 233)','rgb(239, 125, 50)','rgb(156,225,143)']
dash_data = ['solid','solid','solid','solid','solid','solid']
width_data = [2,2,2,2,2,2]
opacity_data = [1,1,1,1,1,1]
legend_data = [True,True,True,True,True,True]#
title_data = ['Decred Block Subsidy Models and On-chain Volume','Date','DCR/USD Price','DCR On-chain Volume']
range_data = [['01-02-2016','01-02-2020'],[-2,3],[0,500e6]]
autorange_data = [True,False,True]
type_data = ['date','log','linear']#
fig = check_standard_charts().subplot_lines_doubleaxis(
    title_data, range_data ,autorange_data ,type_data,
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


x_data = [
    DCR_subs['date'],
    DCR_subs['date']
]
y_data = [
    DCR_subs['dcr_tic_vol'],
    DCR_subs['dcr_tfr_vol']
]
loop_data = [0,1]
name_data = ['Ticket Vol (DCR)','Transfer Vol (DCR)']
for i in loop_data:
    fig.add_trace(
        go.Bar(x=x_data[i],y=y_data[i],name=name_data[i]),secondary_y=True)
fig.update_layout(barmode='stack',bargap=0.01)



for i in [9,14,25,40,60,90,128,200]:
    fig.add_trace(go.Scatter(
        mode='lines',
        x=DCR_subs['date'], 
        y=DCR_subs['DiffMean'].rolling(i).mean(),
        name='Difficulty '+str(i),
        opacity=0.5,
        showlegend=False,
        line=dict(
            width=i/200*2,
            color='rgb(156,225,143)',
            dash='solid'
            )),
        secondary_y=False)

fig.show()