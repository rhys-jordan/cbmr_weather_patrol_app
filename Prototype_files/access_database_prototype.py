

import sqlite3

connection = sqlite3.connect("..\\CBMR_Weather\\instance\\CBMR_Weather.db")
cursor = connection.cursor()




def main():

    command = 'SELECT date, forecaster FROM snow WHERE date = "2/18/2025" '
    #print(division.columns.keys())
    #query = division.select()  # SELECT * FROM divisions
    #print(query)
    cursor.execute(command)
    results = cursor.fetchall()
    print(results[0][1])
    connection.close()





if __name__ == "__main__":
    main()