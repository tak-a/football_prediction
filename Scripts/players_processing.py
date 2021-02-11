# Created by taka the 1/25/21 at 3:52 PM

"""
Script to fetch the career for football players in the top 5 league
(Premier League, Ligue 1, Liga, Serie A and Bundesliga)
from 2015 to 2021)
for each player, we get the following information :
Name, ID, 2015, ..., 2021
It's then stocked in a csv named "players_career_top5.csv"
"""

import config as cfg
import processing_utils as proc
import pandas as pd
from unidecode import unidecode


def player_transfers(transfers_data):
    """
    from the url of the player's info,
    get the his transfer info,
    with the year, the club he left and joined

    :param transfers_data: transfers info of the player
    :return: dictionary, with all his transfer as the following form:
             {year:[from_team, to_team]
    """
    dic_transfers = {}

    transfers = transfers_data.find_all('tr', {"class": ["odd", "even"]})

    for tr in transfers[::-1]:
        date = tr.find('td', {"class": 'date'}).get_text()
        from_team, to_team = tr.find_all('td', {"class": 'team'})
        from_team = unidecode(from_team.find("a").get("title"))
        to_team = unidecode(to_team.find("a").get("title"))

        if int(date[-2:]) < 22:
            date = '20' + date[-2:]
        else:
            date = '19' + date[-2:]

        dic_transfers[date] = [from_team, to_team]

    return dic_transfers


def player_info(url_info, col):
    """
    from the url info, get all the desired information concerning the player
    :param url_info: link of the player's webpage
    :param col: columns of the DataFrame representing the information that we want to collect
    :return: dictionary,  with all the wanted information of the player
    """
    soup = proc.extract_from_url(url_info)

    seasons = soup.select('td.season')
    dic_seasons = {s: [] for s in col}

    dic_seasons['Name'] = unidecode(soup.find('div', {"class": 'card player-card'}).find('h5').get_text())

    player_id = url_info.split('/')[4]
    dic_seasons['ID'] = player_id

    teams = soup.find_all('td', {"class": 'team'})
    teams = [unidecode(t.find('a').get('title')) for t in teams]

    if not teams:
        print('(No career info found for ' + str(dic_seasons['Name']) + '.)')
        for s in col:
            if s.isdigit():
                dic_seasons[s].append('N/A')

    transfers_info = soup.find('table', {"class": 'real-transfers'})

    if transfers_info is None or transfers_info == []:
        transfers = {}
    else:
        transfers = player_transfers(transfers_info)

    # print('transfers : \n', transfers)

    for s, t in zip(seasons, teams):
        # print('saison :', s.get_text())
        # print('teams :', t, '\n')
        for season in str(s.get_text()).split('/'):

            if season in col and t not in dic_seasons[season] and 'II' not in t:
                if (season in transfers and transfers[season][1] == t)or \
                        (season in transfers and transfers[season][0] == t) or \
                        not (str(int(season) - 1) in transfers and t in transfers[str(int(season) - 1)][0]):
                    dic_seasons[season].append(t)

    print(str(dic_seasons['Name']) + ' career dictionary created.')

    return dic_seasons


def is_there_next(soup):
    """
    from the webpage data, determine if there is another page
    with other players to collect data about
    :param soup: webpage text
    :return: boolean, True if there is another page, False otherwise
    """
    pagination = soup.find("div", {"class": "pagination"})
    buttons = pagination.find_all("span", {"class": "bp3-button-text"})

    return 'Next' in (b.get_text() for b in buttons)


def players_career_top5(url_info, collected_ids=[]):
    """
    for each player present on the webpage, collect its data,
    go on with the next page, until there is no more player
    :param url_info: webpage listing all player
    :param collected_ids: players FIFA ID for which we already have data
    :return: Dataframe, containing all player info collected
    """
    players_df = pd.DataFrame(columns=cfg.players_career_columns)

    still_players = True
    offset = 0

    while still_players:
        soup = proc.extract_from_url(url_info + str(offset))
        players_links = soup.find_all("a", {"class": "tooltip"})
        players_ids = soup.find_all("td", {"class": "col col-pi"})

        for pl, p_id in zip(players_links, players_ids):
            link = str(pl.get("href"))

            if p_id.get_text() in collected_ids:
                print('ID', p_id.get_text(), ' already collected, continue.')
                continue

            if 'player' in link:
                link = "/".join(link.split('/')[:-2])
                link += "/live"
                p_career = player_info((cfg.so_fifa + link), list(players_df.columns))

                players_df = players_df.append(p_career, ignore_index=True)

        if not is_there_next(soup):
            still_players = False

        offset += 60
        if still_players:
            print("\n --- Next page --- ( offset :", str(offset), ")\n")
        else:
            print('\n')

    return players_df


if __name__ == "__main__":

    # rlopes = 'https://sofifa.com/player/212692/marcos-paulo-mesquita-lopes/live'
    # diclopes = player_info(rlopes, cfg.players_career_columns)
    # print(diclopes)
    # exit(1)

    ids = []
    final_df = pd.DataFrame(columns=cfg.players_career_columns)

    for i, url in enumerate(cfg.so_fifa_top5_urls):
        print('----- New URL : ' + str(i) + 'eme url----- \n')
        df = players_career_top5(url, ids)
        ids = ids + list(df["ID"])
        final_df = final_df.append(df, ignore_index=True)

    final_df.to_csv(cfg.data_path + '/players_career_top5_TEST.csv', sep=';', encoding='utf-8', index=False)

    print('Player career csv saved.')
