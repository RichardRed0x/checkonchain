import pandas as pd
import numpy as np
from checkonchain.general.standard_charts import *

ZEN_data = pd.read_csv(r"D:\code_development\checkonchain\checkonchain\misc\data\ZEN_blockchain_metrics_20191204.csv")
ZEN_data['total_staked'] = 42*ZEN_data['secure_nodes']+500*ZEN_data['super_nodes']
ZEN_data['total_staked_ratio'] = ZEN_data['total_staked']/ZEN_data['supply']
ZEN_data.columns


"""
#############################################################################
                    ZEN Node Count and Hashrate
#############################################################################
"""
loop_data = [[0,1,2],[3]]
x_data = [
    ZEN_data['blockheight'],
    ZEN_data['blockheight'],
    ZEN_data['blockheight'],
    ZEN_data['blockheight'],
]
y_data = [
    ZEN_data['secure_nodes'],
    ZEN_data['super_nodes'],
    ZEN_data['total_nodes'],
    ZEN_data['nethash'],
]
name_data = [
    'Secure Node Count','Super Node Count','Total Nodes',
    'Hash-rate',
]
title_data = [
    'Horizen Analysis','Block Height','Node Count','Hash-rate'
]
type_data = [
    'linear','linear','linear'
]
fig = check_standard_charts().basic_chart(
    x_data,
    y_data,
    name_data,
    loop_data,
    title_data,
    type_data
)
fig.show()

"""
#############################################################################
                    ZEN Supply Conditions
#############################################################################
"""

loop_data = [[0,1,2,3],[4]]
x_data = [
    ZEN_data['blockheight'],
    ZEN_data['blockheight'],
    ZEN_data['blockheight'],
    ZEN_data['blockheight'],
    ZEN_data['blockheight'],
]
y_data = [
    ZEN_data['total_reward_to_miners'],
    ZEN_data['total_reward_to_foundation'],
    ZEN_data['total_reward_to_secure_nodes'],
    ZEN_data['total_reward_to_super_nodes'],
    ZEN_data['total_staked_ratio']
]
name_data = [
    'PoW Miners','Foundation','Secure Nodes','Super Nodes',
    'Total Stake Ratio'
]
title_data = [
    'Horizen Supply Curves','Block Height','Supply (ZEN)','% of Supply Staked'
]
type_data = [
    'linear','linear','linear'
]
fig = check_standard_charts().basic_chart(
    x_data,
    y_data,
    name_data,
    loop_data,
    title_data,
    type_data
)
fig.update_yaxes(range=[0,10e6],secondary_y=False)
fig.update_yaxes(range=[0,0.5],secondary_y=True)
fig.show()





"""
#############################################################################
                    ZEN Transactions
#############################################################################
"""

ZEN_data2 = ZEN_data[ZEN_data['tx_volume']>1]

loop_data = [[3,4],[0,1,2]]
x_data = [
    ZEN_data['blockheight'],
    ZEN_data['blockheight'],
    ZEN_data['blockheight'],
    ZEN_data['blockheight'],
    ZEN_data['blockheight'],
]
y_data = [
    ZEN_data['tx_sprout'],
    ZEN_data['tx_transparent'],
    ZEN_data['tx_volume'],
    ZEN_data['supply_transparent_pool'],
    ZEN_data['supply_sprout_pool']
]
name_data = [
    'Shielded Tx','Transparent Tx','Tx Volume',
    'Supply Transparent','Supply Shielded'
]
title_data = [
    'Horizen Supply','Block Height','Supply (ZEN)','Transaction Volume (ZEN)'
]
type_data = [
    'linear','linear','linear'
]
fig = check_standard_charts().basic_chart(
    x_data,
    y_data,
    name_data,
    loop_data,
    title_data,
    type_data
)
fig.update_yaxes(range=[0,10e6],secondary_y=False)
fig.update_yaxes(range=[0,1500],secondary_y=True)
fig.show()









