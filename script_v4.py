from bs4 import BeautifulSoup
import requests
import csv
from datetime import date,timedelta
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

namecsv = 'List of New Games Released ' + str(date.today()) + '.csv'
url_filter = 'https://store.steampowered.com/search/?sort_by=Released_DESC&untags=493&category1=998&unvrsupport=401&supportedlang=english&page='
pages_to_search = 2

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
                release_date = (i.find('div', class_='col search_released responsive_secondrow').get_text()).replace(',','')
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

def generate_charts(filename,PriceHisto,ReleaseWeek): #chart function
    with open(filename, encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader) #skips the header row
        readfile = list(reader) #crucial to make the csv readable in loops more than once
        daytitle = filename.split('.')[0] + ' over the last week'
        sns.set(style='darkgrid',font_scale=1,) #global chart settings

        file_date = date( int(daytitle.split(' ')[5] .split('-')[0]) , int(daytitle.split(' ')[5] .split('-')[1]) , int(daytitle.split(' ')[5] .split('-')[2]) ) #shit ass mess

        current_price = []
        discounted = []
        dollar_bins = [0,5,10,15,20,30,40,50,60]

        def last_day_of_month(any_day): #taken from stack overflow
            next_month = any_day.replace(day=28) + timedelta(days=4)  # this will never fail because the resulting date will always land in the next month(i think)

            return ( next_month - timedelta(days=next_month.day) ) .day

        def previous_month(input_date): #adapted from stack overflow as well. Gets the previous month
            last_month = input_date.replace(day=1) - timedelta(days=1)
            return last_month.month

        dates = []
        dates_bin = []

        for x in range( (file_date.day - 7), (file_date.day + 1) ):
            if x <= 0:
                print('NEGATIVE, ROLL BACK TO PREVIOUS MONTH')
                dates_bin.append( last_day_of_month( date(file_date.year, previous_month(file_date), 1) ) - abs(x) )
            else:
                dates_bin.append(x)
        print(dates_bin)
        
        for row in readfile: #iterator for lists 
            if int(row[1].split(' ')[1]) >= (dates_bin[0]):
                if PriceHisto == True:
                    dollar_figure = float(row[2].strip('$')) #gets the dollar values
                    current_price.append(dollar_figure) #puts it in the current_price list
                    if row[4] == 'True': #if flagged as discounted, also puts it into the discount list
                        discounted.append(dollar_figure)
                if ReleaseWeek == True:
                    dates.append(int(row[1].split(' ')[1]))
        
        plt.figure()
        #barplottest = sns.barplot(x='Release Date',data=dates,order=dates_bin)
        #this is some debug shit idk

        if PriceHisto == True:

            plt.figure()
            price_histogram = sns.distplot(current_price,bins=dollar_bins,kde=False,hist=True,color='blue',label='Games')
            price_histogram.set(xlim=0,xlabel='Price in $USD',ylabel='Number of Games',title=daytitle)
            discount_histogram = sns.distplot(discounted,bins=dollar_bins,kde=False,color='green',label='Discounted Games',hist_kws=dict(alpha=1))
            create_text_over_bars(price_histogram,True,1,True,False)
            plt.legend()

        if ReleaseWeek == True:

            plt.figure()
            days_barchart = sns.distplot(dates,bins=dates_bin,kde=False,hist_kws=dict(width=1),color='orange')
            days_barchart.set(xlim=(dates_bin[0],dates_bin[-1]),xlabel='Current Week',title=daytitle )
            create_text_over_bars(days_barchart,False,0.5,True,False)
            #create_text_over_bars(days_barchart, False, 0 , False, True)
            plt.legend()

        plt.show()
        print('Generated Charts')

def create_text_over_bars(distplot,layeredbool,yoffsetdist,print_height_text,print_day_text):
    patches = distplot.patches
    days_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    for index, item in enumerate(patches):
        centerpos = item.get_x()+item.get_width()/2
        height = item.get_height()

        if print_height_text == True:
            if height == 0:
                continue
            if layeredbool is True:
                if index <= 7:
                    distplot.text(x=centerpos,y=height+yoffsetdist,s=int(height),ha='left')
                else:
                    distplot.text(x=centerpos,y=height+yoffsetdist,s=int(height),ha='right')
            else:
                distplot.text(x=centerpos,y=height+yoffsetdist,s=int(height),ha='center')
        elif print_day_text == True:
            format_day = int( item.get_x() )
            
            day_of_week =days_list
            [ 
                date( 
                    date.today().year , 
                    date.today().month , 
                    format_day
                    )
                    .weekday()
            ]
            distplot.text(x=centerpos,y=0,s=day_of_week,ha='center',fontsize='small')
            

generate_csv(namecsv,url_filter,pages_to_search)
generate_charts(namecsv,PriceHisto=True,ReleaseWeek=True)