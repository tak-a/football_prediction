# Created by taka the 14-02-2021 at 16:14

import pandas as pd
import config as cfg
import os

if __name__ == '__main__':
    ratings_df = pd.DataFrame({}, columns=['ID', '17', '18', '19', '20', '21'])

    for i in range(17, 22):
        print('Starting the collect of players rating in fifa {} csv.'.format(i))
        dataset_info = cfg.players_dataset_info[str(i)]
        delim = dataset_info[-2]
        id_col = dataset_info[-1]
        rating = dataset_info[2]
        fifa_df = pd.read_csv(os.path.join(cfg.data_path, 'players_{}.csv'.format(i)), sep=delim)

        for idx, row in fifa_df.iterrows():

            if len(ratings_df.loc[ratings_df['ID'] == int(row[id_col])]) == 0:
                ratings_df = ratings_df.append({c: (int(row[id_col]) if c == 'ID' else 0) for c in ratings_df.columns},
                                               ignore_index=True)

            ratings_df.loc[ratings_df.ID == int(row[id_col]), str(i)] = float(row[rating])
        print('Fifa {} csv rating collected.'.format(i))

    ratings_df.to_csv(os.path.join(cfg.data_path, 'players_rating.csv'), sep=',')
