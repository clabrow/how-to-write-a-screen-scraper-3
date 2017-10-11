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
    rows = root.cssselect("tr")  # selects all <tr> blocks
    for row in rows:
        # Set up our data record - we'll need it later
        record = {}
        table_cells = row.cssselect("td") # extract cell in the table as you loop through it
        if table_cells: # if there are any cells
            record['Racecourse'] = table_cells[0].text_content() # put the text between each tag in a variable called record, unique key is artist
            record['Address and Phone Number'] = table_cells[1].text_content()
            # Print out the data we've gathered
            print record, '------------'
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.sqlite.save(["Racecourse"], record)
        
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
   

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then 
# call a function to scrape it
# ---------------------------------------------------------------------------
starting_url = 'http://www.ukjockey.com/racecourses.html'
# urlparse breaks up the url by /. urlparse.urljoin combines two urls together.
scrape_and_look_for_next_link(starting_url)
