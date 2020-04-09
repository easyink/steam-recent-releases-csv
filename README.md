# steam-store-search-to-csv
This is a python script generates a csv of games given a steam store search url using the Requests python library and BeautifulSoup library.

WHY? Because the Steam API doesn't support the ability to generate a list of recently released games on steam. My solution was to extract the information from their steam search page. 
However, this script can support any steam search url with whatever chosen filters applied, as long as you replace the url variable.

The uploaded script will filter out games listed without a price, or if it is Free, or Free to Play.

if it repeatedly prints pages and pages of the same page, it might be because of cookies in the browser, idk. it bugged out on me for a moment while testing it and then it went away.

It downloads the literal url via Requests and crawls the html using BeautifulSoup. It iterates through a chosen number of pages since the infinite scrolling of the page is not possible with requests.
