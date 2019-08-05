import pandas as pd
import datetime as dt


def calculate_vwap(price_data):
    total_volume = price_data['NumShares'].sum()
    price_data['VWAP'] = (price_data['Price'] * price_data['NumShares']) / total_volume
    return price_data


def get_n_business_dates(ndays, end_date=dt.date.today()):
    curr_start = end_date - dt.timedelta(ndays)
    curr_range = pd.bdate_range(curr_start, end_date)
    while len(curr_range) < ndays:
        dshift = ndays - len(curr_range)
        curr_start -= dt.timedelta(dshift)
        curr_range = pd.bdate_range(curr_start, end_date)
    return curr_range


def subtract_from_date(date, days=0, months=0, years=0):
    return dt.date(date.year-years, date.month-months, date.day-days)