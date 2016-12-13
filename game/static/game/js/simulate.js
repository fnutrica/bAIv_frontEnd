
function getRandomColor() {
    return rgba_ing = 'rgba('+ (Math.floor(Math.random() * 255))+","+ (Math.floor(Math.random() * 255))+","+ (Math.floor(Math.random() * 255));
}

function updateGraph(ctx, sim_data=null){
  restaurants = Object.keys(sim_data);  
  profits = [];
  restaurants_values = Object.values(sim_data);

  random_colors = []
  random_solid = []
  for (rest in restaurants_values){
    profits.push(restaurants_values[rest].profit);
    color = getRandomColor();
    random_colors.push(color+",0.2)");
    random_solid.push(color+",1)");
  }

  var myChart = new Chart(ctx, {
  type: 'bar',
  data: {
      labels: restaurants,
      datasets: [{
          label: 'Profit',
          data: profits,
          backgroundColor: 
              random_colors
          ,
          borderColor: 
              random_solid        
          ,
          borderWidth: 1
      }]
  },
  options: {
      scales: {
          yAxes: [{
              ticks: {
                  beginAtZero:true
              }
          }]
      }
  }
});

 }
 
function showQuestions(questions) {
    formDiv = document.getElementById("user_inputs");
    formDiv.innerHTML = "";
    for (question in questions) {
        var questionDiv = document.createElement("div");
        questionDiv.innerHTML = questionDiv.innerHTML + "<h3><b>" + questions[question].question + "</b></h3>";
        questionDiv.id = "question-" + question;

        var answersDiv = document.createElement("select");
        answersDiv.form = "input-form";
        answersDiv.className = "form-control"
        answers = questions[question].answers;
        answers = answers.split(", ");
        for (answer in answers) {
            var opt = document.createElement("option");
            opt.textContent = answers[answer];
            opt.value = answers[answer];
            answersDiv.appendChild(opt);
        }
        questionDiv.appendChild(answersDiv);
        formDiv.appendChild(questionDiv);
    }

}


function simulate(my_data) {
  $("body").addClass("loading");    
  $.ajax({
      url : "/game/simulate", // the endpoint
      type : "POST", // http method
      data : my_data, // data sent with the post request
      // handle a successful response
      success : function(response) {
          updateData(response);
        }
    });
  };

function updateData(responseData){
  new_scenario_text = responseData['scenario_text'];
  questions = responseData['inputs'];
  sim_results = responseData['restaurants'];
  new_order_n = responseData['scenario_order_n'];
  
  $("#myChart").remove();
  $("#results_graph").append('<canvas id="myChart"><canvas>');
  $("#results_graph").css({"display": "block"});
  $("body").removeClass("loading");
  $("html, body").animate({ scrollTop: $(document).height() }, 1000);
  updateGraph($("#myChart"), sim_results);
  questions = JSON.parse(questions);
  $("#prompt_text").text(new_scenario_text);
  for (question in questions){
    questions[question].question=questions[question].fields.question;
    questions[question].answers = questions[question].fields.answers;
  }
  $("#prompt_text").text(new_scenario_text);
  showQuestions(questions);

  }//updateData

