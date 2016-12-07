from random import randint
from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import Player, Scenario, Input
from django.core import serializers

# Create your views here.

def index(request):
    initial_scenarios = Scenario.objects.filter(order_n=0)
    count = initial_scenarios.count()
    index = randint(0, count-1)
    my_scenario = initial_scenarios[index]
    my_inputs = Input.objects.all().filter(scenario = my_scenario)
    context = {"scenario_text": my_scenario.text, "scenario_order_n": my_scenario.order_n,"scenario_id": my_scenario.scenario_id, "inputs": my_inputs}
    
    return render(request, 'game/home.html', context)

def info(request):
    return render(request, 'game/info.html')

def simulate(request):
    if request.method == 'POST':
        answered_questions = []
        questions = request.POST.keys()
        for question in questions:
            answer = request.POST.get(question)
            answered_questions.append({"question":question, "answer": answer})
        next_order = int(float(request.POST.get("order_n")))+1;
        next_id = int(float(request.POST.get("scenario_id")));

        my_scenario= Scenario.objects.filter(scenario_id = next_id).filter(order_n=next_order)[0]
        my_inputs = serializers.serialize("json",Input.objects.all().filter(scenario = my_scenario))

        response_data = {}
        response_data['scenario_text'] = my_scenario.text
        response_data['scenario_order_n'] = my_scenario.order_n
        response_data['scenario_id'] = my_scenario.scenario_id
        response_data['inputs'] = my_inputs

        context = {"scenario_text": my_scenario.text, "scenario_order_n": my_scenario.order_n,"scenario_id": my_scenario.scenario_id} # "inputs": my_inputs}
        
        return HttpResponse(
            json.dumps(response_data) ,
            content_type="application/json"
            )   
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )
