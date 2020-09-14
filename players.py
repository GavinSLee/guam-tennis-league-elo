import time
import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


def get_driver():
    path = r"C:\Users\Gavin Lee\Documents\side_projects\register_courses\chromedriver.exe"
    web_driver = Chrome(path)
    return web_driver


def goto_league_link(driver):
    link = "https://gntf.org/tennis-league/page/league/listTeam.php?part=lt&xc=1"
    driver.get(link)


def click_on_team(driver):

    form_control = driver.find_element_by_class_name('form-control')
    league_options = form_control.find_elements_by_tag_name('option')

    for k in range(1, len(league_options)):
        time.sleep(2) 
        driver.find_element_by_class_name('form-control').click() 
        time.sleep(2) 
        league_options = driver.find_elements_by_tag_name('option')
        curr_league = league_options[k].click()
        current_season = driver.find_element_by_class_name('card-header').text

        # Gets all teams into a list
        teams = driver.find_elements_by_xpath(
            '//*[@title="View Player Information"]')
        num_teams = len(teams)

        df = pd.DataFrame([['Player', 'Rating', 'Team', 'Season']])

        for i in range(0, num_teams, 2):
            time.sleep(2) 
            teams = driver.find_elements_by_xpath(
                '//*[@title="View Player Information"]')
            # Clicks on each team, which is at every even index
            team_name = (teams[i].text)

            teams[i].click()
            time.sleep(2) 

            # Now we're at the team page
            player_list = get_all_players_on_team(driver)
            df2 = write_player_list_to_df(player_list, team_name, current_season)
            df = df.append(df2)
            driver.back()

        csv_name = str(current_season) + ".csv"
        df.to_csv(csv_name, index=False)


def get_all_players_on_team(driver):
    player_list = driver.find_elements_by_tag_name("td")
    return player_list


def write_player_list_to_df(player_list, team_name, season):

    num_players = len(player_list)

    players_and_ratings = []

    for i in range(0, num_players, 2):
        row = []
        row.append(str(player_list[i].text.encode('utf-8')))
        row.append(str(player_list[i+1].text))
        row.append(team_name)
        row.append(season)

        players_and_ratings.append(row)

    df = pd.DataFrame(players_and_ratings)
    return df


if __name__ == "__main__":
    driver = get_driver()
    goto_league_link(driver)
    click_on_team(driver)
    driver.close()

