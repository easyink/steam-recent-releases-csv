from bs4 import BeautifulSoup
import requests
import csv
from datetime import date

namecsv = 'List of New Games Released ' + str(date.today()) + '.csv'
url_filter = 'https://store.steampowered.com/search/?sort_by=Released_DESC&category1=998&unvrsupport=401&supportedlang=english&page='
pages_to_search = 8

def generate_csv(csvname, base_url, numofpages):
    with open(csvname, 'w', encoding='utf-8', newline='') as csvfile:
        writecsv = csv.writer(csvfile, delimiter=',')
        writecsv.writerow(['Name of Game', 'Release Date', 'Link To Game']) #base row 
        for num in range( 1 , numofpages+1 ):
            url = base_url + str(num)
            print('Went To ', url)
            get_online_html = requests.get(url)
            soup = BeautifulSoup(get_online_html.content, 'lxml')
            get_list = soup.find(id = 'search_resultsRows') #narrows it down to the right section
            game_entry = get_list.find_all('a', href=True) #actual list of games 
            for i in game_entry: #iterates per game in current page
                url_link = i['href']
                game_title = i.find('span', class_='title').get_text()
                release_date = i.find('div', class_='col search_released responsive_secondrow').get_text()
                writecsv.writerow([ game_title , release_date , url_link ]) #write to csv!!
    print('Generated', csvname)

generate_csv(namecsv,url_filter,pages_to_search)