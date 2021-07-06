import json

from flask import Flask, jsonify, render_template
import paho.mqtt.client as mqtt

import sqlite

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("temperatures.html")


@app.route('/salles')
def get_salles():
    return jsonify(list(sqlite.get_salles()))


@app.route('/salles/<int:numero>')
def get_salle_by_numero(numero):
    return jsonify(sqlite.get_salle_by_numero(numero))


if __name__ == '__main__':
    app.run()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("salles")


def on_message(client, userdata, msg):
    if msg.topic == "salles":
        print(msg.payload)
        salle = json.loads(msg.payload)
        sqlite.add_salle(salle)


sqlite.init()
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.42", 1883, 60)
client.loop_start()
