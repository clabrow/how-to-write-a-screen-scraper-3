###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next' 
# links from page to page: use functions, so you can call the same code 
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
import urlparse
import lxml.html

# scrape_table function: gets passed an individual page to scrape
def scrape_table(root): # root variable defined in scrape_and_look_for_next_link: parses xml from url
    rows = root.cssselect("table.data tr")  # selects all <tr> blocks within <table class="data">
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.cssselect("td") # extract cell in the table as you loop through it
        if table_cells: # if there are any cells
            record['Artist'] = table_cells[0].text # put the text between each tag in a variable called record, unique key is artist
            record['Album'] = table_cells[1].text
            record['Released'] = table_cells[2].text
            record['Sales m'] = table_cells[4].text
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.sqlite.save(["Artist"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    # scrape that url
    html = scraperwiki.scrape(url)
    # print out the contents
    print html
    # parses the xml from the url into an element?
    root = lxml.html.fromstring(html)
    # scrape the table and store it in data record set up in previous function
    scrape_table(root)
    # ? Is "a.next" a string from the table?
    next_link = root.cssselect("a.next")
    print next_link
    if next_link:
        # gets the contents of the attribute href 
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        # I guess this moves on to the next link in the url and keeps going until it doesn't find any more
        scrape_and_look_for_next_link(next_url)

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'https://paulbradshaw.github.io/'
starting_url = urlparse.urljoin(base_url, 'scraping-for-everyone/webpages/example_table_1.html')
scrape_and_look_for_next_link(starting_url)
