#Module Calculates and compares the security budgets of BTC and DCR
from checkonchain.dcronchain.dcr_add_metrics import *
from checkonchain.btconchain.btc_add_metrics import *
from checkonchain.dcronchain.dcr_security_model import *


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

asset = 'btc'
df['blk'] = BTC_real['blk']
df['y'] = 0.0
df['H_net'] = BTC_real['pow_hashrate_THs']
df['price'] = BTC_real['PriceUSD']
df['tic_pool'] = 0
df['tic_price'] = 0
df = dcr_security_calculate_df().calculate_df(asset,atk_blk,df)






#plt.plot('y','pow_prof',data=df)
#plt.show()

plt.plot('blk','pow_term',data=df)
plt.plot('blk','pos_term',data=df)
plt.plot('blk','pca',data=df)
plt.show()


