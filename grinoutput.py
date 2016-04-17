import sqlite3

######################ENTER VARIABLES################################
sqlitePath = 'grin.sqlite'  #path to sqlite database
csv = 'C:\Users\Siyang\Desktop\lflower.csv'    #path to output
######################ENTER VARIABLES################################

csv2 = open(csv, 'w')
csv2.write('region,count,level\n')  #input headers
conn = sqlite3.connect(sqlitePath)
cur = conn.cursor()

####################find count for each region in each hierarchical level
###level 1
cur.execute("""SELECT L1continent, count(speciesName) AS sum FROM nativeto n
                JOIN  tblLevel1 L1 ON n.to_id = L1.id
                JOIN species sp ON n.sp_id = sp.id
                WHERE n.lvl_id = 1
                GROUP BY L1continent""")

print '\nLEVEL 1'
for row in cur:
    print '{},{}'.format(row[0],row[1])
    csv2.write('{},{},1\n'.format(row[0],row[1]))

###level 2
cur.execute("""SELECT L2region, count(speciesName) AS sum FROM nativeto n
                JOIN  tblLevel2 L2 ON n.to_id = L2.id
                JOIN species sp ON n.sp_id = sp.id
                WHERE n.lvl_id = 2
                GROUP BY L2region""")

print '\nLEVEL 2'
for row in cur:
    print '{},{}'.format(row[0],row[1])
    csv2.write('{},{},2\n'.format(row[0],row[1]))

###level 3
cur.execute("""SELECT L3area, count(speciesName) AS sum FROM nativeto n
                JOIN  tblLevel3 L3 ON n.to_id = L3.id
                JOIN species sp ON n.sp_id = sp.id
                WHERE n.lvl_id = 3
                GROUP BY L3area""")

print '\nLEVEL 3'
for row in cur:
    print '{},{}'.format(row[0],row[1])
    csv2.write('{},{},3\n'.format(row[0],row[1]))

#GRIN does not put in some regions of level 3 for China
#hence a separate join calculation have to be made from level 4 to level 3
cur.execute("""SELECT L3area, count(speciesName) AS sum FROM nativeto n
                JOIN  tblLevel4 L4 ON n.to_id = L4.id
                JOIN species sp ON n.sp_id = sp.id
				JOIN tblLevel3 L3 ON L4.L3code = L3.L3code
                WHERE n.lvl_id = 4 and L3area LIKE '%china%'
                GROUP BY L3area
				ORDER BY L3area""")
for row in cur:
    print '{},{}'.format(row[0],row[1])
    csv2.write('{},{},3\n'.format(row[0],row[1]))

###level 4
cur.execute("""SELECT L4country, count(speciesName) AS sum FROM nativeto n
                JOIN  tblLevel4 L4 ON n.to_id = L4.id
                JOIN species sp ON n.sp_id = sp.id
                WHERE n.lvl_id = 4
                GROUP BY L4country""")

print '\nLEVEL 4'
for row in cur:
    print '{},{}'.format(row[0].encode('utf'),row[1])
    csv2.write('{},{},4\n'.format(row[0],row[1]))
