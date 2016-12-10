from random import randint
from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import Player, Scenario, Input
from django.core import serializers
from . import Customer 
from . import Tipping_Sim

# Create your views here.

def play(request):
    initial_scenarios = Scenario.objects.filter(order_n=0)
    count = initial_scenarios.count()
    print("count: "+ str(count))
    if (count is not None):
        if (count > 0): 
            index = randint(0, count-1)
            my_scenario = initial_scenarios[index]
            my_inputs = Input.objects.all().filter(scenario = my_scenario)
            context = {"scenario_text": my_scenario.text, "scenario_order_n": my_scenario.order_n,"scenario_id": my_scenario.scenario_id, "inputs": my_inputs}
            return render(request, 'game/home.html', context)
    else:
        return ('<h1>Website is under construction... brace for awesomeness!</h1>')

def index(request):
    return render(request, 'game/info.html')

#Finds follow up scenario for more complext simulations. Currently set to keep the same scenario
def find_next(scenario_id, order_n):
        return Scenario.objects.filter(scenario_id = scenario_id).filter(order_n=order_n)[0]


def simulate(request):
    if request.method == 'POST':
        answered_questions = []
        questions = request.POST.keys()
        for question in questions:
            answer = request.POST.get(question)
            answered_questions.append({"question":question, "answer": answer})
        next_order = int(float(request.POST.get("order_n")));  #can add 1 to order_n when more complex scenarios are built
        scenario_id = int(float(request.POST.get("scenario_id")));
        my_scenario= find_next(scenario_id, next_order)
        my_inputs = serializers.serialize("json",Input.objects.all().filter(scenario = my_scenario))
        

        """
        response_data = {}
        response_data['scenario_text'] = my_scenario.text
        response_data['scenario_order_n'] = my_scenario.order_n
        response_data['scenario_id'] = my_scenario.scenario_id
        response_data['inputs'] = my_inputs
        """

        #send request data to algorithm, get results as response 

        #store results from passing input values to python script
        #generating random data until the algorithm is added into this

        
        #sim_results = Tipping_Sim.tipping_sim()
        sim_results = [{"gens":1, "seller": "restID1", "profit":125, "units_sold":100, "likelihood": 10 },
                    {"gens":1, "seller": "restID1", "profit":125, "units_sold":100, "likelihood": 10},
                    {"gens":1, "seller": "restID1", "profit":125, "units_sold":100, "likelihood": 10},
                    {"gens":1, "seller": "restID1", "profit":125, "units_sold":100, "likelihood": 10 },
                    {"gens":1, "seller": "restID1", "profit":125, "units_sold":100, "likelihood": 100 },
                    {"gens":1, "seller": "restID1", "profit":125, "units_sold":100, "likelihood": 10 },
                    {"gens":1, "seller": "restID1", "profit":125, "units_sold":100, "likelihood": 10 },
                    {"gens":1, "seller": "restID1", "profit":125, "units_sold":100, "likelihood": 10 },
                    {"gens":1, "seller": "restID1", "profit":125, "units_sold":100, "likelihood": 10},
                    {"gens":1, "seller": "restID1", "profit":125, "units_sold":100, "likelihood": 10}]
        restaurants = {"player":{"gens":1, "seller": "restID1", "profit":125, "units_sold":100, "likelihood": 10}, 
                       "other1":{"gens":1, "profit":125, "units_sold":100, "likelihood": 10},
                       "other2":{"gens":1, "profit":125, "units_sold":100, "likelihood": 10}
                       } #list of restaurants objects, containing their final attributes after simulating
        #restaurants = serializers.serialize("json",restaurants)   necessary??

         #fake data from the algorithm




        """
        NO LONGER NECESSARY IF WE PASS RESTAURANT OBJECTS FROM THE SCRIPT

        sim_results.sort(key=operator.itemgetter('gens'))


        restaurant_data = {}

        for result in sim_results:
            restaurant_id = result.seller
            if restaurant_id not in restaurant_data:
                restaurant_data[restaurant_id].profit = result.profit
                restaurant_data[restaurant_id].units_sold = result.units_sold
                restaurant_data[likelihood].units_sold = result.likelihood

            else: 
                restaurant_data[likelihood].units_sold = result.likelihood  #storing last observed likelihood              
                keys = restaurant_data
        """


        

        response_data = {"scenario_text": my_scenario.text, "scenario_order_n": my_scenario.order_n,"scenario_id": my_scenario.scenario_id, "sim_results": sim_results, "inputs": my_inputs, "restaurants": restaurants}
        
        return HttpResponse(
            json.dumps(response_data) ,
            content_type="application/json"
            )   
    else:
        return HttpResponse(
            json.dumps({"error": "did not return a valid response"}),
            content_type="application/json"
        )
