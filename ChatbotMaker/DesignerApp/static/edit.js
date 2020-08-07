// var schem = {
//   "say":{
//     "say-text":{
//       "required":true
//     }
//   },
//   "play":{
//     "url":{
//
//     }
//   },
//   "listen":{
//     "tasks":[
//
//     ]
//   },
//
// }
var bstring = ''
var bobj = {}
var barray = []
function clean(obj, bstring, bobj, barray){
  var new_obj = obj;
  if (Array.isArray(new_obj)){
    for (atr in new_obj){
      if (new_obj[atr] == bstring){
        delete new_obj[atr]
      }
      else {
        new_obj[atr] = clean(new_obj[atr], bstring, bobj, barray)
      }
    }
  }
  else if (typeof new_obj == 'object'){
    for (atr in new_obj){
      if (new_obj[atr] == bstring){
        delete new_obj[atr]
      }
      else {
        new_obj[atr] = clean(new_obj[atr], bstring, bobj, barray)
      }
    }
  }
  else{
  }
  for(atr in new_obj){
    if (JSON.stringify(new_obj[atr]) == JSON.stringify(bobj)){
          delete new_obj[atr];
        }
    try {
      new_obj[atr] = new_obj[atr].filter(function( element ) {
            return element !== undefined;
          });
    }
    catch(err) {

    }
    if (Array.isArray(new_obj[atr])){
      if(JSON.stringify(new_obj[atr]) == JSON.stringify(barray)){
        delete new_obj[atr];
      }
    }
  }
  return new_obj;
}
function createJSON(){
  // var list = document.getElementsByTagName("fieldset");
  // var obj = {};
  // console.log(list);
  // console.log(list[0].name);
  // obj[list[0].name] = schem[list[0].name]
  // for (input in list[0].innerHTML.getElementsByTagName("input"))
  // console.log(obj)
  var obj = $("#actions-form").serializeObject();
  var token = obj.csrfmiddlewaretoken
  delete obj.csrfmiddlewaretoken
  if(JSON.stringify(clean(obj["actions"][document.getElementById("tasks").name.match(/(\d+)/)[0]]["listen"], bstring, bobj, barray)) == JSON.stringify(bobj)){
    obj["actions"][1]["listen"] = true;
  }
  obj = clean(obj, bstring, bobj, barray);
  console.log(obj);
  $.post(window.location.href, {data:JSON.stringify(obj),csrfmiddlewaretoken:token})
}
function callBack(data) {
      // If the $.post was successful
      success: function suc(data) {
          // do stuff
          console.log(data); // returned from your endpoint
      }
}
$('#menu').toggle(false);
$(document).ready(function(){
      $("#add-listen").click(function(){
          $("#listen").append("<input type='text' id='tasks' name='actions["+ document.getElementById("tasks").name.match(/(\d+)/)[0] +"][listen][tasks][]' placeholder='task-x'/>");
      });
      $(document).on("click", "#tasks" , function() {
          $(this).remove();
      });
      $(document).on("click", "#action" , function() {
          $(this).parent().remove();
      });
      $(document).on("click", "#new-action" , function() {
          $('#menu').toggle();
          $("#add-action").toggleClass('rotate');
          var arr = [];
          var list = document.getElementsByClassName('inline-form');
          for (i = 0; i < list.length; i++){
            arr.push(list[i].id);
          }
          arr.push($(this).html())
          console.log(arr)
          var obj = $("#actions-form").serializeObject();
          var token = obj.csrfmiddlewaretoken
          $.get(window.location.href, {new_array:JSON.stringify({"arr":arr}),csrfmiddlewaretoken:token}, 'html')
      });
      $("#add-action").on('click', function() {
        $('#menu').toggle();
        $("#add-action").toggleClass('rotate');
      });
  });
