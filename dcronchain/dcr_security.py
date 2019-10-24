
from mpl_toolkits import mplot3d
%matplotlib inline
import numpy as np
import pandas as pd
import math
import random
import matplotlib.pyplot as plt



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




class cost():

    def __init__(self,asset,atk_blk,y,H_net,blk,pce,Z,p_t):
        # Input Params
        self.asset = asset
        self.atk_blk = atk_blk # number of blks to attack
        self.y = y # portion of stk in atk
        self.H_net = H_net # netwrk total hsh
        self.blk = blk # blk height
        self.pce = pce # pce exch.rate
        self.Z = Z # tic pool size (tic)
        self.p_t = p_t # tic pce (units)



        #Tic Constants
        self.N = 5 # Tic called size
        self.k = 3 # Tic vote size
        self.p = 1 # stake pool participation

        """Set Constants for specific model"""
        if asset ==str('b'):
            self.y = 1e-15 # Hard reset of tic pool to near zero
            self.t_b = 10*60 # blk time (s)
            #pow rentability constants
            self.a = 0 #0.3*self.H_net # total rentable hsh (TH/s)
            self.r_e = 0.2 # rental prce (pce/TH)
            #pow eqip capital constants
            self.h_d = 2.4 # eqip hshpow (TH/s)
            self.w_d = 1 # eqip pow draw (kWh)
            self.p_d = 1700 # eqip capital (pce/unit)

        elif asset ==str('d'):
            self.t_b = 5*60 # blk time (s)
            #pow rentability constants
            self.a = 0 # total rentable hsh (TH/s)
            self.r_e = 0 # rental prce (pce/TH)
            #pow eqip capital constants
            self.h_d = 2.4 # eqip hshpow (TH/s)
            self.w_d = 1 # eqip pow draw (kW)
            self.p_d = 1700 # eqip capital (pce/unit)
            

        # Duration of atk based on blks to be wound back - measure of finality
        self.t_a = self.atk_blk * self.t_b # time of atk (time - s)


        #pow powr constants
        self.adj_d = 0 # adjustment factor for other pow overheads
        self.c = 0.05 # cost per powr ($/KWh)
        self.rho = (self.p_d / self.h_d) # (equip ($/unit)/(TH/s)) = eqip rel cost
        self.nu = self.h_d/self.w_d # (equip (TH/s)/kWh) = eqip powr efficiency
        #print(self.nu,self.rho)

    def R(self): # calc total blk rew
        if self.asset == str('b'):
            R_tot = 50*0.5**(math.floor(self.blk/210000))
            R_pow = R_tot
            R_pos = 0
            R_fnd = 0
        elif self.asset =='d':
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


    def p_y(self): # Probability atk holds reqd tic
        i = 0
        _total = 0
        while i < self.k:
            _bincoef = math.factorial(self.N)/(math.factorial(self.N-i)*math.factorial(i))
            _calc = _bincoef * self.y**(self.N-i)*((1-self.y)*self.p)**i
            _total = _total + _calc
            i += 1
        return _total

    def sig_y(self): # prob honest holds requd tic
        return 1 - self.p_y()

    def x_y(self): # atk factor of hsh reqd (assuming not active)
        return 1/self.p_y() - 1



    """POW"""
    def pow_prof(self): # Daily pow profitability factor
        # beta = Daily USD income (pow_rew * 86400s/day / blk time)
        beta = 86400*self.R()[1] / self.t_b # 86400 * R_pow / blk time (s*units/blk time in s = daily units)
        # pow prof = beta / (cost in units $/(TH/s) maed up of device cost + power cost)
        a_w = ((beta * self.pce)/(self.H_net) - (0.024*self.c/self.nu))/self.rho
        return a_w
        
    def H_a(self): # atk proportion of total hshrte
        # relating H_a to miner profitability --> 0 in the long term
        H_a = self.sig_y() * (86400*self.R()[1]*self.pce) / (self.t_b*(self.pow_prof()*self.rho + 0.024*self.c/self.nu))
        return H_a

    def pow_term(self): # Calculate aggregare pow cost
        # Rental
        R = self.a * self.r_e * self.t_a # TH/s * pce/TH * time
        # Equip Capital
        D = (self.H_a() - self.a) * self.rho # (atk hsh - rent hsh) * (eqip rel cost)
        # Power
        P = (self.H_a()- self.a)/self.nu * self.c * self.t_a
        W = R + D + P
        return W, R/W, D/W, P/W # Return Total Work Cost, %Rental, %Capital, %Power

    def pow_earn(self):
        pass
    
    
    """POS"""
    def pos_prof(self): # annual stk yield %     
        return ((self.p_t+(self.R()[2]/self.N))/self.p_t)**(365.25/28)-1
    
    def pos_term(self):
        # Stake share * tic pool * tic diff (units) * pce ($/unit)
        S_a = (self.y * self.Z * self.R()[2] * self.pce) / (self.N*((self.pos_prof()+1)**(28/365.25)-1))
        return S_a
    

    def pca(self): # Total atk cst
        return self.pow_term()[0] + self.pos_term()

    def check(self):
        return self.R_tot()[0]



