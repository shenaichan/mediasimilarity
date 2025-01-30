from selenium import webdriver
from selenium.webdriver.common.by import By

# set up web driver
driver = webdriver.Firefox()


numTropePages = 61
# 500 tropes per page.......
tropeIndexBaseUrl = "https://tvtropes.org/pmwiki/pagelist_having_pagetype_in_namespace.php?n=Main&t=trope&page="


def getLinks(pageNum: int):
    driver.get(tropeIndexBaseUrl+str(pageNum))
    # links = driver.find_elements(By.PARTIAL_LINK_TEXT, '/pmwiki/pmwiki.php/')
    tableEntries = driver.find_elements(By.TAG_NAME, 'td')
    tropes = []
    for entry in tableEntries:
        link = entry.find_element(By.XPATH, "./*")
        tropes.append(link.text.strip())
    return tropes


# for i in range(1, numTropePages+1):
#     getMediaFromTropePage(i)

print(getLinks(30))

driver.quit()

'''
go to tvtropes
go through all 61 of these
https://tvtropes.org/pmwiki/pagelist_having_pagetype_in_namespace.php?n=Main&t=trope&page=1

grab each link

go into page, first try to open all folders --> don't have to bc the text is already loaded onto the page lol
get each HTML <a> element and check if the link doesn't involve /Main/ (i.e. it's a media)
also check if links involve the link itself, then it's a subpage, and repeat the process here
get the URL, check if it's in the DB already, and if not, add to the DB
once you've made a list of all media, go to each page and get the actual name
'''
