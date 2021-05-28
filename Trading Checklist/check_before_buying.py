import argparse
import datetime

import pandas as pd

import yahoo_fin.stock_info as si

def main():
    # define parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', default='', help="Stock tickers. i.e. 'GOOGL,GOOG'")
    parser.add_argument('-p', default=False, help='Print the output to CSV')
    args = parser.parse_args()

    if args.s:
        print(f'Received symbols: {args.s}')
        symbols = args.s.split(',')

        prices = list()
        for symbol in symbols:
            try:
                expected_price = get_expected_price(symbol)
                live_price = get_live_price(symbol)
                is_undervalued = expected_price > live_price
                prices.append([expected_price, live_price, is_undervalued])
            except:
                print("Couldn't get prices.")

        if args.p:
            pd.DataFrame(prices).to_csv(
                f'prices-{symbols}-{datetime.datetime.now().time()}.csv'
                )
    else:
        print('Please provide symbols. Use -s argument.')


def get_expected_price(symbol) -> float:
    '''
    Parameters:
        symbols (Str): Individual stock ticker
    
    Returns:
        expected EPS * P/E
    '''
    # contain eps and per
    quote_table = si.get_quote_table(symbol, dict_result=True)
    eps = quote_table['EPS (TTM)']
    per = quote_table['PE Ratio (TTM)']

    return eps * per


def get_live_price(symbol) -> float:
    return si.get_live_price(symbol)


if __name__ == "__main__":
    main()