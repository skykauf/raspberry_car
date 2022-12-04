import requests
import os
from PIL import Image
from io import BytesIO

from credentials import openstreetmap_apikey


datadir = 'data/'

def write_gps_route_to_image(lats: list[float], longs: list[float], script_start_datedir: str, script_start_datetime: str, resolution: tuple[int]):
    # may want to reduce number of coordinates sent in map-query
    map_params = {"key": openstreetmap_apikey, "bestfit": ",".join([str(min(lats)-.01), str(min(longs)-.01), str(max(lats)+.01), str(max(longs)+.01)]), "size": ", ".join(resolution), "shape": ",".join([f'{lats[i]},{longs[i]}' for i in range(len(lats))])}

    mapimage = requests.get("http://www.mapquestapi.com/staticmap/v4/getmap", params=map_params)
    if mapimage.status_code == 200:
        print("Successfully retrieved image")
    else:
        print("Couldn't retrieve image")
        print(mapimage.text)
    i = Image.open(BytesIO(mapimage.content))
    i.save(os.path.join(script_start_datedir, f"ROUTEMAP_{script_start_datetime}.jpg"))
    print("saved image to", script_start_datedir)
    print("SHOWN")