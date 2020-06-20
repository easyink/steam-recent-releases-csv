from bs4 import BeautifulSoup
import requests
import csv
from datetime import date

namecsv = 'List of New Games Released ' + str(date.today()) + '.csv'
url_filter = 'https://store.steampowered.com/search/?sort_by=Released_DESC&untags=493&category1=998&unvrsupport=401&supportedlang=english&page='
pages_to_search = 8

def generate_csv(csvname, base_url, numofpages):
    with open(csvname, 'w', encoding='utf-8', newline='') as csvfile:
        writecsv = csv.writer(csvfile, delimiter=',')
        writecsv.writerow(['Name of Game', 'Release Date', 'Current Price', 'Original Price', 'Discount Percentage', 'Link To Game']) #base row 
        for num in range( 1 , numofpages+1 ):
            url = base_url + str(num)
            print('Went To ', url)
            get_online_html = requests.get(url)
            soup = BeautifulSoup(get_online_html.content, 'lxml')
            get_list = soup.find(id = 'search_resultsRows') #narrows it down to the right section
            game_entry = get_list.find_all('a', href=True) #actual list of games 
            for i in game_entry: #iterates per game in current page
                url_link = i['href'].split('?')[0]
                game_title = i.find('span', class_='title').get_text()
                release_date = i.find('div', class_='col search_released responsive_secondrow').get_text()
                if i.find('div', class_= 'col search_price discounted responsive_secondrow'): #if game is discounted
                    discounted = i.find('div', class_= 'col search_price discounted responsive_secondrow')
                    game_price_list = discounted.get_text(strip=True).split("$") #splits the price string in two
                    game_price = '$' + game_price_list[1] #first one is the discounted current price
                    og_price = '$' + game_price_list[2] #second one is the original price
                    discount_percentage = i.find('div', class_='col search_discount responsive_secondrow').get_text(strip=True) #gets the percentage off
                else:
                    game_price = i.find('div', class_='col search_price responsive_secondrow').get_text(strip=True) 
                    og_price = ''
                    discount_percentage = ''

                if game_price and 'Free' not in game_price:
                    writecsv.writerow([ game_title , release_date , game_price, og_price, discount_percentage, url_link ])
    print('Generated', csvname)

generate_csv(namecsv,url_filter,pages_to_search)
