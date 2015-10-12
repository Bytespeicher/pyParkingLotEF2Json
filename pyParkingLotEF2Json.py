#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import json
import re
import datetime

static_data = []
static_data.append({'latitude': "50.9725714", 'longitude': "11.0338341",
                    'adresse': "Thomasstraße, 99084 Erfurt"})
static_data.append({'latitude': "50.9843184", 'longitude': "11.0311626",
                    'adresse': "Wallstraße, 99084 Erfurt"})
static_data.append({'latitude': "50.97828", 'longitude': "11.02073",
                    'adresse': "Bechtheimer Straße 1, 99084 Erfurt"})
static_data.append({'latitude': "50.973088", 'longitude': "11.037674",
                    'adresse': "Willy-Brandt-Platz 2, 99084 Erfurt"})
static_data.append({'latitude': "50.9779121", 'longitude': "11.0370504",
                    'adresse': "Fleischgasse 2, 99084 Erfurt"})
static_data.append({'latitude': "50.9734289", 'longitude': "11.0330801",
                    'adresse': "Forum 1, Lachsgasse"})
static_data.append({'latitude': "50.9744646", 'longitude': "11.0330455",
                    'adresse': "Hirschlachufer 7, 99084 Erfurt"})
static_data.append({'latitude': "50.970866", 'longitude': "11.018662",
                    'adresse': "Bonifaciusstraße 15, 99084 Erfurt"})


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
            name = re.search(r'"[ A-Za-z0-9äöü+-]+"', elem,
                             re.UNICODE).group(0)[1:-1]
            belegt = re.search(r'[\-0-9]+\)', elem).group(0)[0:-1]
            max = re.search(r'von.*,', elem).group(0)[5:-1]
            tmp = {'name': name, 'belegt': belegt, 'maximal': max}
            tmp.update(static_data[i])
            self.data.append(tmp)
            i = i + 1

        return json.dumps(self.data, ensure_ascii=False)

out = ParkingLotEF2Json().getJson()

fo = open("data.json", "wb")
fo.write(out)
fo.close()
