from lxml import etree
from bson.json_util import dumps
import math
# from app.models.traffic_flow import TrafficFlow

box_384_edges = ['486816973', '-486816973', '22327902#0', '-22327902#0', '22327902#1','-22327902#1','22327902#2','-22327902#2','22327902#3','-22327902#3','22327902#4','-34335059','34335064','-34335064','172675262#1','-172675262#1','172675262#0','-172675262#0'
           '171610162#3', '-172675260', '-171610162#2','171610162#2'
           ]
box_672_edges = ['4294652#1', '-4294652#2', '4294652#2', '-4294652#1', '4294652#3', '-4294652#3', '144116760#1', '-144116760#1', '144116761', '-144116761']
box_671_edges = ['44369045', '-44369045','421617196', '-421617196', '52937670', '4082009']
box_670_edges = ['159269895#1', '35165735', '477543784#1','-477543784#1', '-477543784#2', '-486563017']

boxes_edges = {
    '384':box_384_edges ,
    '672': box_672_edges,
    '671':box_671_edges,
    '670':box_670_edges
    }

boxes_edges_speeds = {
    '384':[] ,
    '672': [],
    '671': [],
    '670': []
    }

boxes_edges_avg_speeds = {
    '384':[] ,
    '672': [],
    '671': [],
    '670': []
    }

boxes_edges_congestion = {
    '384':[] ,
    '672': [],
    '671': [],
    '670': []
    }

boxes_edges_quality_of_travel = {
    '384':[] ,
    '672': [],
    '671': [],
    '670': []
    }

max_speeds_of_edges = {}
max_speeds_of_edges['486816973'] = 8.33
max_speeds_of_edges['-486816973'] = 8.33
max_speeds_of_edges['22327902#0'] = 8.33
max_speeds_of_edges['22327902#1'] = 8.33
max_speeds_of_edges['-22327902#0'] = 8.33
max_speeds_of_edges['-22327902#1'] = 8.33
max_speeds_of_edges['22327902#2'] = 8.33
max_speeds_of_edges['-22327902#2'] = 8.33
max_speeds_of_edges['22327902#3'] = 8.33
max_speeds_of_edges['-22327902#3'] = 8.33
max_speeds_of_edges['22327902#4'] = 8.33
max_speeds_of_edges['-34335059'] = 8.33
max_speeds_of_edges['-34335064'] = 8.33
max_speeds_of_edges['34335064'] = 8.33
max_speeds_of_edges['172675262#1'] = 13.89
max_speeds_of_edges['-172675262#1'] = 13.89
max_speeds_of_edges['172675262#0'] = 13.89
max_speeds_of_edges['-172675262#0'] = 13.89
max_speeds_of_edges['171610162#3'] = 13.89
max_speeds_of_edges['-172675260'] = 13.89
max_speeds_of_edges['-171610162#2'] = 13.89
max_speeds_of_edges['171610162#2'] = 13.89

max_speeds_of_edges['4294652#1'] = 13.89
max_speeds_of_edges['-4294652#1'] = 13.89
max_speeds_of_edges['-4294652#2'] = 13.89
max_speeds_of_edges['4294652#2'] = 13.89
max_speeds_of_edges['4294652#3'] = 13.89
max_speeds_of_edges['-4294652#3'] = 13.89
max_speeds_of_edges['144116760#1'] = 13.89
max_speeds_of_edges['-144116760#1'] = 13.89
max_speeds_of_edges['144116761'] = 19.44
max_speeds_of_edges['-144116761'] = 19.44

max_speeds_of_edges['44369045'] = 19.44
max_speeds_of_edges['-44369045'] = 19.44
max_speeds_of_edges['421617196'] = 13.89
max_speeds_of_edges['-421617196'] = 13.89
max_speeds_of_edges['52937670'] = 13.89
max_speeds_of_edges['4082009'] = 13.89

max_speeds_of_edges['159269895#1'] = 13.89
max_speeds_of_edges['35165735'] = 13.89
max_speeds_of_edges['477543784#1'] = 13.89
max_speeds_of_edges['-477543784#1'] = 13.89
max_speeds_of_edges['-477543784#2'] = 13.89
max_speeds_of_edges['-486563017'] = 8.33

class TrafficFlow(object):

    def __init__(self, freeflow_speed, avg_speed, congested, expected_quality_of_travel):
        self.freeflow_speed = freeflow_speed
        self.avg_speed = avg_speed
        self.congested = congested
        self.expected_quality_of_travel = expected_quality_of_travel

    def json(self):
        return {
            'freeflow_speed': self.freeflow_speed,
            'avg_speed': self.avg_speed,
            'congested': self.congested,
            'expected_quality_of_travel': self.expected_quality_of_travel
            }

