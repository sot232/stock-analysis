import argparse
import datetime

import pandas as pd
import numpy as np

import yahoo_fin.stock_info as si
import yfinance as yf

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
                full_company_name = get_company_name_from_ticker(symbol)
                expected_price = get_expected_price(symbol)
                live_price = get_live_price(symbol)
                is_undervalued = get_is_undervalued(expected_price, live_price)
                degree_of_undervalued = get_degree_of_undervalued(expected_price, live_price)
                prices.append([
                    symbol,
                    full_company_name,
                    expected_price,
                    live_price,
                    is_undervalued,
                    degree_of_undervalued
                ])
                print(f'Got a price for {symbol}')
            except:
                print(f"Couldn't get a price for {symbol}.")

        if args.p:
            if len(symbols) > 10:
                ticker_symbols = symbols[:10]

            export_df = pd.DataFrame(prices)
            export_df.columns = [
                'Symbol',
                'Full Name',
                'Expected Price',
                'Live Price',
                'Undervalued?',
                'Degree of "Undervalued?"'
            ]
            export_df.to_csv(
                f'prices-{ticker_symbols}-{datetime.datetime.now().time()}.csv',
                index=False
            )
        print('It is all done!')
    else:
        print('Please provide symbols. Use -s argument.')


def get_company_name_from_ticker(ticker) -> str:
    '''
    Parameters:
        ticker (Str): Company symbol
    
    Returns:
        company_name (Str): Full company name
    '''
    ticker_info = yf.Ticker(ticker)
    company_name = ticker_info.info['longName']
    
    return company_name


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


def get_degree_of_undervalued(expected_price, live_price) -> float:
    '''
    Parameters:
        expected_price (float):
        live_price (float):

    Returns:
        (float):
    '''
    return np.abs(expected_price - live_price)


def get_is_undervalued(expected_price, live_price) -> str:
    '''
    Parameters:
        expected_price (float):
        live_price (float):

    Returns:
        value (Str): Whether the live price is undervalued, overvalued, or undefined
    '''
    if expected_price and live_price:
        is_undervalued = expected_price > live_price
        if is_undervalued:
            value = 'Undervalued'
        else:
            value = 'Overvalued'
    else:
        value = np.NaN
    
    return value
    


def get_live_price(symbol) -> float:
    return si.get_live_price(symbol)


if __name__ == "__main__":
    main()