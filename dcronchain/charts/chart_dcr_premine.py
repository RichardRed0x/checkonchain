# Calculate and plot pre-mine specific curves
import pandas as pd
import numpy as np

from checkonchain.dcronchain.dcr_add_metrics import *
from checkonchain.general.standard_charts import *

#Pull DataFrames
DCR_real = dcr_add_metrics().dcr_real()
#Calculate max block
blk_max = int(DCR_real['blk'][DCR_real.index[-1]])
DCR_pre = dcr_supply_schedule(0).dcr_premine(DCR_real,blk_max)


loop_data = [[0,1,2,3,4,5,6]]
x_data = [
    DCR_pre['date'],
    DCR_pre['date'],
    DCR_pre['date'],
    DCR_pre['date'],
    DCR_pre['date'],
    DCR_pre['date'],
    DCR_pre['date']
]
y_data = [
    DCR_pre['PoWSply_ideal']/DCR_pre['Sply_ideal'],
    DCR_pre['PoSSply_ideal']/DCR_pre['Sply_ideal'],
    (DCR_pre['FundSply_ideal']-1.68e6/2)/DCR_pre['Sply_ideal'],
    DCR_pre['dcr_tic_sply_avg']/DCR_pre['Sply_ideal'],
    DCR_pre['pmine_c0']/DCR_pre['Sply_ideal'],
    DCR_pre['c0_spent_pos']/DCR_pre['Sply_ideal'],
    DCR_pre['com_spent_pos']/DCR_pre['Sply_ideal']
]

name_data = [
    'PoW Theoretical Supply',
    'PoS Theoretical Supply',
    'Treasury Theoretical Supply',
    'Ticket Pool Supply',
    'Founder Total Premine',
    'Founder Spent Premine w/ Staking (46%)',
    'Community Spent Premine w/ Staking (54%)'
]
color_data = [
    'rgb(250, 38, 53)' ,
    'rgb(114, 49, 163)',
    'rgb(255, 192, 0)',
    'rgb(20, 169, 233)',
    'rgb(239, 125, 50)',
    'rgb(239, 125, 50)',
    'rgb(1, 255, 116)'
]
width_data = [2,2,2,2,2,2,2]
dash_data = ['solid','solid','solid','solid','solid','dot','dot']
opacity_data = [1,1,1,1,1,1,1]
legend_data = [True,True,True,True,True,True,True]

title_data = [
    "Decred Supply Characteristics and Premine",
    "<b>Date</b>",
    "<b>Portion of DCR Circulating Supply</b>"
    ]
range_data = [[0,1],[0,0.5]]
type_data = ['date','linear']
autorange_data = [True,False]

fig = check_standard_charts().subplot_lines_singleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data,
    )

fig.show()

