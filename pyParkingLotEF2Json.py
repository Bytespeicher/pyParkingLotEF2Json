#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import json
import re
import datetime
import config

static_data = {}
# Anger 1
static_data["Anger 1"] = {'latitude': "50.9779121",
                          'longitude': "11.0370504",
                          'adresse': "Fleischgasse 2, 99084 Erfurt"}
# Thomaseck
static_data["Thomaseck"] = {'latitude': "50.9725714",
                            'longitude': "11.0338341",
                            'adresse': "Thomasstraße, 99084 Erfurt"}
# Forum 1
static_data["Forum 1"] = {'latitude': "50.9734289",
                          'longitude': "11.0330801",
                          'adresse': "Forum 1, Lachsgasse"}
# Forum 2+3
static_data["Forum 2+3"] = {'latitude': "50.9744646",
                            'longitude': "11.0330455",
                            'adresse': "Hirschlachufer 7, 99084 Erfurt"}
# Thüringenhaus
static_data["Th\xfcringenhaus"] = {
    'latitude': "50.9843184", 'longitude': "11.0311626",
    'adresse': "Wallstraße, 99084 Erfurt"}
# Domplatz
static_data["Domplatz"] = {'latitude': "50.9782800",
                           'longitude': "11.0207300",
                           'adresse': "Bechtheimer Straße 1, 99084 Erfurt"}
# Hauptbahnhof
static_data["Hauptbahnhof"] = {'latitude': "50.9730880",
                               'longitude': "11.0376740",
                               'adresse': "Willy-Brandt-Platz 2, 99084 Erfurt"}
# Sparkassen-Finanzzentrum
static_data["Sparkassen-Finanzzentrum"] = {'latitude': "50.9708660",
                                           'longitude': "11.0186620",
                                           'adresse': "Bonifaciusstraße 15, 99084 Erfurt"}


class ParkingLotEF2Json():
    page = ""
    data = []

    def __init__(self):
        url = "http://stadtplan.erfurt.de/cgi-bin/grafik.plx?L=de&PS=24&T=600&MAP=aspf&Mode=0&ME=3&X=15&Y=15&OBJ="
        user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0'
        headers = {'User-Agent': user_agent}
        req = urllib2.Request(url, None, headers)
        response = urllib2.urlopen(req)
        self.page = response.read()

    def getJson(self):
        m = re.findall(r'Ob(.*von.*);', self.page)
        i = 0
        time = str(datetime.datetime.now())
        self.data.append({'date': time})

        for elem in m:
            name = re.search(r'"[ A-Za-zöüä\xfc0-9+-]+"', elem,
                             re.UNICODE).group(0)[1:-1]
            belegt = re.search(r'[\-0-9]+\)', elem).group(0)[0:-1]
            max = re.search(r'von.*,', elem).group(0)[5:-1]
            tmp = {'name': name, 'belegt': belegt, 'maximal': max}
            tmp.update(static_data.get(name))
            self.data.append(tmp)
            i = i + 1

        return json.dumps(self.data, ensure_ascii=False)

out = ParkingLotEF2Json().getJson()
fo = open(config.OUTPUT_FILE, "wb")
fo.write(out)
fo.close()
