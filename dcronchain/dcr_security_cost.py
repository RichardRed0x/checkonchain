import numpy as np
import pandas as pd
import random
import math

from checkonchain.dcronchain.dcr_add_metrics import *

decred_d9 = 1916 # $ per TH - ASIC capital cost
pow_pools = [
    ['uupool.cn/dcr',0.2681],
    ['poolin.com',0.1817],
    ['f2pool.com',0.1364],
    ['lab.antpool.com',0.0709],
    ['pool.btc.com',0.0291],
    ['decred.luxor.tech',0.0246],
    ['coinmine.pl/dcr',0.0011],
    ['beepool.org',0.0004],
    ['dcr.suprnova.cc',0.0002],
    ['others',0.2876]
]

def dcr_staketohash(atk_stake):
    atk_hash = (6*(1-atk_stake)**5-15*(1-atk_stake)**4+10*(1-atk_stake)**3)/(6*atk_stake**5-15*atk_stake**4+10*atk_stake**3)
    return atk_hash

def dcr_hashtostake(atk_hash):
    atk_hash = (6*(1-atk_stake)**5-15*(1-atk_stake)**4+10*(1-atk_stake)**3)/(6*atk_stake**5-15*atk_stake**4+10*atk_stake**3)
    return atk_hash





pow_pools = pd.DataFrame(data=pow_pools,columns=['pool','atk_hash'])
pow_pools['atk_stake'] = dcr_hashtostake(pow_pools['atk_hash'])


data = [0.01,0.05,0.10,0.20,0.30,0.40,0.45,0.50,0.55,0.60,0.70,0.80,0.90,0.95,1.00]
DCR_secure=pd.DataFrame(data=data,columns=['atk_stake'])
DCR_secure['atk_hash'] = dcr_staketohash(DCR_secure['atk_stake'])

DCR_real = dcr_add_metrics().dcr_real()
DCR_real = DCR_real[['date','blk','S2F','ticket_count','ticket_price','ticket_pool_value','ticket_pool_size','pow_hashrate_THs','pow_diff','circulation','PriceUSD']]
DCR_real = DCR_real.dropna()


pos_cost = pd.DataFrame()
pow_cost = pd.DataFrame()

for i in DCR_secure['atk_stake']:
    pos_cost[str(i)] = i * DCR_real['ticket_pool_value'] * DCR_real['PriceUSD']
    pow_cost[str(i)] = dcr_staketohash(i) * DCR_real['pow_hashrate_THs'] * 1916
    DCR_real[str(i)] = pos_cost[str(i)] + pow_cost[str(i)]


from checkonchain.general.standard_charts import *
DCR_real.columns
x_data = [DCR_real['date'],DCR_real['date'],DCR_real['date'],DCR_real['date'],DCR_real['date']]
y_data = [DCR_real['0.1'],DCR_real['0.3'],DCR_real['0.5'],DCR_real['0.6'],DCR_real['0.9']]
name_data = ['10%','30%','50%','60%','90%']

fig = make_subplots(specs=[[{"secondary_y": False}]])
for i in range(0,5):
    fig.add_trace(go.Scatter(
        x=x_data[i], 
        y=y_data[i],
        mode='lines',
        name=name_data[i]),
        secondary_y=False)

"""$$$$$$$$$$$$$$$ FORMATTING $$$$$$$$$$$$$$$$"""
# Add figure title
fig.update_layout(title_text="Decred Cost to Attack")
fig.update_xaxes(
    title_text="<b>date</b>",
    type='date'
    )
fig.update_yaxes(
    title_text="<b>USD to Attack</b>",
    secondary_y=False,
    type='log')
fig.update_layout(template="plotly_dark")
fig.show()


















## Params
#tic_pl = 40960
#runs = 500
#tic = pd.DataFrame()
##Analysis df
#df = pd.DataFrame(data=np.arange(runs),columns=['blk'])
#
##Stk probabilities
#probs = np.arange(0.05,1,0.05)
#atk_prob = pd.DataFrame(data=probs,columns=['atk_stk'])
#atk_prob['atk_prob']=0
#atk_prob['atk_wrk']=0
##atk_dfs = {}
#
#df['pool'] = 0
#for i in range(0,runs):
#    df.loc[i,['pool']] = random.randint(int(tic_pl*0.995),int(tic_pl*1.005)) #Temp Pool num
#
#
#
#def compute_tic_num(_seed,_pool):
#    random.seed(a=_seed)
#    return random.randint(1,_pool)
#    
#
##Calculate for each probability
#for k in range(0,len(atk_prob.index)):
#    df['atk_pool'] = float(atk_prob.loc[k,['atk_stk']])*df['pool']
#    df['atk_pool'] = df['atk_pool'].apply(np.ceil)
#
#
#    # Setup empty Dataframes
#    for j in range(1,6):
#        print(j)
#        #Set tic # col
#        name = 'tic_'+ str(j)
#        df[name] = 0
#        #Create Pass criteria --> Default = False
#        name = 'tic_'+ str(j)
#        name_pass = name + 'pass'
#        df[name_pass] = False
#    
#        # Calc called tic # and check if honest
#        for i in range(0,runs):
#            random.seed(a=int(df.loc[i,['blk']]+j)) #Set random seed off blk and tic 1-5
#            df.loc[i,[name]] = random.randint(1,int(df.loc[i,['pool']])) #Calc ticket number
#            #Check if hon or atk
#            if int(df.loc[i,[name]]) <= int(df.loc[i,['atk_pool']]):
#                df.loc[i,[name_pass]] = True
#
#    # Drop any duplicates
#    df.drop_duplicates(['tic_1','tic_2','tic_3','tic_4','tic_5'],keep='first')
#    # Calc number of atk_vote
#    df['atk_votes'] = df[['tic_1pass','tic_2pass','tic_3pass','tic_4pass','tic_5pass']].sum(1)
#    # Check if Pass?
#    df.loc[df.atk_votes >= 3, 'atk_suc'] = True
#    df.loc[df.atk_votes < 3, 'atk_suc'] = False 
#
#    atk_prob.loc[k,['atk_prob']] = float(np.sum(df['atk_suc'])/runs)
#    atk_prob[['atk_wrk']] = 1/atk_prob[['atk_prob']]
#
#    #store dataframe inside 
#    #atk_prob['df'] = df
#    print('for atk_stk = ',float(atk_prob.loc[k,['atk_stk']]),', success prob = ',float(atk_prob.loc[k,['atk_prob']]))
#    
#atk_prob
#
## https://towardsdatascience.com/how-to-use-pandas-the-right-way-to-speed-up-your-code-4a19bd89926d
## https://towardsdatascience.com/how-to-make-your-pandas-loop-71-803-times-faster-805030df4f06