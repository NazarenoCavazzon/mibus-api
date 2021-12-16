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

def time_to_hours(time):
    import datetime
    time = str(datetime.timedelta(seconds=time+17))
    return time.split('.')[0]

def time_to_seconds(time):
    import datetime
    date_time = datetime.datetime.strptime(str(time), "%H:%M:%S")
    a_timedelta = date_time - datetime.datetime(1900, 1, 1)
    seconds = a_timedelta.total_seconds()
    return seconds

def time_to_seconds_start(time):
    import datetime
    date_time = datetime.datetime.strptime(str(time), "%H:%M")
    a_timedelta = date_time - datetime.datetime(1900, 1, 1)
    seconds = a_timedelta.total_seconds()
    return seconds

def extractBusStops(kml_file, relation_id, line_id):
    from citymngmt.models import BusStop
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
        lon = coordinates.split(",")[0].strip()
        lat = coordinates.split(",")[1].strip()
        extendeddata = element.find("extendeddata")
        subtitle = extendeddata.find("value").text
        direction = extendeddata.find("value").find_next('value').text
        order_number = int(extendeddata.find("value").find_next('value').find_next('value').text)
        schedule_data = extendeddata.find("value").find_next('value').find_next('value').find_next('value').text.split('|')
        if direction == "Ida":
            stop = busStopClass(name, lat, lon, subtitle, direction, order_number, schedule_data)
            add_in_order(round_stops,stop)
        else:
            stop = busStopClass(name, lat, lon, subtitle, direction, order_number, schedule_data)
            add_in_order(return_stops,stop)

    lastStop = None
    counter = 0

    for stop in round_stops:
        if counter == len(client_list):
            counter = 0
        if stop.schedule_data[0] != '':
            lastStop = stop
            for i in range(len(stop.schedule_data)):
                stop.schedule_data[i] = time_to_hours(time_to_seconds_start(stop.schedule_data[i]))
        else:
            coords = ((lastStop.lon, lastStop.lat),(stop.lon, stop.lat))
            res = client_list[counter].directions(coords)
            duration = res['routes'][0]['summary']['duration']
            for schedule in lastStop.schedule_data:
                seconds = time_to_seconds(schedule)
                seconds += duration
                stop.schedule_data.append(time_to_hours(seconds))
            stop.schedule_data.remove('')
            lastStop = stop
        counter += 1
    
    for stop in return_stops:
        if counter == len(client_list):
            counter = 0
        if stop.schedule_data[0] != '':
            lastStop = stop
            for i in range(len(stop.schedule_data)):
                stop.schedule_data[i] = time_to_hours(time_to_seconds_start(stop.schedule_data[i]))
        else:
            coords = ((lastStop.lon, lastStop.lat),(stop.lon, stop.lat))
            res = client_list[counter].directions(coords)
            duration = res['routes'][0]['summary']['duration']
            for schedule in lastStop.schedule_data:
                seconds = time_to_seconds(schedule)
                seconds += duration
                stop.schedule_data.append(time_to_hours(seconds))
            stop.schedule_data.remove('')
            lastStop = stop
        counter += 1         
    
    all_stops = round_stops + return_stops

    BusStop.objects.filter(line_id=line_id).delete()

    BusStop.objects.bulk_create(
        BusStop(relation_id=relation_id, line_id=line_id, name=stop.name, lat=stop.lat, lon=stop.lon, subtitle=stop.subtitle, direction=stop.direction, order_number=stop.order_number, schedule=stop.schedule_data) for stop in all_stops
        )

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

        
