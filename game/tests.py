from django.test import TestCase
# Create your tests here.
from game.models import Scenario, Input
import random
n_scenarios = 10
test_scenarios = []

class gameTest(TestCase):

    #fixtures = ['test_data.xml']
    def test_index(self):
        print("testing index...")
        resp=self.client.get('/game')
        self.assertEqual(resp.status_code, 200)

    def test_game(self):
        print("testing game...")
        #resp=self.client.get('/game/play')
        #self.assertEqual(resp.status_code, 200)
        print("SKIPPED TESTING GAME")



    #tests the creation of several scenarios, from input variables for the scenario fields
    def test_create(self):
        for i in range(0, n_scenarios):
            test_scenario = {"text": "Test Scenario "+str(i), "scenario_id": i, "order_n": 0}
            test_scenarios.append(test_scenario)
        for test_scenario in test_scenarios:
            Scenario.objects.create(text = test_scenario["text"], scenario_id= test_scenario["scenario_id"], order_n= test_scenario["order_n"] )
        self.assertEqual(len(test_scenarios), Scenario.objects.all().count())
        self.assertEqual(len(test_scenarios), n_scenarios)
        self.assertEqual(Scenario.objects.all().count(), n_scenarios)
