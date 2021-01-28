# Created by taka the 2021-01-18 at 16:55

import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import config as cfg
import unidecode


# return html text from the url
def extract_from_url(url):
    url_text = requests.get(url).text
    return BeautifulSoup(url_text, 'html.parser')


# get all the matches url
def get_matchs_url(page):
    matches = page.find_all(href=re.compile('match-direct'))
    return [str(m.get("href")) for m in matches]


def get_teams_names(match_id):
    splitted = match_id.split('-')
    if match_id.count('-') == 1:  # classic team names
        return tuple(splitted)
    elif match_id.count('-') == 2:  # either paris-sg or saint-etienne in it
        if splitted[0] in ['paris', 'saint']:
            return '-'.join(splitted[:2]), splitted[2]
        else:
            return splitted[0], '-'.join(splitted[1:])
    else: # both PSG and SE in it
        return '-'.join(splitted[:2]), '-'.join(splitted[2:])


# get team composition for a specific match
# return :
# - match_id : name of both team ('team1-team2)
# - players : the 22 starting players
def get_comp_match(match_url):
    match_id = match_url.split('/')[-2]
    match_id = match_id.split('-')[:-1]
    match_id = ('-').join(match_id)
    soup = extract_from_url(cfg.website + match_url + '/compositions')

    players = soup.find_all('span', {'class': 'fieldPlayer__title'})
    if not players:  # if empty list => means different method to show comp on website
        players = soup.find_all('a', {'class': 'link'})

    players = [p.get_text().strip() for p in players]

    return match_id, players


# return all the matches team composition from one day
def get_comps_day(day_matches_url, year):
    dic_matches_comp = {}

    for m_url in day_matches_url:
        mid, players = get_comp_match(m_url)
        players = match_players_id(mid, players, year)
        dic_matches_comp[mid] = players

    return dic_matches_comp


def match_players_id(m_id,players, year):
    teamA, teamB = get_teams_names(m_id)
    n_players = [get_player_id(p, teamA, year) if i < 11 else get_player_id(p, teamB, year)
                 for i, p in enumerate(players)]

    return n_players


def check_player_name(player):
    splitted = player.split(". ")
    if len(splitted) > 1:
        return splitted[-1]
    else:
        return player


def get_player_id(player, club, year, nextyear = False):
    p_name = check_player_name(player)
    players_dataset = 'players_' + year[-2:] + '.csv'
    dt_infos = cfg.players_dataset_infos[year]
    df = pd.read_csv('../Data/' + players_dataset, delimiter=dt_infos[-1])
    if club == 'paris-sg':
        club = 'psg'
    print(p_name, club)
    df[dt_infos[0]] = df[dt_infos[0]].apply(unidecode.unidecode)
    player_row = df[((df[dt_infos[0]].str.contains("(?i)"+unidecode.unidecode(p_name))) &
                    (df[dt_infos[1]].str.contains("(?i)"+club)))]
    print(player_row['ID'], 'pouet')
    if len(player_row) != 1:
        if not nextyear:
            nextyear_res = get_player_id(player, club, str(int(year)+1), True)

        if nextyear or nextyear_res == 'N/A':
            return 'N/A'

    else:
        return int(player_row['ID'])


def get_player_id_sofifa(player, club, year):
    player = check_player_name(player)
    sofifa = cfg.sofifa_player_search
    sofifa += player
    sf_soup = extract_from_url(sofifa)
    print(sf_soup)
    #sf_text.find_all(href=re.compile('match-direct'))
    mydivs = sf_soup.findAll("tbody", {"class": "list"})
    print("Pouet \n\n",mydivs)


if __name__ == "__main__":

    get_player_id_sofifa("Messi", "Barcelone", 2018)
    exit(1)

    for i in range(2017, 2019):
        url = cfg.website + '/Football/ligue-1/saison-' + str(i) + '-' + str(i+1) + '/page-calendrier-resultats/'
        col = ['Day', 'Team A', 'Team B']
        col.extend([str('T' + j + ' player ' + str(i)) for j in ['A', 'B'] for i in range(1, 12)])
        df = pd.DataFrame(columns=col)

        for j in range(1,39):
            if j == 1:
                day = '1ere-journee'
            else:
                day = str(j) +'e-journee'

            soup = extract_from_url(url + day)

            matches_url = get_matchs_url(soup)
            comps = get_comps_day(matches_url, str(i+1))
            # add each match to the dataframe with
            for k, m_id in enumerate(comps):
                row = [j] + list(get_teams_names(m_id)) + comps[m_id]
                #print(row)
                df.loc[(j-1)*10 + k] = row

        df.to_csv('../Data/test_comps_' + str(i)+ '_' + str(i+1) + '.csv',sep=';', encoding='utf-8', index=False)

        print(str(i) + '_' + str(i+1) + ' csv created.')
