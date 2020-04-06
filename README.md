# steam-recent-releases-csv
this is a python script generates a csv of recently released games on steam.

if it repeatedly prints pages and pages of the same page, it might be because of cookies in the browser, idk. it bugged out on me for a moment while testing it and then it went away.

Since the steam api doesn't have a direct command that lets me view their games by recent release, this relies on viewing the store search page by recently released, with the additional filters of Games Only, English Only, and No VR.

It downloads the literal url via Requests and crawls the html using BeautifulSoup. It iterates through multiple pages since the infinite scrolling of the page is not possible.
