from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter

from SIR_wolf_sheep.SIR.agents import Susceptible, Infectious, Removed
from SIR_wolf_sheep.SIR.model import SIR


def agents_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Susceptible:
        if agent.infected:
            portrayal["Color"] = ["#dbd842", "#dbd842", "#dbd842"]
        else:
            portrayal["Color"] = ["#42a0db", "#42a0db", "#42a0db"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    elif type(agent) is Infectious:
        portrayal["Color"] = ["#de3737", "#de3737", "#de3737"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    elif type(agent) is Removed:
        portrayal["Color"] = ["#b3b3b3", "#b3b3b3", "#b3b3b3"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


canvas_element = CanvasGrid(agents_portrayal, SIR.height, SIR.width, 500, 500)
chart_element = ChartModule([{"Label": "Susceptible", "Color": "#dbd842"},
                             {"Label": "Infected", "Color": "#de3737"},
                             {"Label": "Removed", "Color": "#b3b3b3"}])

# text_element = TextElement([{"R": "Susceptible", "Color": "#dbd842"},
#                              {"Label": "Infected", "Color": "#de3737"},
#                              {"Label": "Removed", "Color": "#b3b3b3"}])

model_params = {"initial_susceptible": UserSettableParameter('slider', 'Initial Susceptible Population', 25, 25, 200),
                "initial_infected": UserSettableParameter('slider', 'Initial Infected Population', 1, 1, 10),
                "probability_recognized": UserSettableParameter('slider', 'Probability to be recognized as infected', 0.8, 0.1, 1.0, 0.05),
                "infection_radius": UserSettableParameter('slider', 'Infection Radius (Cells in Grid)', 1, 1, 3),
                "spread_probability": UserSettableParameter('slider', 'Probability to spread virus when in infection radius', 0.3, 0.1, 1.0, 0.05),
                "movement": UserSettableParameter('choice', 'Movement Setting', value="random", choices=['random', 'random_center'])}

server = ModularServer(SIR, [canvas_element, chart_element], "SIR", model_params)
server.port = 8521

# front-end: mini react slider, chart js für animation, pixie js
# react nav elemente einbinden - dom element
# package in react - deklerativ im js style pixie js bauen
# deklerative syntax