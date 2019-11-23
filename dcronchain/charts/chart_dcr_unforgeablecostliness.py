#Compare the Unforgeable Costliness of Bitcoin and Decred
from checkonchain.general.standard_charts import *
from checkonchain.dcronchain.dcr_add_metrics import *
from checkonchain.btconchain.btc_add_metrics import *
from checkonchain.dcronchain.dcr_security_model import *


"""
CONCEPT: 
Unforgeable costliness is the cost required to produce each coin.
1. Calculate block subsidy models (Natv and USD terms)
2. Cummulative sum --> assuming marginal reward = marginal cost
    PoW = Cummulative Sum (100% for BTC and 60% for DCR)
    PoS = Cummulative Sum (30% for DCR)
3. For Decred, there is a balance between PoS and PoW as described 
in Stafford (2019)
    Assume an attacker portion of ticket stake owned 
        P_y = (1%, 5%, 30%, 50% and 95%)
    Probability of honest tickets having 3/5 votes
        sig_y = 1 - P_y
    Proportion of Hashrate attacker needs
        x_y = (1 / P_y) - 1
4. Decred cost to attack = P_y(PoS) + x_y(PoW)
"""

BTC_subs = btc_add_metrics().btc_subsidy_models()
BTC_subs['Unforg_Cost'] = BTC_subs['PoW_income_usd'].cumsum()
DCR_subs = dcr_add_metrics().dcr_ticket_models()
DCR_subs['PoW_Cost'] = DCR_subs['PoW_income_usd'].cumsum()
DCR_subs['PoS_Cost'] = DCR_subs['PoS_income_usd'].cumsum()

#Calculate Range of Decred Security Conditions
for y in range(5,105,5): #Assume range of Attacker ticket stake ownership
    y       = y/100       #Probability attacker tickets make block
    i = 0
    _total = 0
    while i < 3:
        _bincoef = (
            math.factorial(5)
            / (math.factorial(5-i) 
            * math.factorial(i))
        )
        _calc = _bincoef * y**(5-i)*((1-y)*1)**i
        _total = _total + _calc
        i += 1
    P_y     = _total
    sig_y   = 1-P_y         #Probability honest tickets  make valid block
    x_y     = (1 / P_y) - 1 #Attacker required hashpower for given stake
    col_name = 'Unforg_Cost_'+str(int(y*100))+'%' #Set column name
    DCR_subs[col_name] = P_y * DCR_subs['PoS_Cost'] + x_y * DCR_subs['PoW_Cost']

#Calculate monetary premium over pure PoW Energy Expendature
BTC_subs['PoW_Premium'] = BTC_subs['CapMrktCurUSD'] / BTC_subs['Unforg_Cost']
DCR_subs['PoW_Premium'] = DCR_subs['CapMrktCurUSD'] / DCR_subs['Unforg_Cost_100%']

BTC_fee = btc_add_metrics().btc_coin()

"""
#############################################################################
                    UNFORGEABLE COSTLINESS
#############################################################################
"""
loop_data = [[0,1,2,3,4,5,6,7,8],[9,10]]
x_data = [
    BTC_subs['age_sply'],DCR_subs['age_sply'],  #Market Caps
    BTC_subs['age_sply'],                       #BTC UC
    DCR_subs['age_sply'],DCR_subs['age_sply'],  #DCR UC
    DCR_subs['age_sply'],DCR_subs['age_sply'],  #DCR UC
    DCR_subs['age_sply'],DCR_subs['age_sply'],  #DCR UC
    BTC_subs['age_sply'],DCR_subs['age_sply'],   #Pow Premium Secondary
    ]
y_data = [
    BTC_subs['CapMrktCurUSD'],DCR_subs['CapMrktCurUSD'],        #Market Caps
    BTC_subs['Unforg_Cost']+BTC_fee['FeeTotUSD'].cumsum(),                                    #BTC UC
    DCR_subs['Unforg_Cost_5%'],DCR_subs['Unforg_Cost_10%'],     #DCR UC
    DCR_subs['Unforg_Cost_15%'],DCR_subs['Unforg_Cost_30%'],    #DCR UC
    DCR_subs['Unforg_Cost_50%'],DCR_subs['Unforg_Cost_95%'],   #DCR UC
    BTC_subs['PoW_Premium'],DCR_subs['PoW_Premium'],            #Pow Premium Secondary
    ]
