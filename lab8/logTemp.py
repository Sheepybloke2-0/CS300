# Log temperature every 10 seconds
import Adafruit_MCP9808.MCP9808 as MCP9808
import sqlite3
import time
FILENAME = 'temperature.db'
TABLE = 'TemperatureData'
# Create temperature sensor object
sensor = MCP9808.MCP9808()
# Connect to the database
db = sqlite3.connect(FILENAME)
c = db.cursor()
# Continuously take temperature samples till ctrl-C is hit
try:
     while True:
        # Read MCP9808 sensor
        temp = sensor.readTempC()
        print("Temperature:", temp,"degrees C")
        # Insert data into database
        sqlcmd = "INSERT INTO "+TABLE+" VALUES (datetime('now','localtime'),"+str(temp)+")"
        c.execute(sqlcmd)
         # Keep only the last hour of readings
        sqlcmd = "DELETE FROM "+TABLE+" WHERE datetime < datetime('now','localtime','-1 hour')"
        c.execute(sqlcmd)
        db.commit()
        time.sleep(10)
except KeyboardInterrupt:
     print('Done')
     db.close()
