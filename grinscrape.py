import sqlite3, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


######################ENTER VARIABLES################################
sqlitePath = 'grin.sqlite'  #path to sqlite database
chromeDriver = r'C:\Users\XXX\Scripts\chromedriver.exe' #path to chromedriver.exe

######################ENTER VARIABLES################################

#Connect and fetch species list
conn = sqlite3.connect(sqlitePath)
cur = conn.cursor()
cur.execute('SELECT speciesName, id FROM species WHERE scanned IS NULL')
spList = cur.fetchall()

#Fetch flora distribution lists for each level
cur.execute('SELECT L1continent, id FROM tblLevel1') #get level 1 list
L1List = cur.fetchall()
cur.execute('SELECT L2region, id FROM tblLevel2') #get level 2 list
L2List = cur.fetchall()
cur.execute('SELECT L3area, id FROM tblLevel3') #get level 3 list
L3List = cur.fetchall()
cur.execute('SELECT L4country, id FROM tblLevel4') #get level 4 list
L4List = cur.fetchall()

#Connect to chrome browser
browser = webdriver.Chrome(chromeDriver)

#for each species, look into GRIN website of the species and mark if the native regions are present
x=0
for row in spList:
    species = row[0]
    sp_id = row[1]
    x+=1
    print x, species

    browser.get(r'https://npgsweb.ars-grin.gov/gringlobal/taxon/taxonomysimple.aspx')
    elem = browser.find_element_by_name('ctl00$cphBody$txtSearch')  #find search box
    elem.send_keys(species)  #input species
    elem.send_keys(Keys.RETURN) #start search
    time.sleep(5)   #delay for search to process

    html = browser.page_source  #grab entire html
    link = browser.current_url  #grab hyperlink

    #filter html to only include native region
    native = html.find('Native:')   #find index number of the header which gives the native distribution
    native2 = html[native:]         #filter to include all text from native header to end of page
    native3 = native2[:native2.find('<h1>')]    #filter to include text only within native distribution

    #scrape based on level 1 region
    if native > 1:
        cur.execute('UPDATE species SET hyperlink = ? WHERE speciesNAME = ?',(link, species))

    for row in L1List:
        if native <1:
            break
        else:
            region = native3.find(row[0])
            if region > 1:
                cur.execute('INSERT INTO nativeto(sp_id, to_id, lvl_id) VALUES (?, ?, ? )', (sp_id, row[1], 1))

    #scrape based on level 2 region
    for row in L2List:
        if native <1:
            break
        else:
            region = native3.find(row[0])
            if region > 1:
                cur.execute('INSERT INTO nativeto(sp_id, to_id, lvl_id) VALUES (?, ?, ? )', (sp_id, row[1], 2))

    #scrape based on level 3 region
    for row in L3List:
        if native <1:
            break
        else:
            region = native3.find(row[0]) + native3.find(row[2]) #look for synonym too
            if region > 1:
                cur.execute('INSERT INTO nativeto(sp_id, to_id, lvl_id) VALUES (?, ?, ? )', (sp_id, row[1], 3))

    #scrape based on level 4 region
    for row in L4List:
        if native <1:
            break
        else:
            region = native3.find(row[0]) + native3.find(row[2]) #look for synonym too
            if region > 1:
                cur.execute('INSERT INTO nativeto(sp_id, to_id, lvl_id) VALUES (?, ?, ? )', (sp_id, row[1], 4))

    cur.execute('UPDATE species SET scanned = ? WHERE speciesNAME = ?',('Y', species))
    conn.commit()
