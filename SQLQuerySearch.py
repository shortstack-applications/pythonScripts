#This script queries a SQL database for customer contact information
# then prints the data to a csv file.

import mysql.connector as mariadb
import CSVtoLDIFformat

#Try and connect to database
try:
  mydb = mariadb.connect(
  host="",
  database="",
  user="",
  passwd=""
  )
except mariadb.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
   mycursor = mydb.cursor()
    
   
   
#Execute query for Name, ID, Phone and MobPhone
#Current query pulls all customers who have had an account open within the years of 2018 and 2019
#There are two tables called 'customers' and 'accounts'. 
query = ("SELECT DISTINCT customers.name, customers.id, customers.phone, customers.mobile\
                 FROM accounts INNER JOIN customers ON accounts.customer = customers.id\
                 WHERE (((accounts.date) LIKE '%2018%') AND ((accounts.phone)<>'')\
                 OR (((accounts.date) LIKE '%2019%') AND ((customers.phone)<>'')))\
                 OR (((accounts.date) LIKE '%2018%') AND ((customers.mobile)<>''))\
                 OR (((accounts.date) LIKE '%2019%') AND ((customers.mobile)<>''))\
                 ORDER BY customers.name ASC;")

mycursor.execute(query)

#return results of query to queryResult         
queryResult = mycursor.fetchall()

#Open file and write results of query to it
csvFile = open("C:/example/of/file/path/documentName.csv", "r+")
for item in queryResult:
  for eachItem in item:
    csvFile.write(str(eachItem))
    csvFile.write(',')
  csvFile.write("\n")
  


#Close file and database cursor
mycursor.close()    
csvFile.close()

#Open the csvFile in read only and calls the parseFile function from CSVtoLDIFformat.py
csvFile = open("C:/example/of/file/path/documentName.csv".csv", "r")
CSVtoLDIFformat.parseFile(csvFile)
