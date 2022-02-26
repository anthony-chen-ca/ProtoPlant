import json

from flask import Flask, request
from flask import render_template
import sqlite3



def create_table():
    conn = sqlite3.connect('database.db')
    conn.execute('CREATE TABLE IF NOT EXISTS plants (id INTEGER PRIMARY KEY AUTOINCREMENT, temp REAL, light REAL, humid REAL, moist REAL)')
    conn.close()

def create_entry(temp, light, humid, moist):
    conn = sqlite3.connect('database.db')
    query = 'INSERT INTO plants (temp, light, humid, moist) VALUES ({temp}, {light}, {humid}, {moist})'.format(
        temp=temp,
        light=light,
        humid=humid,
        moist=moist
    )
    conn.execute(query)
    conn.commit()
    conn.close()

app = Flask(__name__)

def final_plant():
    conn = sqlite3.connect('database.db')
    query = 'SELECT * FROM plants ORDER BY id DESC LIMIT 1;'
    result = conn.execute(query).fetchall()
    conn.commit()
    conn.close()
    return result

@app.route("/")
def index():
    # Fetch data from
    plant = final_plant()[0]
    print(plant)
    data = {
        'temp': plant[1],
        'light': plant[2],
        'humid': plant[3],
        'moist': plant[4]
    }

    return render_template('ProtoPlant.html', **data)

@app.route('/update_plant', methods=['POST'])
def upate_plant_data():
    data = request.json
    create_entry(
        temp=data['temp'],
        light=data['light'],
        humid=data['humid'],
        moist=data['moist']
    )
    return 'radicals'


if __name__ == '__main__':
    app.run()