name_data = [
    'BTC Market Cap','DCR Market Cap',
    'BTC Unforgeable Cost',
    'DCR Unforgeable Cost 5%','DCR Unforgeable Cost 10%',
    'DCR Unforgeable Cost 15%','DCR Unforgeable Cost 30%',
    'DCR Unforgeable Cost 50%','DCR Unforgeable Cost 95%',
    'BTC Pure PoW Premium','DCR Pure PoW Premium',
    ]
color_data = [
    'rgb(255, 255,255)' ,'rgb(46, 214, 161)' ,
    'rgb(255, 102, 0)',
    'rgb(255, 80, 80)','rgb(255, 102, 102)',
    'rgb(255, 153, 102)','rgb(255, 255, 102)',
    'rgb(156,225,43)', 'rgb(1, 255, 116)',
    'rgb(255, 255, 255)', 'rgb(46, 214, 161)',
    ]
dash_data = [
    'solid','solid',
    'solid',
    'solid','solid',
    'solid','solid',
    'solid','solid',
    'dot','dot',
    ]
width_data = [
    2,2,2,1,1,1,1,1,1,1,1
    ]
opacity_data = [
    1,1,1,1,1,1,1,1,1,1,1
    ]
legend_data = [
    True,True,
    True,
    True,True,True,
    True,True,True,
    True,True
    ]#
title_data = [
    'Sound Money, Unforgeable Costliness',
    'Coin Age (Supply/21M)',
    'Cost to Attack Network (USD)',
    'Pure PoW Premium Ratio']
range_data = [[0,1],[4,12],[-1,5]]
autorange_data = [False,False,False]
type_data = ['linear','log','log']#
fig = check_standard_charts().subplot_lines_singleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
#Increase tick spacing
fig.update_xaxes(dtick=0.1)
fig.show()


"""
#############################################################################
                    COMPARE TOP CAP PROJECTS
#############################################################################
"""

LTC = Coinmetrics_api('ltc',"2011-10-07",today).convert_to_pd().set_index('date',drop=False)
BCH = Coinmetrics_api('bch',"2017-08-01",today).convert_to_pd().set_index('date',drop=False)
DASH = Coinmetrics_api('dash',"2014-01-19",today).convert_to_pd().set_index('date',drop=False)
DCR = Coinmetrics_api('dcr',"2016-02-08",today).convert_to_pd().set_index('date',drop=False)
XMR = Coinmetrics_api('xmr',"2014-04-18",today).convert_to_pd().set_index('date',drop=False)
ZEC = Coinmetrics_api('zec',"2016-10-28",today).convert_to_pd().set_index('date',drop=False)
ETH = Coinmetrics_api('eth',"2015-07-30",today).convert_to_pd().set_index('date',drop=False)

LTC['age_sply'] = LTC['SplyCur']/84e6
BCH['age_sply'] = BCH['SplyCur']/21e6
DASH['age_sply'] = DASH['SplyCur']/17.6e6
XMR['age_sply'] = XMR['SplyCur']/22.466e6
ZEC['age_sply'] = ZEC['SplyCur']/21e6
ETH['age_sply'] = ETH['SplyCur']/135e6

LTC['Unforg_Cost'] = LTC['DailyIssuedNtv'] *LTC['PriceUSD'] 
BCH['Unforg_Cost'] = BCH['DailyIssuedNtv'] *BCH['PriceUSD'] 
DASH['Unforg_Cost']= DASH['DailyIssuedNtv']*DASH['PriceUSD']
XMR['Unforg_Cost'] = XMR['DailyIssuedNtv'] *XMR['PriceUSD'] 
ZEC['Unforg_Cost'] = ZEC['DailyIssuedNtv'] *ZEC['PriceUSD'] 
ETH['Unforg_Cost'] = ETH['DailyIssuedNtv'] *ETH['PriceUSD'] 


loop_data = [[0,1,2,3,4,5,6,7,8,9,10,11,12],[]]
x_data = [
    BTC_subs['age_sply'],
    DCR_subs['age_sply'],DCR_subs['age_sply'],DCR_subs['age_sply'],
    DCR_subs['age_sply'],DCR_subs['age_sply'],DCR_subs['age_sply'],
    LTC['age_sply'], 
    BCH['age_sply'], 
    DASH['age_sply'],
    XMR['age_sply'], 
    ZEC['age_sply'], 
    ETH['age_sply'], 
    ]
