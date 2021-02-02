#Created by taka the 1/25/21 at 3:52 PM


import config as cfg
import requests
from bs4 import BeautifulSoup
import pandas as pd
from unidecode import unidecode
import os

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

    dic_seasons['Name'] = unidecode(soup.find('div', {"class":'card player-card'}).find('h5').get_text())

    id = url_infos.split('/')[4]
    dic_seasons['ID'] = id

    teams = soup.find_all('td', {"class":'team'})
    teams = [unidecode(t.find('a').get('title')) for t in teams]

    # note = soup.find(lambda tag:tag.name == "li" and "Overall Rating" in tag.text).find("span").get_text()
    # dic_seasons['Note'] = note

    for s,t in zip(seasons, teams):
        for season in str(s.get_text()).split('/'):
            if season in col and t not in dic_seasons[season]:
                dic_seasons[season].append(t)

    print(str(dic_seasons['Name']) + ' career dictionary created.')

    return dic_seasons


def players_career(url_infos,):

    df = pd.DataFrame(columns=cfg.players_career_columns)

    for i in range(0,15001, 60):
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


def is_there_next(soup):
    pagination = soup.find("div", {"class":"pagination"})
    buttons = pagination.find_all("span",{"class": "bp3-button-text"})

    return ('Next' in (b.get_text() for b in buttons))


def players_career_top5(url_info, collected_ids=[]):
    dataframe = pd.DataFrame(columns=cfg.players_career_columns)

    still_players = True
    offset = 0

    while still_players:
        soup = extract_from_url(url_info + str(offset))
        players_links = soup.find_all("a", {"class": "tooltip"})
        players_ids = soup.find_all("td", {"class":"col col-pi"})

        for pl, id in zip(players_links, players_ids):
            link = str(pl.get("href"))

            if int(id.get_text()) in collected_ids:
                print('ID', id.get_text(), ' already collected, continue.')
                continue

            if 'player' in link:
                link = "/".join(link.split('/')[:-2])
                link += "/live"
                p_career = player_infos((cfg.so_fifa + link), list(dataframe.columns))

                if not p_career['2020'] and not p_career['2019'] and not p_career['2018'] and not p_career['2017']:
                    continue
                dataframe = dataframe.append(p_career, ignore_index=True)
            # break
        # break
        if not is_there_next(soup):
            still_players = False

        offset += 60
        if still_players:
            print("\n --- Next page --- ( offset :",offset, ")\n")
        else:
            print('\n')

    return dataframe


if __name__ == "__main__":


    # df = pd.DataFrame(
    #     {"Name" : ['A', 'B', 'C', 'D'],
    #      "ID": [00, 11, 22, 33]
    #
    #     }
    # )
    # ids = (df["ID"])
    # if 11 in list(ids):
    #     print('works.')
    # else:
    #     print("doesn't.")
    # for id in ids:
    #     print(type(id))
    #
    #
    # l = 'https://sofifa.com/players?type=all&lg%5B0%5D=13&lg%5B1%5D=16&lg%5B2%5D=19&lg%5B3%5D=31&lg%5B4%5D=53&showCol%5B0%5D=ae&showCol%5B1%5D=oa&showCol%5B2%5D=pi&r=210025&set=true&offset=2880'
    # soup = extract_from_url(l)
    # ids = soup.find_all("td", {"class":"col col-pi"})
    # for id in ids:
    #     print(id.get_text())
    #
    # exit(1)

    # u = 'https://sofifa.com/players?type=all&lg%5B0%5D=13&lg%5B1%5D=16&lg%5B2%5D=19&lg%5B3%5D=31&lg%5B4%5D=53&showCol%5B0%5D=ae&showCol%5B1%5D=oa&showCol%5B2%5D=pi&r=210025&set=true&offset=2880'
    # r = 'https://sofifa.com/players?type=all&lg%5B0%5D=13&lg%5B1%5D=16&lg%5B2%5D=19&lg%5B3%5D=31&lg%5B4%5D=53&showCol%5B0%5D=ae&showCol%5B1%5D=oa&showCol%5B2%5D=pi&r=210025&set=true&offset=2940'
    # soup = extract_from_url(r)
    # pagination = soup.find("div", {"class":"pagination"})
    # buttons = pagination.find_all("span",{"class": "bp3-button-text"})
    #
    # if 'Next' not in (b.get_text() for b in buttons):
    #     print("Pas de next, on stop.")
    # else:
    #     print("On continue.")
    #
    # exit(1)
    # url = cfg.so_fifa_players

    # df = players_career(url)

    ids = []
    final_df = pd.DataFrame()
    for url in cfg.so_fifa_top5_urls:
        print('----- New URL ----- \n')
        df = players_career_top5(url, ids)
        ids = ids + list(df["ID"])
        final_df.append(df, ignore_index=True)

    final_df.to_csv(cfg.data_path + '/players_career_top5.csv', sep=',', encoding='utf-8', index=False)

    print('Player career csv saved.')
    # print(df.loc[0])
