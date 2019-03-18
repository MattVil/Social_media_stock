import datetime as dt
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from matplotlib import style


STOCK = {'Tesla'            : 'TSLA',
         'Google'           : 'GOOGL',
         'Apple'            : 'AAPL',
         'Facebook'         : 'FB',
         'Amazon'           : 'AMZN',
         'General motors'   : 'GM',
         'CVS Health'       : 'CVS',
         'Chevron'          : 'CVX',
         'Verizon'          : 'VZ',
         'JP Morgan'        : 'JPM'}

def get_daily_change(company, date):
    '''date : (month, day, year)'''
    day = dt.datetime(date[2], date[0], date[1]) - dt.timedelta(1)

    df = web.DataReader(STOCK[company], 'yahoo', day)
    df.reset_index(inplace=True,drop=False)
    df = df[df['Date'] == '{}-{}-{}'.format(date[2], date[0], date[1])]
    if(df.empty):
        print("No Stock value for this date.")
        return None
    return float(df.iloc[[0]]['Open'] - df.iloc[[0]]['Close'])

def main():

    for i in range(1, 29):
        print("-"*80)
        print(get_daily_change("Google", (2, i, 2019)))


if __name__ == '__main__':
    main()
