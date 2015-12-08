#!/usr/bin/python
import sys
import os
import json
import Adafruit_DHT


# Parse command line parameters.
sensor_args = { '11': Adafruit_DHT.DHT11,
        '22': Adafruit_DHT.DHT22,
        '2302': Adafruit_DHT.AM2302 }
if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
  sensor = sensor_args[sys.argv[1]]
  pin = sys.argv[2]
else:
  print 'usage: sudo ./Adafruit_DHT.py [11|22|2302] GPIOpin#'
  print 'example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO #4'
  sys.exit(1)

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

# Un-comment the line below to convert the temperature to Fahrenheit.
# temperature = temperature * 9/5.0 + 32

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!

currentFilepath = os.path.dirname(os.path.realpath(__file__));

with open(currentFilepath + '/../package.json') as data_file:
  pkgdata = json.load(data_file)
  filePath = currentFilepath + '/..' + pkgdata['publicPath'] + '/' + 'meta.json';

if humidity is not None and temperature is not None:
  with open(filePath, 'w') as outfile:

    humidity = '{0:0.1f}'.format(humidity)
    temperature = '{0:0.1f}'.format(temperature)

    print 'Temp={0}*  Humidity={1}%'.format(temperature, humidity)


    data = {
      'temperature' : temperature,
      'humidity': humidity
    }

    json.dump(data, outfile)
else:
  print 'Failed to get reading. Try again!'
  sys.exit(1)
