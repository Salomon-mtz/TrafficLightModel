import mesa
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid

from agents import TrafficLight, Vehicle, SideWalk, Building
from model import TrafficModel

def TrafficModel_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is TrafficLight:
        portrayal["Layer"] = 1
        portrayal["Color"] = agent.state
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["w"] = 0.5
        portrayal["h"] = 0.8
        portrayal["text"] = agent.pos

    elif type(agent) is SideWalk:
        portrayal["Color"] = "gray"
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1
    
    elif type(agent) is Building:
        portrayal["Color"] = "gray"
        portrayal["Shape"] = "2271676.png"
        portrayal["Filled"] = "true"
        portrayal["text"] = "edificio"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1
        
    elif type(agent) is Vehicle:
        portrayal["Layer"] = 1
        portrayal["Color"] = ["#69C7B7"]
        portrayal["Shape"] = "circle"
        portrayal["Filled"] = "true"
        portrayal["r"] = 0.5
        portrayal["text"] = agent.pos
        # Change the color of the vehicle according to its speed
        if agent.speed == 1:
            portrayal["Color"] = ["#966525"]
        elif agent.speed == 2:
            portrayal["Color"] = ["#D50FDB"]
        elif agent.speed == 3:
            portrayal["Color"] = ["#812696"]
        elif agent.speed == 4:
            portrayal["Color"] = ["#048FDB"]

        if agent.pesero:
            portrayal["Color"] = ["black"]
            portrayal["r"] = 1

    return portrayal


canvas_element = CanvasGrid(TrafficModel_portrayal, 16, 16, 600, 600)

# Charts
directions_chart = mesa.visualization.ChartModule([
    {"Label": "Crashes", "Color": "red"},
], data_collector_name='datacollector')

speed_chart = mesa.visualization.ChartModule([
    {"Label": "Speed1", "Color": "yellow"},
    {"Label": "Speed2", "Color": "red"},
    {"Label": "Speed3", "Color": "blue"},
    {"Label": "Speed4", "Color": "green"},
], data_collector_name='datacollector')

crossed_chart = mesa.visualization.ChartModule([
    {"Label": "Vehicles_crossed_up", "Color": "Black"},
    {"Label": "Vehicles_crossed_down", "Color": "Blue"},
    {"Label": "Vehicles_crossed_left", "Color": "Brown"},
    {"Label": "Vehicles_crossed_right", "Color": "Pink"}
], data_collector_name='datacollector')

model_params = {
    "nVehicles": 10}

server = ModularServer(
    TrafficModel, [canvas_element,directions_chart,speed_chart,crossed_chart], "Traffic Simulation", model_params
)
server.port = 8521

server.launch()