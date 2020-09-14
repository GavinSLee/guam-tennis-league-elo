import time
import re
import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


def get_driver():
    path = r"C:\Users\Gavin Lee\Documents\side_projects\register_courses\chromedriver.exe"
    web_driver = Chrome(path)
    return web_driver


def goto_league_link(driver):
    link = "https://gntf.org/tennis-league/page/league/listGame.php?part=lg&xc=51"
    driver.get(link)


def get_all_matches(driver):

    form_control = driver.find_element_by_class_name('form-control')
    leagues = driver.find_elements_by_tag_name('option')

    for k in range(25, len(leagues)):
        time.sleep(2)
        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
        print(k)
        time.sleep(2)
        driver.find_element_by_class_name('form-control-sm').click()
        time.sleep(2)
        leagues = driver.find_elements_by_tag_name('option')
        season = str(leagues[k].text)
        leagues[k].click()
        time.sleep(2) 

        match_table = driver.find_elements_by_tag_name("tr")

        column_headers = ['Season', 'Week', 'Date', 'Home Team', 'Visitor Team', 'Home Player One', 'Home Player One Rating', 'Home Player Two', 'Home Player Two Rating',
                          'Visitor Player One', 'Visitor Player One Rating', 'Visitor Player Two', 'Visitor Player Two Rating', 'Home Score', 'Visitor Score']

        df = pd.DataFrame([column_headers])

        for i in range(2, len(match_table)):
            time.sleep(2)
            match_table = driver.find_elements_by_tag_name("tr")
            curr_row = match_table[i].find_elements_by_tag_name("td")
            week = str(curr_row[0].text)
            date = str(curr_row[1].text)
            home_team = str(curr_row[2].text)
            visitor_team = str(curr_row[3].text)
            if home_team == "Bye" or visitor_team == "Bye":
                continue
            curr_week_info = [season, week, date, home_team, visitor_team]

            curr_info_btn = curr_row[len(curr_row
                                         ) - 1].find_element_by_class_name(
                "fa-info-circle")
            curr_info_btn.click()
            time.sleep(1)

            # Now inside current match up history
            matches_row = driver.find_elements_by_tag_name("tbody")

            for j in range(len(matches_row) - 2):
                match_info = []
                curr_match = matches_row[j].find_elements_by_tag_name("td")

                home_players = (curr_match[1].text)
                home_players_list = home_players.split("\n")

                if home_players_list[0] == "()":
                    home_player_one = "()"
                    home_player_one_rating = "0.0"
                else:
                    player_one = home_players_list[0]
                    player_one_list = player_one.split("(")

                    home_player_one = player_one_list[0].strip()
                    home_player_one_rating = player_one_list[1].split(")")[0]

                if home_players_list[1] == "()":
                    home_player_two = "()"
                    home_player_two_rating = "0.0"
                else:
                    player_two = home_players_list[1]
                    player_two_list = player_two.split("(")

                    home_player_two = player_two_list[0].strip()
                    home_player_two_rating = player_two_list[1].split(")")[0]

                visiting_players = (curr_match[3].text)
                visiting_players_list = visiting_players.split("\n")

                if visiting_players_list[0] == "()":
                    visiting_player_one = "()"
                    visiting_player_one_rating = "0.0"
                else:
                    player_one = visiting_players_list[0]
                    player_one_list = player_one.split("(")

                    visiting_player_one = player_one_list[0].strip()
                    visiting_player_one_rating = player_one_list[1].split(")")[
                        0]

                if visiting_players_list[1] == "()":
                    visiting_player_two = "()"
                    visiting_player_two_rating = "0.0"
                else:
                    player_two = visiting_players_list[1]
                    player_two_list = player_two.split("(")

                    visiting_player_two = player_two_list[0].strip()
                    visiting_player_two_rating = player_two_list[1].split(")")[
                        0]

                score = str(curr_match[5].text)
                if score == "-":
                    home_score = "No Score Inputted"
                    visitor_score = "No Score Inputted"
                else:
                    final_score = score.split("- ")
                    home_score = final_score[0].split(" ")[0]
                    visitor_score = final_score[1].split(" ")[0]

                match_info.append(home_player_one.encode('utf-8'))
                match_info.append(home_player_one_rating.encode('utf-8'))
                match_info.append(home_player_two.encode('utf-8'))
                match_info.append(home_player_two_rating.encode('utf-8'))

                match_info.append(visiting_player_one.encode('utf-8'))
                match_info.append(visiting_player_one_rating.encode('utf-8'))
                match_info.append(visiting_player_two.encode('utf-8'))
                match_info.append(visiting_player_two_rating.encode('utf-8'))

                match_info.append(home_score)
                match_info.append(visitor_score)
                final_match_info = curr_week_info + match_info

                df2 = pd.DataFrame([final_match_info])
                df = df.append(df2)

            csv_name = season + '.csv'
            df.to_csv(csv_name, index=False)

            driver.back()


if __name__ == "__main__":
    driver = get_driver()
    goto_league_link(driver)
    get_all_matches(driver)
    driver.close()
