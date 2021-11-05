var request_options_all = (function() {
        var json = null;
        $.ajax({
          'async': false,
          'global': false,
          'url': "request_options.json",
          'dataType': "json",
          'success': function(data) {
            json = data;
          }
        });
        return json;
      })();

var request_options = request_options_all['request_options'];


var options_all = (function() {
        var json = null;
        $.ajax({
          'async': false,
          'global': false,
          'url': "options.json",
          'dataType': "json",
          'success': function(data) {
            json = data;
          }
        });
        return json;
      })();

function get_request_options(requestingfor){
  var secreview_options = options_all["others"];
  $.each(options_all, function(key,value){
    if (key == requestingfor)
    {
      secreview_options = options_all[key]
      if(value['other_options'] == true)
      {
        $.each(options_all['others'], function(all_key,all_value){
          secreview_options[all_key] = all_value;
        });
        delete secreview_options['other_options'];
      }
    }
  });
  return secreview_options;
}

// console.log(options_all);

function deleteChilds(divname) { 
    var e = document.querySelector(divname); 
    // alert(e);
    //e.firstElementChild can be used. 
    var child = e.lastElementChild;  
    while (child) { 
        e.removeChild(child); 
        child = e.lastElementChild; 
    } 
} 

function requestingfor() {
  var environment = document.getElementById("request").value;

  var breaker = document.createElement("BR");
  var button = document.createElement("BUTTON");
  button.innerHTML = "Submit";
  button.className = "form-control btn btn-primary";
  button.style.width = "200px";

  var hidden = document.createElement("INPUT");
  hidden.type = "hidden";
  hidden.value = environment;
  hidden.name = "requestingfor";

  var env_count = 0;

  function createLabel(labelText){
    var label = document.createElement("LABEL");
    label.className = "line-spaccing";

    var t = document.createTextNode(labelText);
    label.setAttribute("for", "label");
    label.appendChild(t);
    document.getElementById("form_div").appendChild(label);
  }

  for(key in request_options){
    if (key == environment){
      env_count += 1;
      base_elements = request_options[key];
      document.getElementById("form_div").innerHTML = "";

      for (index in base_elements){
        var elementType = base_elements[index]['elementType'];
        if (elementType == "input"){
          var input = document.createElement("INPUT");
          input.name = base_elements[index]['name'];
          input.type = base_elements[index]['type'];
          input.placeholder = base_elements[index]['placeholder'];
          input.className = "form-control line-spaccing";
          // input.style = "margin-bottom: 10px";
          input.required = true;
          if(base_elements[index].hasOwnProperty("label"))
            createLabel(base_elements[index]['label']);
        }

        if (elementType == "textarea"){
          var input = document.createElement("TEXTAREA");
          input.rows = 3;
          input.name = base_elements[index]['name'];
          input.innerHTML = base_elements[index]['innerHtml'];
          input.className = "form-control line-spaccing";

          if(base_elements[index].hasOwnProperty("label"))
            createLabel(base_elements[index]['label']);
        }

        if (elementType == "file"){
          var input = document.createElement("INPUT");
          input.type = base_elements[index]['type'];
          
          if(base_elements[index].hasOwnProperty("label"))
            createLabel(base_elements[index]['label']);
        }

        if (elementType == "date"){
          var input = document.createElement("INPUT");
          input.type = base_elements[index]['type'];
          
          if(base_elements[index].hasOwnProperty("label"))
            createLabel(base_elements[index]['label']);
        }

        document.getElementById("form_div").appendChild(input);
      }

      document.getElementById("form_div").appendChild(hidden);
      document.getElementById("form_div").appendChild(breaker);
      document.getElementById("form_div").appendChild(button);

      var div = document.getElementById('description');
      div.classList.remove("description-hide");
      div.className += ' description-show';
    }
  }
  if (env_count == 0)
    document.getElementById("form_div").innerHTML = "";
}

  function go_back(){
    var div_ticket_details = document.getElementById('ticket_details');
    div_ticket_details.classList.remove("hidden");
    div_ticket_details.className += 'shown';

    var div = document.getElementById('description');
    div.classList.remove("shown");
    div.className = 'hidden';

    return false;

  }

