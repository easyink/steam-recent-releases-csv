# steam-store-search-to-csv
This is a python script generates a csv of games given a steam store search url using the Requests python library and BeautifulSoup library. It can also generate charts with that created csv using Seaborn. 

WHY? I wanted to easily see what games were being released and the Steam API doesn't easily support the ability to generate a list of recently released games on steam. So my solution was to extract the information from the literal steam search page. 

However, this script can support any steam search url with whatever chosen filters applied, as long as you replace the url_filter variable.

The uploaded script will filter out games listed without a price, if it is Free, or Free to Play, doesn't support english, VR games, and early access titles.

It downloads the literal url via Requests and crawls the html using BeautifulSoup. It iterates through a chosen number of pages since the infinite scrolling of the page is not possible with requests.

Seaborn is used in the generate_charts function and reads the csv and will generate a price histogram of all the games released in the past week, and layer another histogram showing how many games are discounted as well.
It can also generate another histogram showing how many games are rleased per day in the past week.