y_data = [
    BTC_subs['Unforg_Cost'],
    DCR_subs['Unforg_Cost_5%'],DCR_subs['Unforg_Cost_10%'],  
    DCR_subs['Unforg_Cost_30%'],DCR_subs['Unforg_Cost_50%'], 
    DCR_subs['Unforg_Cost_65%'],DCR_subs['Unforg_Cost_95%'],
    LTC['Unforg_Cost'].cumsum(),
    BCH['Unforg_Cost'].cumsum(),
    DASH['Unforg_Cost'].cumsum(),
    XMR['Unforg_Cost'].cumsum(),
    ZEC['Unforg_Cost'].cumsum(),
    ETH['Unforg_Cost'].cumsum()
    ]
name_data = [
    'BTC',
    'DCR 5%','DCR 10%','DCR 30%',
    'DCR 50%','DCR 65%','DCR 95%',
    'LTC',
    'BCH',
    'DASH',
    'XMR',
    'ZEC',
    'ETH',
    ]
color_data = [
    'rgb(255, 102, 0)',
    'rgb(46, 214, 161)' ,'rgb(46, 214, 161)' ,'rgb(46, 214, 161)' ,
    'rgb(46, 214, 161)' ,'rgb(46, 214, 161)' ,'rgb(46, 214, 161)' ,
    'rgb(214, 214, 194)',
    'rgb(0, 153, 51)',  
    'rgb(51, 204, 255)',
    'rgb(255, 153, 0)',  
    'rgb(255, 255, 0)',  
    'rgb(153, 51, 255)' 

    ]
dash_data = [
    'solid',
    'solid','solid','solid',
    'solid','solid','solid',
    'dot',
    'dot',
    'dot',
    'dot',
    'dot',
    'dot',
    ]
width_data = [
    2,
    2,2,2,2,2,2,
    2,2,2,2,2,2]
opacity_data = [
    1,
    1,0.8,0.7,0.6,0.5,0.3,
    1,1,1,1,1,1
    ]
legend_data = [
    True,
    True,True,True,True,True,True,
    True,True,True,True,True,True]#
title_data = [
    'Compare Unforgeable Costliness',
    'Coin Age (Supply / 2050 Supply)',
    'Cost to Attack Network (USD)']
range_data = [[0,1],[4,12],[-1,5]]
autorange_data = [False,False,False]
type_data = ['linear','log','log']
fig = check_standard_charts().subplot_lines_singleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
#Increase tick spacing
fig.update_xaxes(dtick=0.1)
fig.show()


"""
#############################################################################
                    DECRED SECURITY CURVE
#############################################################################
"""

dcr_security_curve = dcr_security_calculate_df().dcr_security_curve()
loop_data = [[0],[2]]
x_data = [dcr_security_curve['y'],[0,1],dcr_security_curve['y']]
y_data = [dcr_security_curve['x_y'],[1,1],dcr_security_curve['days_buy_y']]
name_data = ['Decred Security Curve','Bitcoin Security Curve','Days to Buy Tickets in Full Blocks']
title_data = [
    'DCR Security Curve',
    'Attacker Share of Ticket Pool',
    'Attacker Require Hashpower Multiple',
    'Days to Buy Tickets in Full Blocks'
    ]
color_data = [
    'rgb(255, 102, 0)',
    'rgb(46, 214, 161)' ,
    'rgb(51, 204, 255)',
]
dash_data = ['solid','solid','dash']
width_data = [2,2,2]
opacity_data = [1,1,1]
type_data = ['linear','linear','linear']
range_data = [[0,1],[0,10],[0,10]]
autorange_data = [False,False,False]
legend_data = [True,True,True]
fig = check_standard_charts().subplot_lines_doubleaxis(
    title_data, range_data ,autorange_data ,type_data,
    loop_data,x_data,y_data,name_data,color_data,
    dash_data,width_data,opacity_data,legend_data
    )
#Increase tick spacing
fig.update_xaxes(dtick=0.1)
fig.update_yaxes(dtick=1,secondary_y=False)
fig.update_yaxes(dtick=1,secondary_y=True)
fig.show()
