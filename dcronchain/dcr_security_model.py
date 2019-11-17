#Parametric model for the cost to attack a PoW and Hybrid PoW/PoS blockchain
import numpy as np
import pandas as pd
import math
import random

class dcr_security_cost():

    def __init__(self,asset,atk_blk,y,H_net,blk,price,Z,p_t):
        # Input Params
        self.asset = asset # 'btc' or 'dcr' supported
        self.atk_blk = atk_blk # depth of blocks to attack | double spend
        self.y = y # portion of stake owned by attacker
        self.H_net = H_net # network total hashrate (TH/s)
        self.blk = blk # blk height
        self.price = price # DCR/Fiat Exchange Rate
        self.Z = Z # Ticket pool size (~40960)
        self.p_t = p_t # Ticket price (DCR)

        #Ticket Constants for Decred
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


    def p_y(self): 
        #Probability attacker holds required tickets to make valid block
        i = 0
        _total = 0
        while i < self.k:
            _bincoef = (
                math.factorial(self.N)
                / (math.factorial(self.N-i) 
                * math.factorial(i))
            )
            _calc = _bincoef * self.y**(self.N-i)*((1-self.y)*self.p)**i
            _total = _total + _calc
            i += 1
        return _total

    def sig_y(self): 
        #Probability honest party required tickets to make valid block (1-p_y)
        return 1 - self.p_y()

    def x_y(self): # attacker factor of hashpower required (assuming attacker hash is not already active)
        return 1/self.p_y() - 1

    """Proof-of-Work Term"""
    def pow_prof(self): # Daily pow profitability factor
        # beta = Daily USD income
        # 86400 * R_pow / blk time (s*units/blk time in s = daily units)
        beta = 86400*self.R()[1] / self.t_b 
        #PoW profitability a_w
        # a_w = beta / (network hashrate H_net) - cost of ASIC and Power 
        # --> Aggregate Income - Costs
        a_w = ((beta * self.price)/(self.H_net) - (0.024*self.c/self.nu))/self.rho
        return a_w
        #Note - pow_prof calcs based on H_net --> H_a calc. Thus a_w links H_net and H_a

    def H_a(self): # attackers proportion of total hashrate
        # relating H_a to miner profitability --> 0 in the long term
        # Attackers hashrate = Prob Honest Tickest * Daily PoW USD Reward / (blk_time(ASIC + power costs))
        H_a = (self.sig_y() 
        * (86400*self.R()[1]*self.price) 
        / (self.t_b*(self.pow_prof()*self.rho + 0.024*self.c/self.nu))
        )
        return H_a

    def pow_term_rent(self):
        # Rental Costs
        R = self.a * self.r_e * self.t_a # TH/s * price/TH * time
        return R

    def pow_term_asic(self):
        # ASIC Capital
        # (atk hsh - rent hsh) * (ASIC rel cost) * Overhead adjustment factor
        D = (self.H_a() - self.a) * self.rho * self.adj_d 
        return D

    def pow_term_power(self):        
        # Power Costs
        P = (self.H_a()- self.a)/self.nu * self.c * self.t_a
        return P

    def pow_term(self): 
        #Calculate aggregate PoW cost
        W = self.pow_term_rent() + self.pow_term_asic() + self.pow_term_power()
        return W #Return Total Proof-of-Work Cost

   
    """Proof-of-Stake Term"""
    def pos_prof(self): # annual stk yield %
        # 
        return ((self.p_t+(self.R()[2]/self.N))/self.p_t)**(365.25/28)-1
    
    def pos_term(self):
        # Stake share * tic pool * tic diff (units) * price ($/unit)
        S_a = (self.y * self.Z * self.R()[2] * self.price) / (self.N*((self.pos_prof()+1)**(28/365.25)-1))
        return S_a
    
    """Total Cost to Attack"""
    def pca(self): # Total atk cst
        return self.pow_term() + self.pos_term()


