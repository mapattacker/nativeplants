import sqlite3, time, urllib


######################ENTER VARIABLES################################
sqlitePath = 'grin.sqlite'  #path to sqlite database

######################ENTER VARIABLES################################

#Connect and fetch species list
conn = sqlite3.connect(sqlitePath)
cur = conn.cursor()
cur.execute('SELECT speciesName, id FROM species WHERE speciesName = ? AND hyperlink is NULL',(raw_input('Input Species Name:'),))
spList = cur.fetchall()

#Fetch flora distribution lists for each level
cur.execute('SELECT L1continent, id FROM tblLevel1') #get level 1 list
L1List = cur.fetchall()
cur.execute('SELECT L2region, id FROM tblLevel2') #get level 2 list
L2List = cur.fetchall()
cur.execute('SELECT L3area, id, synonym FROM tblLevel3') #get level 3 list
L3List = cur.fetchall()
cur.execute('SELECT L4country, id, synonym FROM tblLevel4') #get level 4 list
L4List = cur.fetchall()

link = raw_input('Paste GRIN species url: ')
html = urllib.urlopen(link).read()

x=0
for row in spList:
    species = row[0]
    sp_id = row[1]
    x+=1
    print x, species

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
            region = native3.find(row[0]) + native3.find(row[2])    #look for synonym too
            if region > 1:
                cur.execute('INSERT INTO nativeto(sp_id, to_id, lvl_id) VALUES (?, ?, ? )', (sp_id, row[1], 3))

    #scrape based on level 4 region
    for row in L4List:
        if native <1:
            break
        else:
            region = native3.find(row[0]) + native3.find(row[2])    #look for synonym too
            if region > 1:
                cur.execute('INSERT INTO nativeto(sp_id, to_id, lvl_id) VALUES (?, ?, ? )', (sp_id, row[1], 4))

    cur.execute('UPDATE species SET scanned = ? WHERE speciesNAME = ?',('Y', species))
    conn.commit()
