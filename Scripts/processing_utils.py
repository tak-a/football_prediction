# Created by taka the 2/3/21 at 7:54 PM

import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import config as cfg
from datetime import datetime
import os


def extract_from_url(url):
    """
    from an url, return the html code
    :param url: string link of the webpage we want the html text of
    :return: bs4, the html text of the webpage
    """
    url_text = requests.get(url).text
    return BeautifulSoup(url_text, 'html.parser')


def compute_y_val(home_goal, away_goal):
    if home_goal > away_goal:
        return [1, 0, 0]
    elif home_goal < away_goal:
        return [0, 0, 1]
    else:
        return [0, 1, 0]


def fetch_players_rating(df, match_ids, rating_col):
    l = []
    for player_id in match_ids:
        # print(player_id)
        # print(df.head())
        val = (df.loc[df['ID'] == int(player_id), rating_col])
        # a = df.loc[df['ID'] == player_id]
        # print(a.iloc[0])
        # print(sum(a.iloc[0][2:].values)/len(a.iloc[0][2:].values))
        # print(val.iloc[0], 'Pouet')
        # exit(1)
        # print(val)
        if len(val) == 0:
            print('ID {} not found.'.format(player_id))
            exit(1)
        else:
            # print(val)
            rate = val.iloc[0]
            if rate == 0.0:
                a = df.loc[df['ID'] == player_id]
                tmp = [el for el in a.iloc[0][1:].values if el != 0.0]
                l.append(float(sum(tmp)/len(tmp))/100)
            else:
                l.append(float(rate)/100)
    return np.array(np.array(l))
    # return np.array([(float(df.loc[df[id_col_name] == id, rating_col].iloc[0])/100) for id in match_ids], dtype=float)


def prepare_data(comps_df, season_matches_df):
    x_val = []
    y_val = []
    previous_date = '01/01/1900'
    year = previous_date[-4:]
    rating_df = pd.read_csv(os.path.join(cfg.data_path, 'players_rating.csv'), sep=';')

    for index, c_row in comps_df.iterrows():
        if previous_date != str(c_row['Date']):
            previous_date = c_row['Date']
            try:
                m_row = season_matches_df.loc[season_matches_df['Date'].apply(lambda x: datetime.strptime(x,'%d/%m/%y'))
                                              == datetime.strptime(str(c_row['Date']), '%d/%m/%Y')]
            except ValueError:
                m_row = season_matches_df.loc[season_matches_df['Date'].apply(lambda x: datetime.strptime(x,'%d/%m/%Y'))
                                              == datetime.strptime(str(c_row['Date']), '%d/%m/%Y')]

        if len(m_row) == 1:
            # print(c_row)
            fifa_year = str(int(str(c_row['Date'])[-2:])+1)
            match_rating = fetch_players_rating(rating_df, c_row.iloc[4:], fifa_year)
            # exit()
            x_val.append(match_rating)
            y_val.append(np.array(compute_y_val(int(m_row['FTHG']), int(m_row['FTAG']))))
        else:
            home = c_row['Team A'].lower()
            away = c_row['Team B'].lower()
            # print(home)
            if home == 'psg':
                home = 'paris sg'
            elif home == 'asse':
                home = 'st etienne'
            elif home == 'ol':
                home = 'lyon'
            elif home == 'om':
                home = 'marseille'

            select_row = m_row.loc[(m_row['HomeTeam'].str.lower() == home) |
                                   (m_row['AwayTeam'].str.lower() == away)]
            if len(select_row) == 1:
                fifa_year = str(int(str(c_row['Date'])[-2:])+1)
                match_rating = fetch_players_rating(rating_df, c_row.iloc[4:], fifa_year)
                x_val.append(match_rating)
                y_val.append(np.array(compute_y_val(int(select_row['FTHG']), int(select_row['FTAG']))))
            else:
                print('Error, didn\'t find matching row.')
                print('(Index : {}, size rows : {})'.format(index, len(select_row)))
                print(c_row)
                exit(1)

    return x_val, y_val


# dfComps = pd.read_csv(cfg.data_path + '/comps_ids_2017_2018.csv', sep=',')
# smatchesdf = pd.read_csv(cfg.data_path + '/matches_2017_2018.csv', sep=',')
#
# x_vals, y_vals = prepare_data(dfComps, smatchesdf)
#
# print(x_vals, y_vals)