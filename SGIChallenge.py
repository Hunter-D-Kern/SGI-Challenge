import pyodbc
from datetime import datetime

server = 'hunters-sgi-server.database.windows.net'
database = 'AdventureWorks2017'
username = 'guestuser'
password = 'SGI-Access'
driver= '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+password)
cursor = cnxn.cursor()


execute = True
while(execute):
    zipcode = input("Please input a zipcode:\n")
    zipcode = str(zipcode)

    startDate = input("Start of date range (YYYYMMDD):\n")

    if startDate < '20130731' or startDate > '20140803':
        startDate = input("All transactions are between 2013-07-31 and 2014-08-03, you should try a different date (YYYYMMDD)\n")

    startDate = str(datetime.strptime(startDate, '%Y%m%d').date())

    endDate = input("End of date range (YYYYMMDD):\n")
    if endDate < '20130731' or endDate > '20140803':
        endDate = input("All transactions are between 2013-07-31 and 2014-08-03, you should try a different date (YYYYMMDD)\n")
    elif endDate < startDate:
        input("Please choose a date later than the start date {}:\n".format(startDate))

    endDate = str(datetime.strptime(endDate, '%Y%m%d').date())

    QueryString = "SELECT A.PostalCode, AVG(P.ActualCost) AS 'Average Dollar per Transaction', " \
                         "COUNT(P.ActualCost) AS 'Number of Transactions', S.TerritoryID " \
                         "FROM Person.Address A, Sales.SalesOrderHeader S, Production.TransactionHistory P " \
                         " WHERE (A.PostalCode=('{}')AND (P.TransactionDate BETWEEN ('{}') AND ('{}')) " \
                         "AND A.AddressID=S.BillToAddressID AND S.SalesOrderID=P.ReferenceOrderID) " \
                         "GROUP BY A.PostalCode, S.TerritoryID".format(zipcode, startDate, endDate)

    cursor.execute(QueryString)
    row = cursor.fetchone()
    if row is None:
        print("No results found for zipcode {}.".format(zipcode))
        YN = input("Would you like to try again with a different zipcode? Y/N:\n")
        if YN.lower() == "n":
            execute = False
            break
        else:
            continue
    territoryID = row[3]
    resultString = "Average Dollars per Transactopm in Zipcode {}: {}" \
                   "\nRegion: {}".format(zipcode, row[1], row[3])
    print(resultString)

    RegionQuery = "SELECT AVG(S.TotalDue) FROM Sales.SalesOrderHeader S " \
                  "JOIN Production.TransactionHistory P ON S.SalesOrderID = P.ReferenceOrderID " \
                  "WHERE S.TerritoryID=({}) AND (P.TransactionDate BETWEEN ('{}') AND ('{}'))".format(territoryID, startDate, endDate)

    cursor.execute(RegionQuery)
    row = cursor.fetchone()
    regionString = "Average sales for Region {} : {}".format(territoryID, row[0])
    print(regionString)

# QueryString = "SELECT AVG(P.ActualCost) AS 'Average Dollar per Transaction' " \
#                      "FROM Production.TransactionHistory P " \
#                      "JOIN Sales.SalesOrderHeader S ON S.SalesOrderID = P.ReferenceOrderID " \
#                      "JOIN Person.Address A ON A.AddressID=S.ShipToAddressID " \
#                      "WHERE (A.PostalCode=('{}')AND (P.TransactionDate BETWEEN ('{}') AND ('{}')) ) ".format(zipcode, startDate, endDate)

# cursor.execute("SELECT TOP 20 pc.Name as CategoryName, p.name as ProductName FROM [SalesLT].[ProductCategory] pc JOIN [SalesLT].[Product] p ON pc.productcategoryid = p.productcategoryid")
# print(QueryString)
