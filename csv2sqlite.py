import sqlite3, csv

con = sqlite3.connect("recallInfo.db")
cur = con.cursor()
cur.execute("CREATE TABLE recallInfoTemp (code varchar(15), issueDate INTEGER, brandName text,"
            " companyName text, productDescription text, recallReason text, url text)")

with open('latest.csv','r') as new_table:
    dr = csv.DictReader(new_table) # comma is default delimiter
    to_db = [(i['code'], i['issueDate'], i['sex'], i['brandName'], i['companyName'], i['productDescription'],
              i['recallReason'], i['url']) for i in dr]

cur.executemany("INSERT INTO recallInfoTemp VALUES (?,?,?,?,?,?,?);", to_db)
con.commit()

cur.execute("INSERT INTO recallInfo (code, issueDate, brandName, companyName, productDescription"
            ",recallReason, url) SELECT * from recallInfoTemp")

cur.execute("DROP TABLE recallInfoTemp")