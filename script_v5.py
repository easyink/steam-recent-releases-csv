from bs4 import BeautifulSoup
import requests
from datetime import date,timedelta
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def read_html(filename,base_url,numofpages):
    for num in range( 1, numofpages+1 ):
        url_with_page = base_url + str(num)
        print('Went To ', url_with_page)
        requested_url = requests.get(url_with_page)
        soup = BeautifulSoup(requested_url.content, 'lxml')
        get_game_entry_from_list = ( ( soup.find( id= 'search_resultsRows') ).find_all( 'a', href=True) )
        for game in get_game_entry_from_list:
            game_url = game['href'] .split('?')[0]
            game_title = game.find('span', class_='title') .get_text()
            game_release_date = ( game.find( 'div', class_='col search_released responsive_secondrow' ).get_text() ) .replace(',','')
            if game.find( 'div', class_= 'col search_price discounted responsive_secondrow'): #if game is discounted
                game_price_list = game.find('div', class_= 'col search_price discounted responsive_secondrow') .get_text(strip=True) .split('$')
                original_price = game_price_list[1]
                current_price = game_price_list[2]
                is_discounted = True
                discount_percentage = game.find('div', class_='col search_discount responsive_secondrow').get_text(strip=True) #gets the percentage off
            else:
                current_price = game.find('div', class_='col search_price responsive_secondrow').get_text(strip=True)
                original_price = ''
                discount_percentage = ''
                is_discounted = False
            if current_price and 'Free' not in original_price:
                game_dict_entry = {'Title of Game':game_title,'Release Date': game_release_date, 'Current Price': current_price,'Original Price': original_price,'Is Discounted': is_discounted,'Discount Percentage': discount_percentage,'Link To Game':game_url}
                game_list.append(game_dict_entry)
    print("Read HTML")

def generate_panda_dataframe(data_dict,csv_filename):
    game_df = pd.DataFrame(data=data_dict,)

    game_df .to_csv(csv_filename) #writes to csv
    print('Written to CSV file')

def generate_charts(csvfile,PriceHisto,ReleaseWeek):
    csv_dataframe = pd.read_csv(csvfile,header=0,index_col=False,usecols=['Title of Game','Release Date','Current Price','Original Price','Is Discounted','Discount Percentage','Link To Game'])
    daytitle = csvfile.split('.')[0]
    sns.set(style='darkgrid',font_scale=1,)
    file_date = date( int(daytitle.split(' ')[5] .split('-')[0]) , int(daytitle.split(' ')[5] .split('-')[1]) , int(daytitle.split(' ')[5] .split('-')[2]) ) #shit ass mess

    def last_day_of_month(any_day): #taken from stack overflow
        next_month = any_day.replace(day=28) + timedelta(days=4)  # this will never fail because the resulting date will always land in the next month(i think)
        return ( next_month - timedelta(days=next_month.day) ) .day

    def previous_month(input_date): #adapted from stack overflow as well. Gets the previous month
        last_month = input_date.replace(day=1) - timedelta(days=1)
        return last_month.month

    dates_bin = []
    ########is this even used anymore?????
    for x in range( (file_date.day - 7), (file_date.day + 1) ):
        if x <= 0:
            print('NEGATIVE, ROLL BACK TO PREVIOUS MONTH')
            get_day_of_date = (last_day_of_month( date(file_date.year, previous_month(file_date), 1) ) - abs(x))
            reordered_date = " ".join( (date(file_date.year, previous_month(file_date), 1 ).strftime("%b") , get_day_of_date, file_date.year) )
        else:
            reordered_date = " ".join( ( (file_date.strftime("%b")), str(x) , str(file_date.year) ) )
        
        dates_bin.append( reordered_date )
        print(reordered_date)
    #print(dates_bin)

    plt.figure()
    #barplottest = sns.barplot(x='Release Date',y='Title of Game',data=csv_dataframe,)
    #sns.catplot(x='Release Date',y='Title of Game',kind='bar',data=csv_dataframe)
    sns.countplot(x='Release Date',data=csv_dataframe,order=dates_bin)
    plt.show()

game_list = []
name_csv_string = 'List of New Games Released ' + str(date.today()) + '.csv'
url_filter = 'https://store.steampowered.com/search/?sort_by=Released_DESC&untags=493&category1=998&unvrsupport=401&supportedlang=english&page='
pages_to_search = 7 #default is 7 

#read_html(filename=name_csv_string,base_url=url_filter,numofpages=pages_to_search)
#generate_panda_dataframe(game_list,name_csv_string)

generate_charts(name_csv_string,False,False)