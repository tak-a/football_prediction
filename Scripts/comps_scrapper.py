# Created by taka the 2021-01-18 at 16:55

import re
import processing_utils as proc
import pandas as pd
import config as cfg
import unidecode


def get_matchs_url(page):
    """
    Get the links of the matches from the page text
    :param page: BS4 element, html code of the page
    :return: list, matches' links
    """
    matches = page.find_all(href=re.compile('match-direct'))
    return [str(m.get("href")) for m in matches]


def get_teams_names(match_id):
    """
    get the names of both teams of the match
    :param match_id: string, contains names of the teams
    :return:tuple, the 2 names separated
    """
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


def get_comp_match(match_url):
    """
    get both teams composition for a specific match
    :param match_url:string, url of the match
    :return:tuple, ("team1-team2",[22 starting players of the match])
    """
    match_id = match_url.split('/')[-2]
    match_id = match_id[:-5]
    soup_comp = proc.extract_from_url(cfg.lequipe + match_url + '/compositions')

    players = soup_comp.find_all('span', {'class': 'fieldPlayer__title'})
    if not players:  # if empty list => means different method to show comp on website
        players = soup_comp.find_all('a', {'class': 'link'})

    players = [p.get_text().strip() for p in players]

    return match_id, players


def get_match_date(match_url):
    """
    get the year of the match
    :param match_url:
    :return:
    """
    match_soup = proc.extract_from_url(cfg.lequipe + match_url)
    match_header = match_soup.find("h1", {"class": "heading heading--1"})
    m_date = match_header.get_text().split()[-3:]
    m_date = m_date[0] + '/' + str(cfg.years.index(m_date[1])).zfill(2) + '/' + m_date[2]

    return m_date


def get_comps_day(day_matches_url):
    """
    return all the matches team composition from one day of the season
    :param day_matches_url: list, urls of all the matches for the day
    :return: tuple, (dictionnary => {'match_id': [match_comp], list => matches dates)
    """
    dic_matches_comp = {}
    matches_dates = []
    for m_url in day_matches_url:
        match_date = get_match_date(m_url)
        matches_dates.append(match_date)
        mid, players = get_comp_match(m_url)
        players = match_players_ids(mid, players, match_date[-4:])
        dic_matches_comp[mid] = players
        print('Composition of match {} collected.'.format(mid))

    return dic_matches_comp, matches_dates


def match_players_ids(match_id, players, year):
    """
    for a specific match, fetch the 22 starting players id
    :param match_id: string, the names of the teams
    :param players: list, names of the 22 starting players
    :param year: string, year of the match
    :return: list, containing th ids of the 22 starting player
    """
    team_a, team_b = get_teams_names(match_id)
    career_df = pd.read_csv(cfg.career_top5_file, sep=',')
    comps_ids = []

    for i, p in enumerate(players):
        p_name = check_player_name(p)

        if i < 11:
            club = team_a
        else:
            club = team_b

        if club == 'paris-sg':
            club = 'psg'

        matching_row = career_df[(career_df[year].str.contains("(?i)" + club) &
                                  unidecode.unidecode(career_df['Name'].str).contains("(?i)" +
                                                                                      unidecode.unidecode(p_name)))]

        if matching_row.shape[0] != 1:
            comps_ids.append('N/A')
        else:
            comps_ids.append(matching_row['ID'].iloc[0])

    return comps_ids


def check_player_name(player):
    """
    If the variable player doesn't contain only the lastname (ex : L. Messi)
    remove the start to keep only the lastname
    :param player: string, name of the player
    :return: the lastname only of the player
    """
    name = player.split(". ")
    if len(name) == 1:
        return name[0]
    else:
        return " ".join(name[1:])


if __name__ == "__main__":

    for i in range(2017, 2018):
        url = cfg.ligue1_season_calendar.format(i, i+1)
        col = ['Day', 'Date', 'Team A', 'Team B']
        col.extend(["T{} player {}".format(j, i) for j in ['A', 'B'] for i in range(1, 12)])
        df = pd.DataFrame(columns=col)

        for j in range(1, 39):
            if j == 1:
                day = '1ere-journee'
            else:
                day = str(j) + 'e-journee'

            print(day)
            soup = proc.extract_from_url(url + day)

            matches_url = get_matchs_url(soup)
            comps, m_dates = get_comps_day(matches_url)

            # add each match to the DataFrame with
            for k, (player_id, date) in enumerate(zip(comps, m_dates)):
                row = [j] + [date] + list(get_teams_names(player_id)) + comps[player_id]
                df.loc[(j-1)*10 + k] = row

            # break

            print("Previous compositions added to the DataFrame. \n")

        df.to_csv(cfg.data_path + "/test_comps_ids_{}_{}.csv".format(i, i+1), sep=';', encoding='utf-8', index=False)

        print(str(i) + '_' + str(i+1) + ' csv created.')
