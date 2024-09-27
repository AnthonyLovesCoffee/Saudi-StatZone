from bs4 import BeautifulSoup
import pandas as pd
import requests 
import time

teams = []  # list to store all teams

html = requests.get('https://fbref.com/en/comps/70/Saudi-Professional-League-Stats').text  # requesting html
soup = BeautifulSoup(html, 'lxml')
table = soup.find_all('table', class_='stats_table')[0]  # only accessing first table

links = table.find_all('a')
links = [l.get("href") for l in links]  # parsing through links
links = [l for l in links if '/squads/' in l]  # filtering through links to only get squads

team_urls = [f"https://fbref.com{l}" for l in links]  # formatting back to links

# loop through each team URL
for i, team_url in enumerate(team_urls, 1): 
    team_name = team_url.split("/")[-1].replace("-Stats", "")  # isolating the names of the teams
    print(f"Scraping data for team {i}/{len(team_urls)}: {team_name}...")

    try:
        data = requests.get(team_url).text
        soup = BeautifulSoup(data, 'lxml')
        stats = soup.find_all('table', class_="stats_table")[0]  # again, only want the first table

        # Assuming 'team_data' is a BeautifulSoup Tag
        team_data = pd.read_html(str(stats))[0]
        team_data["Team"] = team_name
        teams.append(team_data)  # appending the data
        
        print(f"Successfully scraped data for {team_name}.")
    except Exception as e:
        print(f"Failed to scrape data for {team_name}: {e}")
    
    time.sleep(5)  # avoid getting blocked from scraping

print("Finished scraping team data")

stat_df = pd.concat(teams) # concatenating all of the stats
stat_df.to_csv("stats.csv") # importing to csv