import os
import requests
import re
import argparse
import pandas as pd
from bs4 import BeautifulSoup

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-y", "--Year", type=int, help="Year")

    return parser.parse_args()

def main():
    args = parse_args()

    url = "https://www.sports-reference.com/cbb/conferences/"
    page = requests.get(url)
    bs = BeautifulSoup(page.content, 'html.parser')

    year = args.Year
    print(year)

    activeTable = bs.find('div', {"id":"all_active"})
    defunctTable = bs.find('div', {"id":"div_defunct"})
    
    activeRows = activeTable.find_all("tr") 
    defunctRows = defunctTable.find_all("tr") 
    rows = activeRows[1:len(activeRows)] + defunctRows[1:len(defunctRows)]
    
    confAbbrv = pd.DataFrame()

    regex = "/cbb/conferences/(.*)/\""

    for x in rows:
        data = x.select('td')
        yearMin = [i for i in data if i['data-stat'] == 'year_min'][0].get_text()
        yearMax = [i for i in data if i['data-stat'] == 'year_max'][0].get_text()

        if int(year) < int(yearMin) or int(year) > int(yearMax):
            continue

        a = x.find('a')
        conf = a.get_text()
        abbrv = re.search(regex,str(a)).group(1)
        confAbbrv = confAbbrv.append({
            'Name' : conf,
            'Abbreviation': abbrv
        }, ignore_index = True)

    confs = pd.DataFrame()
    nameRegex = "/cbb/schools/(.*)/"

    abbrvs = dict(zip(confAbbrv.Name.tolist(), confAbbrv.Abbreviation.tolist()))

    for conf in confAbbrv.Name:
        confUrl = url + "/{}/{}.html".format(abbrvs[conf],year)
        confPage = requests.get(confUrl)
        confBs = BeautifulSoup(confPage.content, 'html.parser')
        teams = confBs.findAll('td', {"data-stat":"school_name"})
        for team in teams:
            if "Was not considered a major school this season" in str(team):
                continue
            teamLink = team.find('a')['href']
            name = re.search(nameRegex, teamLink).group(1)
            confs = confs.append({
                'School' : name,
                'Conference' : conf
            }, ignore_index = True)

    confDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../static/ConferenceData")
    
    confAbbrv[['Name', 'Abbreviation']].to_csv(os.path.join(confDir, "{}_ConferenceAbbreviations.csv").format(year), index = False)
    confs[['School', 'Conference']].to_csv(os.path.join(confDir, "{}_SchoolToConferenceMap.csv".format(year)), index = False)

if __name__ == "__main__": main()