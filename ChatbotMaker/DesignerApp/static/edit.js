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
function clean(obj, bstring, bobj, barray){
  var new_obj = obj;
  if (Array.isArray(new_obj)){
    console.log("Parsing Array");
    for (atr in new_obj){
      if (new_obj[atr] == bstring){
        console.log("Deleting String")
        delete new_obj[atr]
      }
      else {
        new_obj[atr] = clean(new_obj[atr], bstring, bobj, barray)
      }
    }
  }
  else if (typeof new_obj == 'object'){
    console.log("Parsing Object");
    for (atr in new_obj){
      if (new_obj[atr] == bstring){
        console.log("Deleting String")
        delete new_obj[atr]
      }
      else {
        new_obj[atr] = clean(new_obj[atr], bstring, bobj, barray)
      }
      if (JSON.stringify(new_obj[atr]) == JSON.stringify(bobj)){
          console.log(delete new_obj[atr]);
        }
    }
  }
  else{
    console.log("not object or array")
  }
  try {
    new_obj = new_obj.filter(function( element ) {
          return element !== undefined;
        });
  }
  catch(err) {

  }
  for(atr in new_obj){
    if (JSON.stringify(new_obj[atr]) == JSON.stringify(bobj)){
          console.log(delete new_obj[atr]);
        }
    try {
      new_obj = new_obj.filter(function( element ) {
            return element !== undefined;
          });
    }
    catch(err) {

    }
    if (Array.isArray(new_obj[atr])){
      if(JSON.stringify(new_obj[atr] == JSON.stringify(barray)))
        console.log(delete new_obj[atr]);
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
  console.log(obj);
  var string = $("#actions-form").serializeJSON();
  console.log(string);
}
