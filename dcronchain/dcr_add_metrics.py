# Calculate a Suite of Decred Specific Metrics
#Data Science
import pandas as pd
import numpy as np
import math
import datetime as date
today = date.datetime.now().strftime('%Y-%m-%d')

from checkonchain.general.coinmetrics_api import * #Coinmetrics.io
from checkonchain.general.regression_analysis import *
from checkonchain.dcronchain.dcr_schedule import * #DCR Schedule
from checkonchain.dcronchain.dcr_dcrdata_api import * #DCRdata.org

import os
os.getcwd()
os.chdir('D:\code_development\checkonchain\checkonchain')

"""ROADMAP
Functions pull data from relevant APIs and combine into useful datasets

Current APIs supported
    - Coinmetrics
    - dcrdata

Functions Available
dcr_coin            = coinemtrics with supplemented price data from early data sources
dcr_sply            = theoretical supply curve with added S2F model
dcr_sply_curtailed  = dcr_sply curtailed to 0.667 days to reduce df size (reduce load on charts)
dcr_diff            = dcrdata difficulty for PoS and PoW. Data setup in 144 block windows 
                        ['blk','window','time','tic_cnt_window','tic_price','tic_miss','pow_diff']
dcr_perf            - dcrdata blockchain performance 
                        ['blk','time','dcr_sply','dcr_tic_sply','tic_part','tic_pool','tic_blk','pow_hashrate_THs','pow_work_EH']

"""

