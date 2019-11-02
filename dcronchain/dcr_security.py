
from mpl_toolkits import mplot3d
%matplotlib inline
import numpy as np
import pandas as pd
import math
import random
import matplotlib.pyplot as plt

from checkonchain.dcronchain.dcr_add_metrics import *
from checkonchain.btconchain.btc_add_metrics import *

#Scenarios
# 1 - Actual Performance
#       Input Knowns = H_net, tic, pce
#       Assume = y
#       Output = PCA vs time (2D, y lines), pow prof vs time (pce secondary), Ha vs time
#
# 2 - Parametric
#       Input Knowns = 
#       Assume = y
#       Output = y vs sig(y) vs 

class dcr_security_cost():

    def __init__(self,asset,atk_blk,y,H_net,blk,pce,Z,p_t):
        # Input Params
        self.asset = asset # 'btc' or 'dcr' supported
        self.atk_blk = atk_blk # number of blocks to attack / double spend
        self.y = y # portion of stake owned by attacker
        self.H_net = H_net # network total hashrate (TH/s)
        self.blk = blk # blk height
        self.pce = pce # DCR/Fiat Exchange Rate
        self.Z = Z # Ticket pool size (~40960)
        self.p_t = p_t # tic price (DCR)

        #Tic Constants
        self.N = 5 # Tickets called per block
        self.k = 3 # Tickets required to vote yes
        self.p = 1 # stake pool online rate (0-1) (relate to missed)

        """Set Constants for specific model"""
        if asset ==str('btc'):
            self.y = 1e-15 # Hard reset of tic pool to near zero
            self.t_b = 10*60 # blk time (s)
            #PoW rentability constants
            self.a = 0 # total rentable hsh (TH/s)
            self.r_e = 0.2 # rental price (fiat / TH/s)
            #PoW ASIC capital constants
            self.h_d = 2.4 # ASIC hashrate (TH/s)
            self.w_d = 1 # ASIC power draw (kW)
            self.p_d = 1700 # ASIC capital (fiat/ASIC Device)

        elif asset ==str('dcr'):
            self.t_b = 5*60 # blk time (s)
            #PoW rentability constants
            self.a = 0 # total rentable hashrate (TH/s)
            self.r_e = 0 # rental price (fiat / TH/s)
            #PoW ASIC capital constants
            self.h_d = 2.4 # ASIC hashpower (TH/s)
            self.w_d = 1 # ASIC power draw (kW)
            self.p_d = 1700 # ASIC capital (fiat/ASIC Device)
            
        # Duration of attack based on blocks to be wound back - compare of finality
        self.t_a = self.atk_blk * self.t_b # time of attack (time in s)

        #PoW power constants
        self.adj_d = 1 # adjustment factor for other PoW overheads (multiple on Device cost)
        self.c = 0.05 # cost per power ($/KWh)
        self.rho = (self.p_d / self.h_d) # (ASIC ($/unit)/(TH/s)) = ASIC relative cost
        self.nu = self.h_d/self.w_d # (ASIC (TH/s)/kWh) = ASIC power efficiency

    def R(self): # calc total block reward for btc and dcr
        if self.asset == str('btc'):
            R_tot = 50*0.5**(math.floor(self.blk/210000))
            R_pow = R_tot
            R_pos = 0
            R_fnd = 0
        elif self.asset =='dcr':
            R_tot = 31.19582664*(100/101)**(math.floor(self.blk/6144))
            R_pow = 0.6 * R_tot
            R_pos = 0.3 * R_tot
            R_fnd = 0.1 * R_tot
        else:
            R_tot = 0
            R_pow = 0
            R_pos = 0
            R_fnd = 0
        return R_tot,R_pow,R_pos,R_fnd


    def p_y(self): # Probability attacker holds required tickets to make valid block
        i = 0
        _total = 0
        while i < self.k:
            _bincoef = math.factorial(self.N)/(math.factorial(self.N-i)*math.factorial(i))
            _calc = _bincoef * self.y**(self.N-i)*((1-self.y)*self.p)**i
            _total = _total + _calc
            i += 1
        return _total

    def sig_y(self): # probability honest party required tickets to make valid block (1-p_y)
        return 1 - self.p_y()

    def x_y(self): # attacker factor of hashpower required (assuming attacker hash is not already active)
        return 1/self.p_y() - 1

    """Proof-of-Work Term"""
    def pow_prof(self): # Daily pow profitability factor
        # beta = Daily USD income (PoW Reward * 86400s/day / blk time)
        beta = 86400*self.R()[1] / self.t_b # 86400 * R_pow / blk time (s*units/blk time in s = daily units)
        # PoW profitability = beta / (network hashrate H_net) - cost of ASIC and Power --> Aggregate Income - Costs
        a_w = ((beta * self.pce)/(self.H_net) - (0.024*self.c/self.nu))/self.rho
        return a_w
        #Note - pow_prof calcs based on H_net --> H_a calc. Thus a_w links H_net and H_a

    def H_a(self): # attackers proportion of total hashrate
        # relating H_a to miner profitability --> 0 in the long term
        # Attackers hashrate = Prob Honest Tickest * Daily PoW USD Reward / (blk_time(ASIC + power costs))
        H_a = self.sig_y() * (86400*self.R()[1]*self.pce) / (self.t_b*(self.pow_prof()*self.rho + 0.024*self.c/self.nu))
        return H_a

    def pow_term(self): # Calculate aggregare PoW cost
        # Rental Costs
        R = self.a * self.r_e * self.t_a # TH/s * pce/TH * time
        # ASIC Capital
        D = (self.H_a() - self.a) * self.rho * self.adj_d # (atk hsh - rent hsh) * (ASIC rel cost) * Overhead adjustment factor
        # Power Costs
        P = (self.H_a()- self.a)/self.nu * self.c * self.t_a
        W = R + D + P
        return W, R/W, D/W, P/W # Return Total Work Cost, %Rental, %Capital, %Power

    def pow_earn(self):
        pass
    
    
    """Proof-of-Stake Term"""
    def pos_prof(self): # annual stk yield %
        # 
        return ((self.p_t+(self.R()[2]/self.N))/self.p_t)**(365.25/28)-1
    
    def pos_term(self):
        # Stake share * tic pool * tic diff (units) * pce ($/unit)
        S_a = (self.y * self.Z * self.R()[2] * self.pce) / (self.N*((self.pos_prof()+1)**(28/365.25)-1))
        return S_a
    
    def pca(self): # Total atk cst
        return self.pow_term()[0] + self.pos_term()

    def populate_df(self,df):
        df['sig_y'] = df.apply(
            lambda row : self.dcr_security_cost(
                asset,atk_blk,row['y'],row['H_net'],row['blk'],row['pce'],row['tic_pool'],row['tic_pce']
                ).sig_y(),axis=1) 
        df['p_y'] = df.apply(
            lambda row : self.dcr_security_cost(
                asset,atk_blk,row['y'],row['H_net'],row['blk'],row['pce'],row['tic_pool'],row['tic_pce']
                ).p_y(),axis=1) 
        df['x_y'] = df.apply(
            lambda row : self.dcr_security_cost(
                asset,atk_blk,row['y'],row['H_net'],row['blk'],row['pce'],row['tic_pool'],row['tic_pce']
                ).x_y(),axis=1) 
        df['H_a'] = df.apply(
            lambda row : self.dcr_security_cost(
                asset,atk_blk,row['y'],row['H_net'],row['blk'],row['pce'],row['tic_pool'],row['tic_pce']
                ).H_a(),axis=1) 
        df['pow_%rent'] = df.apply(
            lambda row : self.dcr_security_cost(
                asset,atk_blk,row['y'],row['H_net'],row['blk'],row['pce'],row['tic_pool'],row['tic_pce']
                ).pow_term()[1],axis=1)
        df['pow_%cap'] = df.apply(
            lambda row : self.dcr_security_cost(
                asset,atk_blk,row['y'],row['H_net'],row['blk'],row['pce'],row['tic_pool'],row['tic_pce']
                ).pow_term()[2],axis=1)
        df['pow_%powr'] = df.apply(
            lambda row : self.dcr_security_cost(
                asset,atk_blk,row['y'],row['H_net'],row['blk'],row['pce'],row['tic_pool'],row['tic_pce']
                ).pow_term()[3],axis=1)
        df['pow_term'] = df.apply(
            lambda row : self.dcr_security_cost(
                asset,atk_blk,row['y'],row['H_net'],row['blk'],row['pce'],row['tic_pool'],row['tic_pce']
                ).pow_term()[0],axis=1) / 1e6
        df['pos_term'] = df.apply(
            lambda row : self.dcr_security_cost(
                asset,atk_blk,row['y'],row['H_net'],row['blk'],row['pce'],row['tic_pool'],row['tic_pce']
                ).pos_term(),axis=1) / 1e6
        df['pow_pos_ratio'] = df['pow_term'] / df['pos_term']

        df['pca'] = df.apply(
            lambda row : self.dcr_security_cost(
                asset,atk_blk,row['y'],row['H_net'],row['blk'],row['pce'],row['tic_pool'],row['tic_pce']
                ).pca(),axis=1) / 1e6
        df['pow_prof'] = df.apply(
            lambda row : self.dcr_security_cost(
                asset,atk_blk,row['y'],row['H_net'],row['blk'],row['pce'],row['tic_pool'],row['tic_pce']
                ).pow_prof(),axis=1)
        df['pos_prof'] = df.apply(
            lambda row : self.dcr_security_cost(
                asset,atk_blk,row['y'],row['H_net'],row['blk'],row['pce'],row['tic_pool'],row['tic_pce']
                ).pos_prof(),axis=1) 
        return df


DCR_real = dcr_add_metrics().dcr_real()
BTC_real = btc_add_metrics().btc_real()

asset = 'dcr'
atk_blk = 1

df = pd.DataFrame()
df['H_net'] = DCR_real['pow_hashrate_THs']
df['blk'] = DCR_real['blk']
df['pce'] = DCR_real['PriceUSD']
df['tic_pool'] = DCR_real['ticket_pool_size']
df['tic_pce'] = DCR_real['ticket_price']
df['y'] = 0.1


#plt.plot('y','pow_prof',data=df)
#plt.show()

plt.plot('y','pow_term',data=df)
plt.plot('y','pos_term',data=df)
plt.plot('y','pca',data=df)
plt.show()


