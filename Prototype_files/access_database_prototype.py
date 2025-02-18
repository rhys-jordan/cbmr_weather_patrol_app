import sqlalchemy
from sqlalchemy import create_engine, MetaData, text, Column, Integer, DateTime, String, Float

import sqlite3

connection = sqlite3.connect("..\\CBMR_Weather\\instance\\CBMR_Weather.db")
cursor = connection.cursor()



#"C:\Users\rhysj\OneDrive\Desktop\cbmr_weather_patrol_app\CBMR_Weather\instance\CBMR_Weather.db"

def main():

    command = 'SELECT date FROM snow '
    #print(division.columns.keys())
    #query = division.select()  # SELECT * FROM divisions
    #print(query)
    cursor.execute(command)
    results = cursor.fetchall()
    print(results)
    connection.close()





if __name__ == "__main__":
    main()