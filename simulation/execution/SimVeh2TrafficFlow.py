from lxml import etree
import xmltodict, json
import os, sys, sumolib

'''Needed dependenciear are SUMO, matplotlib and pyproj'''

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

net = None
doc = None

def readInputNet(filepath):
    global net
    net = sumolib.net.readNet(filepath)
    global doc
    doc = etree.parse(filepath)

def parseXMLtoEdgeLane(filepath, outputfile):
    # entries_to_remove = {'CO', 'CO2', 'HC', 'NOx', 'PMx', 'electricity', 'fuel', 'noise'}
    entries_to_keep = {'id', 'maxspeed', 'meanspeed', 'occupancy', 'shape'}
    with open(outputfile, 'w') as fb:
        fb.write('<full-export>')
        for event, elem in etree.iterparse(filepath, events = ('start', 'end')):
            if event == 'start':
                if elem.tag == 'data':
                    latest_timestep = elem.attrib['timestep']
                    elem.clear()
            if event == 'start':
                if elem.tag == 'edge':
                    elem.nsmap.pop('xsi', None)
                    elem.set('timestep', latest_timestep)
                    for j in elem.iterfind("lane"):
                        lane_id = j.attrib['id']
                        lon_lat_array = findLonLat(lane_id)
                        j.set('shape', str(lon_lat_array))
                        attributes = j.attrib
                        attributes = j.attrib
                        for attribute in attributes.keys():
                            if attribute not in entries_to_keep:
                                j.attrib.pop(attribute, None)
                    fb.write(etree.tostring(elem, encoding='utf8').decode('utf8'))
                    elem.clear()
            if event == 'end':
                elem.clear()
        fb.write('</full-export>')

def findLonLat(laneid):
    query_string = "//lane[@id=" + "'" + laneid +  "'" + "]/@shape"
    shape = doc.xpath(query_string)
    list_shape = shape[0].split(' ')
    number_array = []
    for coor in list_shape:
        coordinates = coor.split(',')
        lon, lat = net.convertXY2LonLat(float(coordinates[0]), float(coordinates[1]))
        number_array.append(lon)
        number_array.append(lat)
    str_shape = ','.join(map(str, number_array))
    # print(number_array)
    return str_shape

#Call example

readInputNet('../data/input-simulation/small-extract-for-testing/net.net.xml')
# parseXMLtoEdgeLane('data.xml', 'dataAfterParsingXML.xml')
parseXMLtoEdgeLane('../data/input-simulation/small-extract-for-testing/data.xml', 'dataAfterParsingXML2.xml')