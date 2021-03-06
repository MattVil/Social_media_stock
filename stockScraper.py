import datetime as dt
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from matplotlib import style

from utils import STOCK


def get_daily_change(company, date):
    '''date : (month, day, year)'''
    day = dt.datetime(date[2], date[0], date[1]) - dt.timedelta(1)

    df = web.DataReader(STOCK[company.replace('_', ' ')], 'yahoo', day)
    df.reset_index(inplace=True,drop=False)
    df = df[df['Date'] == '{}-{}-{}'.format(date[2], date[0], date[1])]
    if(df.empty):
        print("No Stock value for this date.")
        return None
    return float(df.iloc[[0]]['Open'] - df.iloc[[0]]['Close'])

def main():

    for i in range(1, 32):
        print("3/{}/2019 ".format(i)+"-"*70)
        google = get_daily_change("Google", (3, i, 2019))
        tesla = get_daily_change("Tesla", (3, i, 2019))
        apple = get_daily_change("Apple", (3, i, 2019))
        amazon = get_daily_change("Amazon", (3, i, 2019))
        facebook = get_daily_change("Facebook", (3, i, 2019))
        if(google):
            print("Google: {:.4f}\tTesla: {:.4f}\tApple: {:.4f}\tAmazon: {:.4f}\tFacebook: {:.4f}".format(google,
                                                                                  tesla,
                                                                                  apple,
                                                                                  amazon,
                                                                                  facebook))


if __name__ == '__main__':
    main()