function open_issue(key,status,summary,requestingfor){
  if(status == "To Do" || status == "Waiting for customer")
    alert("Ticket can not be Approved. Only Reject action allowed with JIRA status# "+status);
 
  if(requestingfor == "")
    requestingfor = "sec_bug";

  issue_status = status;
  issue_key = key;
  
  document.getElementById('ticket_options').innerHTML="";

  peer_review_needed = false;
  for (var i = 0; i < PEER_REVIEW_REQUIRED_FOR.length; i++) {
    if(summary.includes(PEER_REVIEW_REQUIRED_FOR[i]))
    {
      peer_review_needed = true;
      break;
    }

  }
  var approve_action = document.createElement("INPUT");
  approve_action.type = "submit";
  approve_action.name = "Action";
  // console.log(key,status,summary,requestingfor);
  if(status.toLowerCase() == "under review" || !peer_review_needed)
    approve_action.value = "Approve";
  else
    approve_action.value = "Send for Review";
  approve_action.classList = "btn btn-success";

  var close_action = document.createElement("INPUT");
  close_action.type = "submit";
  close_action.name = "Action";
  close_action.id = "Reject";
  close_action.value = "Reject";
  close_action.classList = "btn btn-danger";
  
  var approve_div = document.createElement("DIV");
  approve_div.classList = "pull-left";

  var close_div = document.createElement("DIV");
  close_div.classList = "pull-right";

  var action_div = document.getElementById('Action');
  action_div.innerHTML = "";

  approve_div.appendChild(approve_action);
  action_div.appendChild(approve_div);

  close_div.appendChild(close_action);
  action_div.appendChild(close_div);

  // var ticket_details = '';
  document.getElementById('key').innerHTML = key;
  document.getElementById('summary').innerHTML = summary;
  document.getElementById('status').innerHTML = status;
  document.getElementById('ticket_status').value = status;
  document.getElementById('ticket_id').value = key;
  document.getElementById('requestingfor').value = requestingfor;

  var div_ticket_details = document.getElementById('ticket_details');
  div_ticket_details.classList.remove("shown");
  div_ticket_details.className += 'hidden';

  var div = document.getElementById('description');
  div.classList.remove("hidden");
  div.className = 'shown';

  var hidden = document.createElement("INPUT");
  hidden.type = "hidden";
  hidden.value = requestingfor;
  hidden.name = "requestingfor";


  var request_options = get_request_options(requestingfor);
  $.each(request_options, function(key,value){
    var input = document.createElement("LI");
    var text = document.createTextNode(key);
    input.className = "list-group-item";
    input.appendChild(text);

    var div = document.createElement("DIV");
    div.className = "material-switch pull-right";
    var input2 = document.createElement("INPUT");
    input2.id = value;
    input2.name = key;
    input2.type = "checkbox";
    div.appendChild(input2);

    var label = document.createElement("LABEL");
    label.setAttribute("for", value);
    label.className = "label-success"
    div.appendChild(label)

    input.appendChild(div);

    document.getElementById('ticket_options').appendChild(input);

  });
}

const all_statusses = {};
const color_by_status = {};
const colors = {};

const myCharts = {};

