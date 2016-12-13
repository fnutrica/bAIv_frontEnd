from random import randint
from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import Scenario, Input
from django.core import serializers
from . import Customer 
from . import Tipping_Sim

# Create your views here.

def play(request):
    initial_scenarios = Scenario.objects.filter(order_n=0)
    count = initial_scenarios.count()
    if (count is not None):
        if (count > 0): 
            index = randint(0, count-1)
            my_scenario = initial_scenarios[index]
            my_inputs = Input.objects.all().filter(scenario = my_scenario)
            context = {"scenario_text": my_scenario.text, "scenario_order_n": my_scenario.order_n,"scenario_id": my_scenario.scenario_id, "inputs": my_inputs}
            return render(request, 'game/simulation.html', context)
    else:
        return ('<h1>Website is under construction... brace for awesomeness!</h1>')

def index(request):
    return render(request, 'game/home.html')

def find_next(scenario_id, order_n):
        return Scenario.objects.filter(scenario_id = scenario_id).filter(order_n=order_n)[0]


def simulate(request):
    if request.method == 'POST':
        answered_questions = []
        questions = request.POST.keys()
        for question in questions:
            answer = request.POST.get(question)
            answered_questions.append({"question":question, "answer": answer})
        curr_order = int(float(request.POST.get("order_n")))
        scenario_id = int(float(request.POST.get("scenario_id")));
        pot_scenarios = Scenario.objects.filter(scenario_id = scenario_id)
        if (curr_order< len(pot_scenarios)-1):
            next_order = curr_order+1; 
        else:
            next_order = curr_order

        my_scenario= find_next(scenario_id, next_order)
        my_inputs = serializers.serialize("json",Input.objects.all().filter(scenario = my_scenario))
        


        init_price= request.POST.get("init_price")
        n_restaurants= request.POST.get("n_restaurants")
        n_customers= request.POST.get("n_customers")
        max_generations= request.POST.get("max_generations")

        sim_data = [init_price,n_restaurants,n_customers,max_generations]
        sim_data_ints = []
        for i in range(len(sim_data)):
            if sim_data[i] is not None:
                sim_data[i] = int(sim_data[i])

        restaurants = Tipping_Sim.tipping_sim(sim_data[0], sim_data[1], sim_data[2], sim_data[3])
        response_data = {"scenario_text": my_scenario.text, "scenario_order_n": my_scenario.order_n,"scenario_id": my_scenario.scenario_id, "inputs": my_inputs, "restaurants": restaurants}
        
        return HttpResponse(
            json.dumps(response_data) ,
            content_type="application/json"
            )   
    else:
        return HttpResponse(
            json.dumps({"error": "did not return a valid response"}),
            content_type="application/json"
        )
