from flask import Flask, jsonify
import mysql.connector
import yfinance as yf
from datetime import datetime, date, timedelta
import threading
import time as T
import os

app = Flask(__name__)

# Environment variables for database connection
for name, value in os.environ.items():
    print("{0}: {1}".format(name, value))
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "mypassword")
DB_PORT = os.getenv("DB_PORT", "3307")
FETCH_INTERVAL_SECONDS = int(os.getenv("FETCH_INTERVAL_SECONDS", "40"))
for name, value in os.environ.items():
    print("{0}: {1}".format(name, value))
def db_connect():
    return mysql.connector.connect(
        host = DB_HOST,
        user = DB_USER,
        password = DB_PASS,
        port = int(DB_PORT)
    )

def fetch_and_store_stock_data():
    with db_connect() as db:
        with db.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS Stockdb")
            cursor.execute("USE Stockdb")

            # deleting table so previous/old data is deleted
            cursor.execute("DROP TABLE IF EXISTS stockPrediction_onedaystock")
            cursor.execute("DROP TABLE IF EXISTS stockPrediction_oneyearstock")
            cursor.execute("DROP TABLE IF EXISTS stockPrediction_company")

            # creating new tables so only new data is added
            cursor.execute("CREATE TABLE IF NOT EXISTS stockPrediction_company(id MEDIUMINT NOT NULL AUTO_INCREMENT,name VARCHAR(10) NOT NULL, PRIMARY KEY(id))")
            cursor.execute("CREATE TABLE IF NOT EXISTS stockPrediction_oneyearstock(id MEDIUMINT NOT NULL AUTO_INCREMENT, name VARCHAR(10) NOT NULL, time DATE NOT NULL, open DOUBLE NOT NULL, close DOUBLE NOT NULL, high DOUBLE NOT NULL, low DOUBLE NOT NULL, volume DOUBLE NOT NULL, PRIMARY KEY(id))")
            cursor.execute("CREATE TABLE IF NOT EXISTS stockPrediction_onedaystock(id MEDIUMINT NOT NULL AUTO_INCREMENT, name VARCHAR(10) NOT NULL, time DATETIME NOT NULL, price DOUBLE NOT NULL, volume DOUBLE NOT NULL, PRIMARY KEY(id))")

            # List of company names
            company_name = ["AAPL", "MSFT", "TSLA", "AMZN", "GOOGL", "SPY", "BRK-B", "JNJ", "V", "PG"]

            # Iterate over company names to insert them into the company table
            for name in company_name:
                cursor.execute(f"SELECT * FROM stockPrediction_company WHERE name = '{name}'")
                result = cursor.fetchone()

                if not result:
                    try:
                        cursor.execute(f"INSERT INTO stockPrediction_company(name) VALUES('{name}')")
                        db.commit()
                    except:
                        db.rollback()

            # Loop to fetch data and insert into tables
            max_it = 1
            current_it = 0

            while current_it <= max_it:
                print("Thread executing")
                # Fetch one year stock data
                print("One year & one day stock")
                today = date.today()
                interval = timedelta(days=365)
                oneYearBefore = today - interval

                # Insert one day stock data
                now = datetime.now()
                for name in company_name:
                    stock = yf.Ticker(name)
                    result = stock.history(period='1d')

                    if not result.empty:
                        price = result['Close'].iloc[0]
                        volume = result['Volume'].iloc[0]
                        sql = f"INSERT INTO stockPrediction_onedaystock(name, time, price, volume) VALUES('{name}', '{now}', {price}, {volume})"
                        try:
                            cursor.execute(sql)
                            db.commit()
                        except:
                            print('Error on inserting one day stock data')
                            db.rollback()
                    else:
                        print(f"No data found for {name}, skipping one day stock data...")


                # Wait for  seconds before next iteration
                T.sleep(FETCH_INTERVAL_SECONDS)
                current_it += 1

            # Close database connection
            db.close()

@app.route('/start_fetching', methods=['POST'])
def start_fetching():
    threading.Thread(target=fetch_and_store_stock_data).start()
    return jsonify({'message': 'Stock data fetching started'}), 202

@app.route('/all_stock_data', methods=['GET'])
def get_all_stock_data():
    data = []
    try:
        db = db_connect()
        print("DB Connected")
        cursor = db.cursor(dictionary=True)
        fetch_and_store_stock_data()
        cursor.execute("USE Stockdb")

        print("Query Executed")

        query = "SELECT * FROM stockPrediction_onedaystock ORDER BY time DESC"
        cursor.execute(query)

        print("Query Executed")

        rows = cursor.fetchall()

        # Manually convert datetime objects to string in each row
        for row in rows:
            for key, value in row.items():
                if isinstance(value, datetime):
                    row[key] = value.isoformat()
            data.append(row)
        print("Data added")

        cursor.close()
        db.close()
    except mysql.connector.Error as error:
        print(f"Failed to retrieve data from MySQL table: {error}")
        return jsonify({'error': 'Database error'}), 500

    if data:
        return jsonify(data), 200
    else:
        return jsonify({'message': 'No data found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)