function draw_graph(graph_id,canvas_id,data,chartType,filter_type, title){
  var statusses = all_statusses[filter_type];
  filtered_data = data[filter_type];

  var data_lengths = [];
  var label_colors = [];
  var border_color = [];
  var total_count = 0;

  var issue_statusses = statusses;

  statusses.forEach(element => (function(){
    if (!Object.keys(filtered_data).includes(element)){
      issue_statusses = _.without(issue_statusses,element);
    }
    else{
      data_lengths.push(filtered_data[element].length);
      label_colors.push(colors['BACKGROUND'][color_by_status[element]]);
      border_color.push(colors['BORDER'][color_by_status[element]]);

      total_count += filtered_data[element].length;
    }
  })());

  if (!(graph_id in myCharts))
  {
  }

  myCharts[graph_id] = new Chart(canvas_id, {
        type: chartType,
        data: {
            labels: issue_statusses,
            datasets: [{
                data: data_lengths,
                backgroundColor: label_colors,
                borderColor: border_color,
                borderWidth: 1
            }]
        },
        options: {
          scales: {
              y: {
                  beginAtZero: true
              }
          },
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'bottom'
            },
            title: {
              display: true,
              text: 'Application Security'
            }
          },
          'onClick' : function (evt, item) {
            $('#issuesLabel').html('Issues with <b class="state">"'+issue_statusses[item[0]['index']]+'"</b> state');
            $('#issues_body').html('');
            data[filter_type][issue_statusses[item[0]['index']]].forEach(setMsg);

            function setMsg(item, index){
              var JIRA_URL = $('#JIRA_URL').data("name");
              var key = Object.keys(item)[0];
              var value = item[key];
              $('#issues_body').html($('#issues_body').html()+"<br /><a href='"+JIRA_URL+"browse/"+key+"'>"+key+' # '+value+"</a>");
            }
            $('#issues_btn').click();
          }
        }
    });

    myCharts[graph_id].config._config.options.plugins.title.text = title.toUpperCase()+" # "+total_count;
    myCharts[graph_id].update();

    // $('#'+graph_id+'_label').html($('#'+graph_id+'_label').html()+" # "+total_count);
}

function create_graph_for_url(issue_type, assignee, reporter, chartType='pie', filter_type='by_status',review_or_bug='secreviews',since=''){  
  if (chartType == '')
    chartType = 'pie';

  if (review_or_bug == "")
    review_or_bug = "secreviews";

  var title = issue_type+" "+review_or_bug;
  var url = issue_type+'_'+review_or_bug;
  var graph_id = url;

  url = url+"?";

  if (assignee != "")
  {
    url = url+"&assignee="+assignee;
    graph_id = graph_id+"_assigned_me";
    title = title+" assigned to me";
  }

  if (reporter != "")
  {
    url = url+"&reporter="+reporter;
    graph_id = graph_id+"_by_me";
    title = title+" reported by me";
  }

  if (since != "")
  {
    url = url+"&since=-14d";
    graph_id = graph_id+"_2_weeks";
    title = title+" in 2 weeks";
  }

  if(review_or_bug != "")
    url = url+"&review_or_bug="+review_or_bug;

  graph_id = graph_id+"_"+filter_type;

  var graphs = document.getElementById('graphs');
  var childs = graphs.children;

  if(childs.length == 0 || childs[childs.length-1].children.length/3 == 0 )
  {
    var iDiv = document.createElement('div');
    iDiv.className = "row dashboard text-center";
    iDiv.style = "width: 100%";
    graphs.appendChild(iDiv);
    childs = graphs.children;
  }

  child = childs[childs.length-1];

  var childDiv = document.createElement('div');
  childDiv.className = "pad border x400x";
  childDiv.style = "width: 25%; display: inline-block;";

  var canvas = document.createElement('canvas');
  canvas.id = graph_id;
  canvas.style.width = 100;
  canvas.style.height = 100;

  childDiv.appendChild(canvas);
  child.appendChild(childDiv);

  $.ajax({
    'async': false,
    'global': false,
    'url': "/get_tickets/"+url,
    'dataType': "json",
    'beforeSend': function() {
      $(".loader").show();
      showLoader();
    },
    'success': function(data) {
      var canvas = document.getElementById(graph_id);
      const ctx = canvas.getContext('2d');
      draw_graph(graph_id,ctx,data,chartType,filter_type, title);
    },
    'complete': function(data){
      $(".loader").hide();
      hideLoader();
    }
  });
}

function showLoader() {
    $("#loader").css("display", "");
}

function hideLoader() {
    setTimeout(function () {
        $("#loader").css("display", "none");
    }, 1000);
}

$.ajax({
  'async': false,
  'global': false,
  'url': "/ticket_states/",
  'dataType': "json",
  'success': function(data) {
    all_statusses['by_status'] = data['by_status'];
    all_statusses['by_severity'] = data['by_severity'];
    colors['BACKGROUND'] = data.COLOR_CODES['BACKGROUND'];
    colors['BORDER'] = data.COLOR_CODES['BORDER'];
    
    Object.keys(data['STATUS_CODES']).forEach(element => (function(){
      color_by_status[element] = data['STATUS_CODES'][element];
    })());

    // console.log(all_statusses);
  }
});
