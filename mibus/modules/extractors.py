from bs4.element import ProcessingInstruction


def extractLineRoute(kml_file):
    from bs4 import BeautifulSoup as bs
    almostList = []
    finalList = []
    cacheList = []
    counter = 0
    soup = bs(kml_file,'lxml')
    coordinates = soup.find("coordinates")
    for element in coordinates:
        elementList = element.split(",")
    for element in elementList:
        elementClean = element.split("-")
        try: 
            almostList.append(elementClean[1])
        except:
            pass
    for element in almostList:
        if counter == 0:            
            cacheList.append(float("-"+element))
            counter += 1
        elif counter == 1:
            cacheList.append(float("-"+element))
            finalList.append([cacheList[1], cacheList[0]])
            cacheList = []
            counter = 0
    return finalList


def add_in_order(stop_list, stop):
    izq, der = 0, len(stop_list) - 1
    pos = 0
    while izq <= der:
        med = (izq + der) // 2
        if stop_list[med].order_number == stop.order_number:
            pos = med
            break
        if stop.order_number < stop_list[med].order_number:
            der = med - 1
        else:
            izq = med + 1
    if izq > der:
        pos = izq
    stop_list[pos:pos] = [stop]
    return stop_list

def extractBusStops(kml_file):
    import math
    import openrouteservice
    from bs4 import BeautifulSoup as bs
    from mibus.modules.classes import busStopClass
    client = openrouteservice.Client(key='5b3ce3597851110001cf62489377f14681be4bf3a9c34d46519bf6d6')
    client1 = openrouteservice.Client(key='5b3ce3597851110001cf62489b5702d61d78455c983a4922543592c0')
    client2 = openrouteservice.Client(key='5b3ce3597851110001cf624817d765407a114a4d8e0b7e9e38b7f3f2')
    client3 = openrouteservice.Client(key='5b3ce3597851110001cf6248c294600dafbc4955814ecd9bb33e905d')
    client_list = [client, client1, client2, client3]

    round_stops = []
    return_stops = []

    soup = bs(kml_file,'lxml')
    elements = soup.find_all("placemark")
    for element in elements:
        name = element.find("name").text
        coordinates = element.find("coordinates").text
        x = coordinates.split(",")[0].strip()
        y = coordinates.split(",")[1].strip()
        extendeddata = element.find("extendeddata")
        subtitle = extendeddata.find("value").text
        direction = extendeddata.find("value").find_next('value').text
        order_number = int(extendeddata.find("value").find_next('value').find_next('value').text)
        schedule_data = extendeddata.find("value").find_next('value').find_next('value').find_next('value').text
        if direction == "Ida":
            stop = busStopClass(name, x, y, subtitle, direction, order_number, schedule_data)
            add_in_order(round_stops,stop)
        else:
            stop = busStopClass(name, x, y, subtitle, direction, order_number, schedule_data)
            add_in_order(return_stops,stop)

    for stop in return_stops:
        print(stop.order_number)
    schedule = []
    lastStop = []
    counter = 0

    return print(round_stops)

def extractAndUpdate(bus_stops, relation_id):
    from citymngmt.models import Line
    _lines = Line.objects.filter(relation_id=relation_id)
    for _line in _lines:
        stop_list = []
        for bus_stop in bus_stops:
            lines = bus_stop["lines"].split("|")
            for line in lines:
                if line == _line.name:
                    stop_list.append([bus_stop["lat"], bus_stop["lon"]])
        _line.stops = stop_list
        _line.save()

        
