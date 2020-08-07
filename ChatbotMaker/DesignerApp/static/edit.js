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
        console.log(delete new_obj[atr]);
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
  delete obj.csrfmiddlewaretoken;
  if(JSON.stringify(clean(obj["listen"], bstring, bobj, barray)) == JSON.stringify(bobj))
  {
    obj["listen"] = true;
  }
  obj = clean(obj, bstring, bobj, barray)
  console.log(obj);
  console.log(JSON.stringify(obj));
}
