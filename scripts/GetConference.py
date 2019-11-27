import os
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup

def main():
    url = "https://www.sports-reference.com/cbb/conferences/"
    page = requests.get(url)
    bs = BeautifulSoup(page.content, 'html.parser')

    year = "2019"

    tbl = bs.find('div', {"id":"all_active"})
    
    rows = tbl.find_all("tr") 
    rows = rows[1:len(rows)]
    
    confAbbrv = pd.DataFrame()

    regex = "/cbb/conferences/(.*)/\""

    for x in rows:
        a = x.find('a')
        conf = a.get_text()
        abbrv = re.search(regex,str(a)).group(1)
        confAbbrv = confAbbrv.append({
            'Name' : conf,
            'Abbreviation': abbrv
        }, ignore_index = True)

    confs = pd.DataFrame()
    nameRegex = "/cbb/schools/(.*)/"

    #confs = confAbbrv.keys()

    abbrvs = dict(zip(confAbbrv.Name.tolist(), confAbbrv.Abbreviation.tolist()))

    for conf in confAbbrv.Name:
        if conf == "American Athletic Conference" and int(year) < 2014:
            continue
        confUrl = url + "/{}/{}.html".format(abbrvs[conf],year)
        confPage = requests.get(confUrl)
        confBs = BeautifulSoup(confPage.content, 'html.parser')
        teams = confBs.findAll('td', {"data-stat":"school_name"})
        for team in teams:
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