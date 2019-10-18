#Produce Decred Supply Schedule
#Data Science
import pandas as pd
import numpy as np
import math

from checkonchain.dcronchain.dcr_dcrdata_api import *
from checkonchain.dcronchain.dcr_add_metrics import *

import os
os.getcwd()
os.chdir('D:\code_development\checkonchain\checkonchain')

"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
DECRED SUPPLY FUNCTION
dcr_supply_schedule.dcr_supply_function(end_blockheight)
Returns blk, TotSply, PoWSply, PoSSply, FundSply, Inflation, S2F
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""

class dcr_supply_schedule:

    #Set constants for DECRED
    def __init__(self,blk_max):
        self.initial_sply = 1.68e6
        self.initial_W = 0
        self.initial_S = 0.5*self.initial_sply
        self.initial_F = 0.5*self.initial_sply
        self.initial_br = 31.19582664
        self.br_W = 0.6
        self.br_S = 0.3
        self.br_F = 0.1
        self.halving = 6144
        self.blk_min = 1
        self.blk_max = blk_max
        self.blk_time = 5 #min
        self.atoms = 1e8

        #Premine constants
        self.founder_unspent    = 0.28970827970828 #portion of founders reward unspent refer block 1
        self.founder_spent      = 1-self.founder_unspent
        self.community_unspent  = 0.173283983849524 #portion of community reward unspent refer block 1
        self.community_spent    = 1-self.community_unspent
        self.treasury_founder_outflow = 0.25 #assume 25% draw annual C0 draw treasury
        self.treasury_founder_expenses = 0.5 #assume 50% of founders fund is expenses

    def dcr_schedule(self,blk):
        response = int(math.floor(blk/self.halving))
        return response

    def dcr_blk_rew(self,blk):
        if blk == 0:
            response = self.initial_sply
        else:
            response = self.initial_br*(100/101)**self.dcr_schedule(blk)
        return response

    def dcr_supply_function(self):
        print('...Calculating Decred Supply Curve up to block height ',self.blk_max,'...')
        response=np.zeros((self.blk_max,8))
        response[0,0]=int(0) #block height
        response[0,1]=self.dcr_blk_rew(0) #Current Block Reward
        response[0,2]=self.initial_sply #Total Supply
        response[0,3]=self.initial_W #Total PoW Supply
        response[0,4]=self.initial_S #Total PoS Supply
        response[0,5]=self.initial_F #Total Treasury Supply
        response[0,6]=self.dcr_blk_rew(0)*(365*24*60/self.blk_time)/self.initial_sply #Inflation Rate
        response[0,7]=1/response[0,6] #Stock-to-Flow Ratio 
        for i in range (1, self.blk_max):
            response[i,0] = int(i)
            response[i,1] = self.dcr_blk_rew(i)
            response[i,2] = response[i-1,2]+self.dcr_blk_rew(i)
            response[i,3] = response[i-1,3]+self.dcr_blk_rew(i)*self.br_W
            response[i,4] = response[i-1,4]+self.dcr_blk_rew(i)*self.br_S
            response[i,5] = response[i-1,5]+self.dcr_blk_rew(i)*self.br_F
            response[i,6] = self.dcr_blk_rew(i)*(365*24*60/self.blk_time)/response[i,2]
            response[i,7] = 1/response[i,6]
    
        columns=['blk','blk_reward','Sply_ideal','PoWSply_ideal','PoSSply_ideal','FundSply_ideal','inflation_ideal','S2F_ideal']
        df = pd.DataFrame(data=response,columns=columns)
        return df


    def dcr_premine(self,dcr_real):
        response = dcr_real
        #Calculate relative DCR holdings
        response['pmine_c0']                        = self.initial_F #initial founder reward
        response['pmine_c0_spent']                  = self.initial_F * self.founder_spent #spent founder reward
        response['pmine_c0_unspent']                = self.initial_F * self.founder_unspent #spent founder reward
        response['pmine_com']                       = self.initial_S #initial founder reward
        response['pmine_com_spent']                 = self.initial_S * self.community_spent #spent founder reward
        response['pmine_com_unspent']               = self.initial_S * self.community_unspent #spent founder reward

        #Calculkate staking rewards by block - cut where no DCR was in the pool
        response = response[response['ticket_pool_value']>0]
        response['spent_pool_ratio'] = (response['pmine_com_spent']+response['pmine_c0_spent'])/response['ticket_pool_value']

        _c0_com_spent_ratio = (self.initial_F * self.founder_spent)/(self.initial_S * self.community_spent+self.initial_F * self.founder_spent)
        #Calculate absolute worst case where no PoW rewards are staked and C0 and community spent all stake
        response['c0_spent_pos']    = response['pmine_c0_spent'] + _c0_com_spent_ratio*(response['PoSSply_ideal'] - self.initial_S)
        response['com_spent_pos']   = response['pmine_com_spent']  + (1-_c0_com_spent_ratio)*(response['PoSSply_ideal'] - self.initial_S)
        return response