# raspberry_car

Modern car sensor suite with automatic database sync

Sensors:

  - Camera (resolution ???)

  - GPS / gyroscope

  - Car ODB port

TODO rest


make non poetry requirements file for raspberry pi

  pi needs this install for opencv to work:

    sudo apt-get install libatlas-base-dev


  poetry export --without-hashes > requirements.txt

  pip install --requirement requirements.txt