class dcr_security_calculate_df():
    """Calculates a dataframe from dcr_security model
    Inputs: df = DataFrame structured with the following columns
        df['blk']       = Block Height (time variable)
        df['H_net']     = Hashrate measured in TH/s
        df['price']     = Price of coin in USD
        df['tic_pool']  = Tickets in pool (target is 40960)
        df['tic_price'] = Ticket Price in DCR
        df['y']         = Portion of the ticket pool owned by an attacker (0 to 1)
    Outputs: df = Dataframe with appended columns
        df['sig_y']     = Probability honest party required tickets to make valid block (1-p_y)
        df['p_y']       = Probability attacker holds required tickets to make valid block
        df['x_y']       = Attacker factor of hashpower required (assuming attacker hash is not already active)
        df['H_a']       = Attackers proportion of total hashrate
        df['pow_rent'] = PoW Cost to Attack (Rental Component, %age)
        df['pow_asic'] = PoW Cost to Attack (ASIC Capital Component, %age)
        df['pow_power'] = PoW Cost to Attack (Power Component, %age)
        df['pow_term']  = PoW Cost to Attack Total (USD)
        df['pos_term']  = PoS Cost to Attack Total (USD)
        df['pow_term']  = PoW Cost to Attack Total (USD)
        df['pca']       = Total Cost to Attack (USD)
        df['pow_ratio'] = Ratio of PoW contribution to PCA pow/term / pca
        df['pow_prof']  = Miner profitability
        df['pos_prof']  = Staker profitability
    """
    def __init__(self):
        pass

    def calculate_df(self,asset,atk_blk,df):
        df['sig_y'] = df.apply(
            lambda row : dcr_security_cost(
                asset,atk_blk,row['y'],row['H_net'],row['blk'],row['price'],row['tic_pool'],row['tic_price']
                ).sig_y(),axis=1) 
        df['p_y'] = df.apply(
            lambda row : dcr_security_cost(
                asset,atk_blk,row['y'],row['H_net'],row['blk'],row['price'],row['tic_pool'],row['tic_price']
                ).p_y(),axis=1) 
        df['x_y'] = df.apply(
            lambda row : dcr_security_cost(
                asset,atk_blk,row['y'],row['H_net'],row['blk'],row['price'],row['tic_pool'],row['tic_price']
                ).x_y(),axis=1) 
        df['H_a'] = df.apply(
            lambda row : dcr_security_cost(
                asset,atk_blk,row['y'],row['H_net'],row['blk'],row['price'],row['tic_pool'],row['tic_price']
                ).H_a(),axis=1) 
        df['pow_rent'] = df.apply(
            lambda row : dcr_security_cost(
                asset,atk_blk,row['y'],row['H_net'],row['blk'],row['price'],row['tic_pool'],row['tic_price']
                ).pow_term_rent(),axis=1)
        df['pow_asic'] = df.apply(
            lambda row : dcr_security_cost(
                asset,atk_blk,row['y'],row['H_net'],row['blk'],row['price'],row['tic_pool'],row['tic_price']
                ).pow_term_asic(),axis=1)
        df['pow_power'] = df.apply(
            lambda row : dcr_security_cost(
                asset,atk_blk,row['y'],row['H_net'],row['blk'],row['price'],row['tic_pool'],row['tic_price']
                ).pow_term_power(),axis=1)
        df['pow_term'] = df.apply(
            lambda row : dcr_security_cost(
                asset,atk_blk,row['y'],row['H_net'],row['blk'],row['price'],row['tic_pool'],row['tic_price']
                ).pow_term(),axis=1) / 1e6
        df['pos_term'] = df.apply(
            lambda row : dcr_security_cost(
                asset,atk_blk,row['y'],row['H_net'],row['blk'],row['price'],row['tic_pool'],row['tic_price']
                ).pos_term(),axis=1) / 1e6
        df['pca'] = df.apply(
            lambda row : dcr_security_cost(
                asset,atk_blk,row['y'],row['H_net'],row['blk'],row['price'],row['tic_pool'],row['tic_price']
                ).pca(),axis=1) / 1e6
        df['pow_ratio'] = df['pow_term'] / df['pca']
        df['pow_prof'] = df.apply(
            lambda row : dcr_security_cost(
                asset,atk_blk,row['y'],row['H_net'],row['blk'],row['price'],row['tic_pool'],row['tic_price']
                ).pow_prof(),axis=1)
        df['pos_prof'] = df.apply(
            lambda row : dcr_security_cost(
                asset,atk_blk,row['y'],row['H_net'],row['blk'],row['price'],row['tic_pool'],row['tic_price']
                ).pos_prof(),axis=1)
        return df
