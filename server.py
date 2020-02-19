from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from agents import Fox, Bunny, GrassPatch
from model import Environment


def environment_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Bunny:
        portrayal["Shape"] = "pictures/bunny.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    elif type(agent) is Fox:
        portrayal["Shape"] = "pictures/fox.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        portrayal["text"] = round(agent.energy, 1)
        portrayal["text_color"] = "White"

    elif type(agent) is GrassPatch:
        if agent.fully_grown:
            portrayal["Color"] = ["#00FF00", "#00CC00", "#009900"]
        else:
            portrayal["Color"] = ["#84e184", "#adebad", "#d6f5d6"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


canvas_element = CanvasGrid(environment_portrayal, 20, 20, 500, 500)
chart_element = ChartModule([{"Label": "Foxes", "Color": "#AA0000"},
                             {"Label": "Bunny", "Color": "#666666"}])

model_params = {"grass": UserSettableParameter('checkbox', 'Grass Enabled', True),
                "grass_regrowth_time": UserSettableParameter('slider', 'Grass Regrowth Time', 20, 1, 50),
                "initial_bunny": UserSettableParameter('slider', 'Initial Bunny Population', 100, 10, 300),
                "bunny_reproduce": UserSettableParameter('slider', 'Bunny Reproduction Rate', 0.04, 0.01, 1.0,
                                                         0.01),
                "initial_fox": UserSettableParameter('slider', 'Initial Fox Population', 50, 10, 300),
                "fox_reproduce": UserSettableParameter('slider', 'Fox Reproduction Rate', 0.05, 0.01, 1.0,
                                                        0.01,
                                                        description="The rate at which Fox agents reproduce."),
                "fox_gain_from_food": UserSettableParameter('slider', 'Fox Gain From Food Rate', 20, 1, 50),
                "bunny_gain_from_food": UserSettableParameter('slider', 'Bunny Gain From Food', 4, 1, 10)}

server = ModularServer(Environment, [canvas_element, chart_element], "Fox Bunny World", model_params)
server.port = 8000
