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

def extractBusStops(kml_file):
    from bs4 import BeautifulSoup as bs
    finalList = []
    finalListPrint = []
    soup = bs(kml_file,'lxml')
    coordinates = soup.find_all("placemark")
    for element in coordinates:
        cacheList = {
            "lines": [],
            "name": "",
            "subtitle": "",
            "address": "",
            "lat": 0,
            "lon": 0,
            "zone":""
        }
        name = element.find("name").text
        coordinates = element.find("coordinates").text
        x = coordinates.split(",")[0].strip()
        y = coordinates.split(",")[1].strip()
        extendeddata = element.find("extendeddata")
        valueLineas = extendeddata.find("value").text
        valueSentido = extendeddata.find("value").find_next('value').text
        valueZona = extendeddata.find("value").find_next('value').find_next('value').text
        finalList.append([x,y,name,valueLineas,valueSentido, valueZona])
        cacheList["lines"] = valueLineas
        cacheList["name"] = name
        cacheList["subtitle"] = valueSentido
        cacheList["address"] = name
        cacheList["lat"] = float(y)
        cacheList["lon"] = float(x)
        cacheList["zone"] = valueZona
        finalListPrint.append(cacheList)
    return finalListPrint

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

        