class dcr_add_metrics():
    
    def __init__(self):
        self.topcapconst    = 12 #Top Cap = topcapconst * Avg Cap
        self.blkrew_ratio   = [0.6,0.3,0.1] #PoW,PoS,Fund Block Reward Fraction
        self.sply_curtail   = 6144 / 32 #reduce dataset = 0.667days
        self.dust_limit     = 100 #set Decred dust limit in bytes

    def dcr_coin(self): 
        """
        Pulls Coinmetrics v2 API Community
            Adds age metric (days)
            Adds Bittrex early price data not included in coinmetrics from csv
        """    
        df = Coinmetrics_api('dcr',"2016-02-08",today).convert_to_pd()
        #Calculate coin age since launch in days
        df['age'] = (df[['date']] - df.loc[0,['date']])/np.timedelta64(1,'D')
        print('...adding PriceUSD and CapMrktCurUSD for $0.49 (founders, 8/9-Feb-2016)')
        print('and Bittrex (10-02-2016 to 16-05-2016)...')
        #Import Early price data --> founders $0.49 for 8/9 Feb 2016 and Bitrex up to 16-May-2016 (saved in relative link csv)
        df_early = pd.read_csv(r"dcronchain\resources\data\dcr_pricedata_2016-02-08_2016-05-16.csv")
        df_early['date'] = pd.to_datetime(df_early['date'],utc=True) #Convert to correct datetime format
        df['notes'] = str('') # add notes for storing data
        for i in df_early['date']: #swap in early price data
            df.loc[df.date==i,'PriceUSD'] = float(df_early.loc[df_early.date==i,'PriceUSD'])
            df.loc[df.date==i,'PriceBTC'] = float(df_early.loc[df_early.date==i,'PriceBTC'])
            df.loc[df.date==i,'CapMrktCurUSD'] = (
                df.loc[df.date==i,'PriceUSD'] * 
                df.loc[df.date==i,'SplyCur']
            )
            df.loc[df.date==i,'notes'] = df_early.loc[df_early.date==i,'notes']
        # Restructure final dataset
        df = df[[
            'date', 'blk','age','btc_blk_est',
            'DailyIssuedNtv', 'DailyIssuedUSD', 'inf_pct_ann', 'S2F',
            'AdrActCnt', 'BlkCnt', 'BlkSizeByte', 'BlkSizeMeanByte',
            'CapMVRVCur', 'CapMrktCurUSD', 'CapRealUSD', 'DiffMean', 
            'FeeMeanNtv','FeeMeanUSD', 'FeeMedNtv', 'FeeMedUSD', 'FeeTotNtv', 'FeeTotUSD',
            'PriceBTC', 'PriceUSD', 'PriceRealised', 'SplyCur',
            'TxCnt', 'TxTfrCnt', 'TxTfrValAdjNtv', 'TxTfrValAdjUSD',
            'TxTfrValMeanNtv', 'TxTfrValMeanUSD', 'TxTfrValMedNtv',
            'TxTfrValMedUSD', 'TxTfrValNtv', 'TxTfrValUSD',
            'notes'
            ]]
        return df

    def dcr_diff(self):
        """
        Pulls dcrdata Difficulty data
        """
        df = dcrdata_api().dcr_difficulty()
        return df

    def dcr_perf(self):
        """
        Pulls dcrdata Performance data
        """
        df = dcrdata_api().dcr_performance()
        return df
        
    def dcr_sply(self,to_blk): #Calculate Theoretical Supply Curve
        """
        Calculate the theoretical supply curve
        """
        df = dcr_supply_schedule(to_blk).dcr_supply_function()
        #Calculate projected S2F Models Valuations (Uses defined constants in general.regression_analysis)
        dcr_s2f_model           = regression_analysis().regression_constants()['dcr_s2f']
        df['CapS2Fmodel']       = (
            np.exp( float(dcr_s2f_model['coefficient']) * 
            np.log(df['S2F_ideal']) + float(dcr_s2f_model['intercept'])))
        df['PriceS2Fmodel']     = df['CapS2Fmodel'] / df['Sply_ideal']
        #Calculate dust limit price according to S2F model
        df['dust_limit_S2F'] = df['PriceS2Fmodel']/1e8 * self.dust_limit

        #Calc S2F Model - Bitcoin Plan B Model
        planb_s2f_model         = regression_analysis().regression_constants()['planb']
        df['CapPlanBmodel']     = (
            np.exp( float(planb_s2f_model['coefficient']) * 
            np.log(df['S2F_ideal']) + float(planb_s2f_model['intercept'])))
        df['PricePlanBmodel']   = df['CapPlanBmodel']/df['Sply_ideal']        
        
        return df

    def dcr_sply_curtailed(self,to_blk):
        """
        Curtail theoretical supply curve for charting
        """
        dcr_sply_interval = self.sply_curtail
        df = self.dcr_sply(to_blk)
        return df.iloc[::dcr_sply_interval,:] #Select every 

    def dcr_natv(self):
        """
        Compile dcrdata sets difficulty and performance
        Final dataset is by block
        Difficulty is filled backwards (step function)
        """
        _diff = self.dcr_diff() #Pull dcrdata difficulty
        _perf = self.dcr_perf() #Pull dcrdata performance
        # DCR_natv = merge _diff (by window) to _perf (by blk)
        df = pd.merge(
            _perf.drop(['time'],axis=1),
            _diff.drop(['time','tic_miss'],axis=1),
            on='blk',how='left')
        # Fill backwards for difficulty metrics
        df[['tic_price','pow_diff','window']] = df[
            ['tic_price','pow_diff','window']
            ].fillna(method='bfill')
        # Restructure final dataset
        df = df[[
            'blk', 'window',
            'tic_cnt_window', 'tic_price', 'tic_blk', 'tic_pool',
            'dcr_tic_sply', 'dcr_sply',
            'pow_diff','pow_hashrate_THs', 'pow_work_TH'
        ]]
        return df

    def dcr_real(self):
        print('...Combining Decred specific metrics - (coinmetrics + dcrdata)...')
        _coin = self.dcr_coin() #Coinmetrics by date
        _natv = self.dcr_natv() #dcrdata API by block
        #_blk_max = int(_coin['blk'][_coin.index[-1]])
        #Cull _coin to Key Columns
        _coin = _coin[[
            'date','blk','age','CapMrktCurUSD','CapRealUSD',
            'DiffMean','PriceBTC','PriceUSD','PriceRealised',
            'SplyCur','DailyIssuedNtv','DailyIssuedUSD','S2F',
            'inf_pct_ann','TxTfrValNtv','TxTfrValUSD']]
        #Calculate sum of tickets and avg tic price per day
        _coin['tic_day'] = _coin['tic_price_avg']=0.0
        blk_from = 0 #Captures last _coin block (block from)
        _row = 0 #captures current blk (natv is by block)
        for i in _coin['blk']:
            #Sum tickets bought on the day
            _coin.loc[_row,['tic_day']]         = float(_natv.loc[blk_from:i,['tic_blk']].sum()) #tickets bought that day
            _coin.loc[_row,['tic_price_avg']]   = float(_natv.loc[blk_from:i,['tic_price']].mean()) #avg tic price that day
            blk_from = i
            _row += 1
        #Merge _coin and _natv
        df = pd.merge(_coin,_natv.drop(['tic_cnt_window'],axis=1),on='blk',how='left')
        df = df[[
            'date', 'blk', 'age','window',
            'CapMrktCurUSD', 'CapRealUSD','PriceBTC', 'PriceUSD', 'PriceRealised', 
            'DailyIssuedNtv','DailyIssuedUSD','TxTfrValNtv','TxTfrValUSD',
            'S2F', 'inf_pct_ann','SplyCur','dcr_tic_sply', 'dcr_sply',
            'tic_day', 'tic_price_avg','tic_price', 'tic_blk', 'tic_pool', 
            'DiffMean','pow_diff', 'pow_hashrate_THs', 'pow_work_TH'
            ]]
        return df

    def dcr_subsidy_models(self):
        print('...Calculating Decred block subsity models...')
        df = self.dcr_real()
        #Calculate PoS Return on Investment
        df['PoW_income_dcr']    = df['DailyIssuedNtv']*self.blkrew_ratio[0]
        df['PoS_income_dcr']    = df['DailyIssuedNtv']*self.blkrew_ratio[1]
        df['Fund_income_dcr']   = df['DailyIssuedNtv']*self.blkrew_ratio[2]
        df['Total_income_dcr']  = df['PoW_income_dcr']+df['PoS_income_dcr']+df['Fund_income_dcr']
        
        df['PoW_income_usd']    = df['PoW_income_dcr']  *df['PriceUSD']
        df['PoS_income_usd']    = df['PoS_income_dcr']  *df['PriceUSD']
        df['Fund_income_usd']   = df['Fund_income_dcr'] *df['PriceUSD']
        df['Total_income_usd']  = df['Total_income_dcr']*df['PriceUSD']
        return df

    def dcr_ticket_models(self):  #Calculate Ticket Based Valuation Metrics
        print('...Calculating Decred Ticket models...')
        df = self.dcr_subsidy_models()
        # Ticket Cap = cummulative USD put into tickets
        df['tic_dcr_cost'] = df['tic_day'] * df['tic_price_avg']
        df['tic_usd_cost'] = df['tic_dcr_cost'] * df['PriceUSD']
        df['CapTic'] = df['tic_usd_cost'].cumsum()
        df['CapTicPrice'] = df['CapTic'] / df['SplyCur']

        #Calculate Ticket Volume On-chain
        df['dcr_tic_vol'] = df['tic_day'] * df['tic_price_avg']
        df['dcr_tfr_vol'] = df['TxTfrValNtv'] - df['dcr_tic_vol']
        df['tic_tfr_ratio'] = df['dcr_tic_vol'] / df['dcr_tfr_vol']


        #Calculate Aggregate Ticket Risk-Reward
        #Risk = 28 to 142 day volatility of ticket value
        #Reward = PoS_income_dcr
        df['dcr_hodl_rating'] = (df['tic_dcr_cost'] / df['PoS_income_dcr'])
        df['dcr_hodl_rating_tot'] = df['dcr_hodl_rating']*df['SplyCur']*df['PriceUSD']
        df['dcr_hodl_rating_pool'] = df['dcr_hodl_rating']*df['dcr_tic_sply']/1e8*df['PriceUSD']
        df['dcr_hodl_rating_posideal'] = df['dcr_hodl_rating']*df['SplyCur']*self.blkrew_ratio[1]*df['PriceUSD']
        return df

    def dcr_pricing_models(self):
        print('...Calculating Decred pricing models...')
        _real = self.dcr_real()
        df = _real
        #BTC Realised CAP
        df['CapRealised_BTC'] = df['TxTfrValNtv']*df['PriceBTC']
        df['CapRealised_BTC'] = df['CapRealised_BTC'].cumsum()/df['SplyCur']
        # Average Cap and Average Price
        df['CapAvg'] = df['CapMrktCurUSD'].fillna(0.0001) #Fill not quite to zero for Log charts/calcs
        df['CapAvg'] = df['CapAvg'].expanding().mean()
        df['PriceAvg'] = df['CapAvg']/df['SplyCur']
        # Delta Cap and Delta Price
        df['CapDelta'] = df['CapRealUSD'] - df['CapAvg']
        df['PriceDelta'] =df['CapDelta']/df['SplyCur']
        # Top Cap and Top Price
        df['CapTop'] = df['CapAvg']*self.topcapconst
        df['PriceTop'] =df['CapTop']/df['SplyCur']

        #Calc S2F Model - Specific to Decred
        dcr_s2f_model = regression_analysis().ln_regression(df,'S2F','CapMrktCurUSD','date')['model_params']
        df['CapS2Fmodel'] = np.exp(float(dcr_s2f_model['coefficient'])*np.log(df['S2F'])+float(dcr_s2f_model['intercept']))
        df['PriceS2Fmodel'] = df['CapS2Fmodel']/df['SplyCur']
        #Calc S2F Model - Bitcoins Plan B Model
        planb_s2f_model = regression_analysis().regression_constants()['planb']
        df['CapPlanBmodel'] = np.exp(float(planb_s2f_model['coefficient'])*np.log(df['S2F'])+float(planb_s2f_model['intercept']))
        df['PricePlanBmodel'] = df['CapPlanBmodel']/df['SplyCur']

        # Inflow Cap and Inflow Price
        df['CapInflow'] = df['DailyIssuedUSD'].expanding().sum()
        df['PriceInflow'] =df['CapInflow']/df['SplyCur']
        
        # Fee Cap and Fee Price
        df['CapFee'] = df['FeeTotUSD'].expanding().sum()
        df['PriceFee'] =df['CapFee']/df['SplyCur']

        #Calculate Miner Income
        df['MinerIncome'] = df['CapInflow'] + df['CapFee']
        df['FeesPct'] =  df['CapFee']/df['MinerIncome']
        df['MinerCap'] = df['MinerIncome'].expanding().sum()
        return df

    def dcr_oscillators(self):
        print('...Calculating Decred Oscillators...')
        _coin = self.dcr_coin()

        df = _coin        
        #Calc - NVT_28, NVT_90, NVTS, RVT_28, RVT_90, RVTS
        df['NVT_28'] = df['CapMrktCurUSD'].rolling(28).mean()/ df['TxTfrValUSD'].rolling(28).mean()
        df['NVT_90'] = df['CapMrktCurUSD'].rolling(90).mean()/df['TxTfrValUSD'].rolling(90).mean()
        df['NVTS']   = df['CapMrktCurUSD']/ df['TxTfrValUSD'].rolling(28).mean()
        df['RVT_28'] = df['CapRealUSD'].rolling(28).mean()/ df['TxTfrValUSD'].rolling(28).mean()
        df['RVT_90'] = df['CapRealUSD'].rolling(90).mean()/df['TxTfrValUSD'].rolling(90).mean()
        df['RVTS']   = df['CapRealUSD']/ df['TxTfrValUSD'].rolling(28).mean()
        return df

#DCR_coin = dcr_add_metrics().dcr_coin()
#DCR_diff = dcr_add_metrics().dcr_diff()
#DCR_perf = dcr_add_metrics().dcr_perf()
#DCR_natv = dcr_add_metrics().dcr_natv()
#DCR_real = dcr_add_metrics().dcr_real()


#
#x_data = [
#    DCR_real['date'],
#    DCR_real['date'],
#    DCR_real['date'],
#    DCR_real['date']
#]
#y_data = [
#    DCR_real['TxTfrValNtv'],#.rolling(28).mean(),
#    DCR_real['dcr_tic_day'],#.rolling(28).mean(),
#    DCR_real['PriceBTC'],#.rolling(28).mean()
#    DCR_real['BTC_RC']
#]
#name_data = ['DCR Tx Total','DCR Tx Tickets','DCRBTC Price','DCRBTC Realised']
#loop_data = [[0,1],[2,3]]
#title_data = ['DCR Tickets vs Transfers','date','DCR Moving Onchain','DCR BTC Price']
#type_data = ['date','log','log']
#fig = check_standard_charts().basic_chart(x_data,y_data,name_data,loop_data,title_data,type_data).show()



