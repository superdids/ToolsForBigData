import time

from mrjob.job import MRJob
import json

from mrjob.step import MRStep

LAT_MAX = 'lat_max'
LNG_MAX = 'lng_max'
LAT_MIN = 'lat_min'
LNG_MIN = 'lng_min'

def location_hashing(entry):
    return entry[27], entry[28]

class MrMinMaxLatLng(MRJob):
    def steps(self):
        return [
            MRStep(mapper=self.passLocations,
               reducer=self.yieldGreatest)
        ]

    # Generates a (k,v) pair for each occurrence of a word
    # in a text file.
    def passLocations(self, _, line):
        lineJSON = json.loads(line)

        lat, lng = location_hashing(lineJSON)
        if type(lat) != type(None):
            yield LAT_MAX, float(lat)
            yield LAT_MIN, float(lat)

        if type(lng) != type(None):
            yield LNG_MAX, float(lng)
            yield LNG_MIN, float(lng)

    # The reduction step now performs the sum function on the values list,
    # and returns a single value as result.
    def yieldGreatest(self, key, values):
        if key == LAT_MAX:
            yield LAT_MAX, max(values)
        elif key == LNG_MAX:
            yield LNG_MAX, max(values)
        elif key == LAT_MIN:
            yield LAT_MIN, min(values)
        else:
            yield LNG_MIN, min(values)


if __name__ == '__main__':
    start = time.time()
    MrMinMaxLatLng.run()
    end = time.time()
    print('Execution time: ', (end-start))