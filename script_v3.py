from bs4 import BeautifulSoup
import requests
import csv
from datetime import date

csvname = 'List of New Games Released ' + str(date.today()) + '.csv'
def generate_csv(numofpages):
    with open(csvname, 'w', encoding='utf-8', newline='') as csvfile:
            writecsv = csv.writer(csvfile, delimiter=',')
            writecsv.writerow(['Name of Game', 'Release Date', 'Link To Game']) #base row 
            for num in range( 1 , numofpages+1 ):
                url = 'https://store.steampowered.com/search/?sort_by=Released_DESC&category1=998&unvrsupport=401&supportedlang=english&page=' + str(num)
                get_online_html = requests.get(url)
                html_name = 'steampage_' + str(num) + '.html'
                with open(html_name, 'wb',) as local_file:
                    local_file.write(get_online_html.content)
                with open(html_name,'rb') as local_file:
                    html_contents = local_file.read()
                    soup = BeautifulSoup(html_contents, 'lxml')
                    get_list = soup.find(id = 'search_resultsRows') #narrows it down to find the right section
                    game_entry = get_list.find_all('a', href=True) #actual list of games 
                    for i in game_entry:
                        url_link = i['href']
                        game_title = i.find('span', class_='title').get_text()
                        release_date = i.find('div', class_='col search_released responsive_secondrow').get_text()
                        writecsv.writerow([ game_title , release_date , url_link ]) #write to csv!!
                        #print('NAME:', game_title)
                        #print('URL:', url_link)
                        #print('RELEASE DATE:', release_date)
    print('Generated', csvname)

generate_csv(8)