def parse_and_save(filepath):
    # tree = etree.ElementTree(etree.fromstring(filepath))
    tree = etree.parse(filepath)
    root = tree.getroot()
    simulation_id = ''
    scenario = ''
    i = 0
    for elem in root.iter('edge'):
        if i == 0:
            parent = elem.getparent()
            simulation_id = parent.attrib['id']
            scenario = parent.attrib['scenario']
        edgeid = elem.attrib['id']
        if edgeid in box_384_edges:
            fill_dictionaries('384', elem, edgeid)
        elif edgeid in box_672_edges:
            fill_dictionaries('672', elem, edgeid)
        elif edgeid in box_671_edges:
            fill_dictionaries('671', elem, edgeid)
        elif edgeid in box_670_edges:
            fill_dictionaries('670', elem, edgeid)

    print(boxes_edges_speeds)
    print(boxes_edges_avg_speeds)
    print(boxes_edges_congestion)
    print(boxes_edges_quality_of_travel)
    construct_json(simulation_id, scenario)
def construct_json(simulation_id, scenario):
    box_384 =  get_averages('384')
    box_672 = get_averages('672')
    box_671 = get_averages('671')
    box_670 = get_averages('670')
    json_result = {
            'simulation_id': simulation_id,
            'scenario': scenario,
            'simulation':[
                {
                    'box_id': '384',
                    'traffic_flow': TrafficFlow(box_384[0], box_384[1], box_384[2], box_384[3]).json()
                    },
                {
                    'box_id': '672',
                    'traffic_flow': TrafficFlow(box_672[0], box_672[1], box_672[2], box_672[3]).json()
                    },
                {
                    'box_id': '671',
                    'traffic_flow': TrafficFlow(box_671[0], box_671[1], box_671[2], box_671[3]).json()
                    },
                {
                    'box_id': '670',
                    'traffic_flow': TrafficFlow(box_670[0], box_670[1], box_670[2], box_670[3]).json()
                    }
                ]
        }
    # print(dumps(json_result))

def get_averages(box_id):
    freeflow_speed = math.ceil(sum(boxes_edges_speeds[box_id])/float(len(boxes_edges_speeds[box_id])))
    avg_speed = math.ceil(sum(boxes_edges_avg_speeds[box_id])/float(len(boxes_edges_avg_speeds[box_id])))
    congestion_value = math.ceil(sum(boxes_edges_congestion[box_id])/float(len(boxes_edges_congestion[box_id])))
    expected_quality_of_travel = math.floor(sum(boxes_edges_quality_of_travel[box_id]) / float(len(boxes_edges_quality_of_travel[box_id])))
    congested = False
    if congestion_value  > 5:
        congested = True
    if congestion_value >= 5 and congestion_value < 13:
        expected_quality_of_travel = 4
    if congestion_value >= 13 and congestion_value <= 30:
        expected_quality_of_travel = 3
    if congestion_value > 30:
        expected_quality_of_travel = 1
    print(freeflow_speed, avg_speed, congested, expected_quality_of_travel, congestion_value)
    return (freeflow_speed, avg_speed, congested, expected_quality_of_travel)

def fill_dictionaries(box_id, elem, edgeid):
    freeflow_speed = math.ceil(3.6*float(max_speeds_of_edges[edgeid]))
    avg_speed = math.ceil(3.6*float(elem.attrib['speed']))
    congested = math.ceil(float(elem.attrib['occupancy']))
    print(congested)
    x = math.ceil(float(100 - float(congested)))
    expected_quality_of_travel = math.floor((x / 10.0))

    boxes_edges_speeds[box_id].append(freeflow_speed)
    boxes_edges_avg_speeds[box_id].append(avg_speed)
    boxes_edges_congestion[box_id].append(congested)
    boxes_edges_quality_of_travel[box_id].append(expected_quality_of_travel)


xml = '<meandata xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/meandata_file.xsd"><interval begin="1000.00" end="5000.00" id="2019-07-12-11-17-06-30751d2a-323c-407d-b420-df900258a045" scenario="morning"><edge id="486816973" sampledSeconds="135.28" traveltime="6.49" overlapTraveltime="7.12" density="0.41" occupancy="0.19" waitingTime="0.00" speed="12.34" departed="0" arrived="1" entered="19" left="18" laneChangedFrom="0" laneChangedTo="0"/><edge id="-103901661" sampledSeconds="2.01" overlapTraveltime="2.09" density="2.52" occupancy="0.05" waitingTime="0.00" speed="2.48" departed="1" arrived="0" entered="0" left="1" laneChangedFrom="0" laneChangedTo="0"/>   </interval></meandata>'
parse_and_save('../data/output-simulation/edge.xml')
# doc = etree.parse('../data/output-simulation/edge.xml')
# query_string = "//edge[@id=" + "'" + '486816973' +  "'" + "]"
# shape = doc.xpath(query_string)
# print(shape[0])


