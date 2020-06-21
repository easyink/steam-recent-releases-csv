from bs4 import BeautifulSoup
import requests
import csv
from datetime import date
import seaborn as sns
import matplotlib.pyplot as plt

namecsv = 'List of New Games Released ' + str(date.today()) + '.csv'
url_filter = 'https://store.steampowered.com/search/?sort_by=Released_DESC&untags=493&category1=998&unvrsupport=401&supportedlang=english&page='
pages_to_search = 8

def generate_csv(filename, base_url, numofpages):
    with open(filename, 'w', encoding='utf-8', newline='') as csvfile:
        writecsv = csv.writer(csvfile, delimiter=',')
        writecsv.writerow(['Name of Game', 'Release Date', 'Current Price', 'Original Price', 'Discounted?','Discount Percentage', 'Link To Game']) #base row 
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
                    is_discounted=True
                    discounted = i.find('div', class_= 'col search_price discounted responsive_secondrow')
                    game_price_list = discounted.get_text(strip=True).split("$") #splits the price string in two
                    game_price = '$' + game_price_list[2] #second one is the discounted current price
                    og_price = '$' + game_price_list[1] #first one is the original price
                    discount_percentage = i.find('div', class_='col search_discount responsive_secondrow').get_text(strip=True) #gets the percentage off
                else:
                    is_discounted=False
                    game_price = i.find('div', class_='col search_price responsive_secondrow').get_text(strip=True) 
                    og_price = ''
                    discount_percentage = ''

                if game_price and 'Free' not in game_price:
                    writecsv.writerow([ game_title , release_date , game_price, og_price, is_discounted, discount_percentage, url_link ])
    print('Generated', filename)

def generate_charts(filename):
    with open(filename, encoding='utf-8') as f:
        reader = csv.reader(f)
        header_row = next(reader)

        current_price = []
        discounted = []
        for row in reader:
            dollar_figure = float(row[2].strip('$'))
            current_price.append(dollar_figure)
            if row[4] == 'True':
                discounted.append(dollar_figure)

        dollar_bins = [0,5,10,15,20,30,40,50,60] #dollar bins
        sns.set(style='darkgrid',font_scale=1,)
        
        price_histogram = sns.distplot(current_price,bins=dollar_bins,kde=False,hist=True,color='blue',label='Games')
        price_histogram.set(xlim=0,xlabel='Price in $USD',ylabel='Number of Games',title=filename.split('.')[0])

        discount_histogram = sns.distplot(discounted,bins=dollar_bins,kde=False,color='green',label='Discounted Games',hist_kws=dict(alpha=1))
        
        patches = price_histogram.patches
        for index, item in enumerate(patches): 
            height = item.get_height()
            if index <= 7:
                price_histogram.text( x=item.get_x()+item.get_width()/2, y=height+1, s=int(height), ha='left')
            elif height == 0:
                continue
            else:
                price_histogram.text( x=item.get_x()+item.get_width()/2, y=height+1, s=int(height), ha='right')

        plt.legend()
        plt.show()


#generate_csv(namecsv,url_filter,pages_to_search)

generate_charts('List of New Games Released 2020-06-21.csv')
