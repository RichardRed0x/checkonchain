#Module Calculates and compares the security budgets of BTC and DCR
from checkonchain.dcronchain.dcr_add_metrics import *
from checkonchain.btconchain.btc_add_metrics import *
from checkonchain.dcronchain.dcr_security_model import *
import os
os.getcwd()
os.chdir('D:\code_development\checkonchain\checkonchain')


#Set number of blocks to re-org
atk_blk = 1
#Set Asset to DCR and pull relevant data
DCR_real = dcr_add_metrics().dcr_real()
asset = 'dcr'
df = pd.DataFrame(columns=['blk','y','H_net','price','tic_price','tic_pool'])
count = 0
for i in range(0,100,5):
    df['blk'] = DCR_real['blk']
    df['y'] = i/100
    df['H_net'] = DCR_real['pow_hashrate_THs']
    df['price'] = DCR_real['PriceUSD']
    df['tic_pool'] = DCR_real['tic_pool']
    df['tic_price'] = DCR_real['tic_price']
    df = dcr_security_calculate_df().calculate_df(asset,atk_blk,df)
    if count ==0:
        response = df
        df = pd.DataFrame(columns=['blk','y','H_net','price','tic_price','tic_pool'])
    else:
        response = response.append(df,ignore_index=True)
        df = pd.DataFrame(columns=['blk','y','H_net','price','tic_price','tic_pool'])
    count += 1
DCR_secure = response


"""BITCOIN"""
#Extract Real Data
BTC_real = btc_add_metrics().btc_real()
BTC_hash = pd.read_csv(r"btconchain\data\btc_blockchaincom_hashrate.csv")
BTC_hash = pd.concat([BTC_hash.set_index('blk',drop=False),BTC_real.set_index('blk',drop=True)],axis=1,join='inner')
BTC_hash = BTC_hash.drop(BTC_hash.index[0])
BTC_hash.reset_index(drop=True)


asset = 'btc'
df['blk'] = BTC_hash['blk']
df['y'] = 0.0
df['H_net'] = BTC_hash['pow_hashrate_THs']
df['price'] = BTC_hash['PriceUSD']
df['tic_pool'] = 0
df['tic_price'] = 0
df = dcr_security_calculate_df().calculate_df(asset,atk_blk,df)





import requests
response = requests.get("https://blockchain.info/q/hashrate")
print(response.json())

import quandl




#plt.plot('y','pow_prof',data=df)
#plt.show()

plt.plot('blk','pow_term',data=df)
plt.plot('blk','pos_term',data=df)
plt.plot('blk','pca',data=df)
plt.show()


