import pandas as pd
import numpy as np
import glob


def concatenate_csv():
    path = r'C:\Users\Gavin Lee\Desktop\guam_tennis_league_elo\match_history\Women'
    all_files = glob.glob(path + "/*.csv")

    li = []

    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)

    frame = pd.concat(li, axis=0, ignore_index=True)
    frame.to_csv('Women Master Match History.csv', index=False)
    print("Done")


def delete_error_matches():
    df = pd.read_csv(
        r"C:\Users\Gavin Lee\Desktop\guam_tennis_league_elo\Men Master Match History.csv")
    df = df[df['Visitor Score'] != 'No Score Inputted']
    df = df[df['Home Score'] != 'No Score Inputted']

    df = df[df['Home Player One'] != '()']
    df = df[df['Home Player Two'] != '()']

    df = df[df['Visitor Player One'] != '()']
    df = df[df['Visitor Player Two'] != '()']
    df.to_csv('Men Master Match History (Cleaned).csv', index=False)


def more_cleaning():
    df = pd.read_csv(
        r"C:\Users\Gavin Lee\Desktop\guam_tennis_league_elo\Men Master Match History (Cleaned).csv")

    df.loc[df['Season'] == "2014 Men's Tennis League",
           'Season'] = "2014 Men's Fall Tennis League"

    df.to_csv("Men Master Match History (Cleaned).csv", index=False)

if __name__ == "__main__":
    more_cleaning()
