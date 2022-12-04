# raspberry_car

Modern car sensor suite with automatic database sync

Sensors:

  - Camera (resolution ???)

  - GPS / gyroscope

  - Car ODB port


Raspberry pi installation:

  - sudo apt-get install libatlas-base-dev

  - sudo apt install gpsd

  - sudo service gpsd start

  - pip install --requirement requirements.txt



make non poetry requirements file for raspberry pi

  poetry export --without-hashes > requirements.txt

  pip install --requirement requirements.txt