df = pd.DataFrame()
asset = 'd'
atk_blk = 1
df['y'] = np.linspace(0.1,1.0,10)
df['H_net'] = np.linspace(200e3,200e3,10)#*random.randint(85,130)/100
df['blk'] = np.linspace(6144*100,6144*100,10).round(0)
df['pce'] = np.linspace(15,15,10)*random.randint(85,130)/100
df['tic_pool'] = 40960
df['tic_pce'] = np.linspace(100,100,10)



df['sig_y'] = df.apply(
    lambda row : cost(
        asset,atk_blk,row['y'],row['H_net'],row['blk'],row['pce'],row['tic_pool'],row['tic_pce']
        ).sig_y(),axis=1) 

df['p_y'] = df.apply(
    lambda row : cost(
        asset,atk_blk,row['y'],row['H_net'],row['blk'],row['pce'],row['tic_pool'],row['tic_pce']
        ).p_y(),axis=1) 

df['x_y'] = df.apply(
    lambda row : cost(
        asset,atk_blk,row['y'],row['H_net'],row['blk'],row['pce'],row['tic_pool'],row['tic_pce']
        ).x_y(),axis=1) 


df['H_a'] = df.apply(
    lambda row : cost(
        asset,atk_blk,row['y'],row['H_net'],row['blk'],row['pce'],row['tic_pool'],row['tic_pce']
        ).H_a(),axis=1) 

df['pow_%rent'] = df.apply(
    lambda row : cost(
        asset,atk_blk,row['y'],row['H_net'],row['blk'],row['pce'],row['tic_pool'],row['tic_pce']
        ).pow_term()[1],axis=1)

df['pow_%cap'] = df.apply(
    lambda row : cost(
        asset,atk_blk,row['y'],row['H_net'],row['blk'],row['pce'],row['tic_pool'],row['tic_pce']
        ).pow_term()[2],axis=1)

df['pow_%powr'] = df.apply(
    lambda row : cost(
        asset,atk_blk,row['y'],row['H_net'],row['blk'],row['pce'],row['tic_pool'],row['tic_pce']
        ).pow_term()[3],axis=1)


df['pow_term'] = df.apply(
    lambda row : cost(
        asset,atk_blk,row['y'],row['H_net'],row['blk'],row['pce'],row['tic_pool'],row['tic_pce']
        ).pow_term()[0],axis=1) / 1e6

df['pos_term'] = df.apply(
    lambda row : cost(
        asset,atk_blk,row['y'],row['H_net'],row['blk'],row['pce'],row['tic_pool'],row['tic_pce']
        ).pos_term(),axis=1) / 1e6

df['pca'] = df.apply(
    lambda row : cost(
        asset,atk_blk,row['y'],row['H_net'],row['blk'],row['pce'],row['tic_pool'],row['tic_pce']
        ).pca(),axis=1) / 1e6

df['pow_prof'] = df.apply(
    lambda row : cost(
        asset,atk_blk,row['y'],row['H_net'],row['blk'],row['pce'],row['tic_pool'],row['tic_pce']
        ).pow_prof(),axis=1) 

df


#plt.plot('y','pow_prof',data=df)
#plt.show()

plt.plot('y','pow_term',data=df)
plt.plot('y','pos_term',data=df)
plt.plot('y','pca',data=df)
plt.show()


