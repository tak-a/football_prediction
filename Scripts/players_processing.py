#Created by taka the 1/25/21 at 3:52 PM


import config as cfg
import requests
from bs4 import BeautifulSoup
import pandas as pd


def extract_from_url(page_url):
    url_text = requests.get(page_url).text
    return BeautifulSoup(url_text, 'html.parser')


# def player_transfers(url_transfers):
#     soup = extract_from_url(url_transfers)
#
#     dic_transfers = {}
#     transfers = soup.find('table', {"class":'real-transfers'})
#     if transfers is None:
#         return dic_transfers
#     else :
#         transfers = transfers.find_all('tr', {"class":["odd", "even"]})
#
#     for tr, in transfers[::-1]:
#         date = tr.find('td', {"class":'date'}).get_text()
#         from_team, to_team = tr.find_all('td', {"class":'team'})
#         date = date[:-2] +'/20' + date[-2:]
#         dic_transfers[date] = [from_team, to_team]
#
#     return dic_transfers


def player_infos(url_infos, col):
    soup = extract_from_url(url_infos)

    seasons = soup.select('td.season')
    dic_seasons = {s: [] for s in col}

    dic_seasons['Name'] = soup.find('div', {"class":'card player-card'}).find('h5').get_text()

    id = url_infos.split('/')[4]
    dic_seasons['ID'] = id

    teams = soup.find_all('td', {"class":'team'})
    teams = [t.find('a').get('title') for t in teams]

    # note = soup.find(lambda tag:tag.name == "li" and "Overall Rating" in tag.text).find("span").get_text()
    # dic_seasons['Note'] = note

    for s,t in zip(seasons, teams):
        for season in str(s.get_text()).split('/'):
            if season in col and t not in dic_seasons[season]:
                dic_seasons[season].append(t)

    print(str(dic_seasons['Name']) + ' career dictionary created.')

    return dic_seasons


def players_career(url_infos):

    df = pd.DataFrame(columns=cfg.players_career_columns)

    for i in range(0,1801 , 60):
        soup = extract_from_url(url_infos +str(i))
        players_links = soup.find_all("a", {"class": "tooltip"})
        for pl in players_links:
            link = str(pl.get("href"))
            if 'player' in link:
                link = "/".join(link.split('/')[:-2])
                link += "/live"
                p_career = player_infos((cfg.so_fifa_url + link), list(df.columns))
                if not p_career['2020'] and not p_career['2019'] and not p_career['2018'] and not p_career['2017']:
                    continue
                df = df.append(p_career, ignore_index=True)
            # break
        # break
    return df


if __name__ == "__main__":

    url = cfg.so_fifa_players

    df = players_career(url)
    df.to_csv(cfg.data_path + '/players_career.csv', sep=';', encoding='utf-8', index=False)

    print('Player career csv saved.')
    # print(df.loc[0])
