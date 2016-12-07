from random import randint
from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import Player, Scenario, Input

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
        print(request)

        answered_questions = []
        questions = request.POST.keys()
        for question in questions:
            answer = request.POST.get(question)
            answered_questions.append({"question":question, "answer": answer})
        next_order = int(float(request.POST.get("order_n")))+1;
        next_id = int(float(request.POST.get("scenario_id")));

        my_scenario= Scenario.objects.filter(scenario_id = next_id).filter(order_n=0)[0]
        my_inputs = Input.objects.all().filter(scenario = my_scenario)
        context = {"scenario_text": my_scenario.text, "scenario_order_n": my_scenario.order_n,"scenario_id": my_scenario.scenario_id, "inputs": my_inputs}
        return HttpResponse(
            context,
            content_type="application/parameter"
            )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

    """    


        response_data = {}

        response_data['resulst'] = 'Create post successful!'
        response_data['postpk'] = post.pk
        response_data['text'] = post.text
        response_data['created'] = post.created.strftime('%B %d, %Y %I:%M %p')
        response_data['author'] = post.author.username

         HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )return
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

    """