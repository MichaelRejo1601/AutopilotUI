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
// var arr = [];
// var listen_index;
//
// var bstring = ''
// var bobj = {}
// var barray = []
// function clean(obj, bstring, bobj, barray){
//   var new_obj = obj;
//   if (Array.isArray(new_obj)){
//     for (atr in new_obj){
//       if (new_obj[atr] == bstring){
//         delete new_obj[atr]
//       }
//       else {
//         new_obj[atr] = clean(new_obj[atr], bstring, bobj, barray)
//       }
//     }
//   }
//   else if (typeof new_obj == 'object'){
//     for (atr in new_obj){
//       if (new_obj[atr] == bstring){
//         delete new_obj[atr]
//       }
//       else {
//         new_obj[atr] = clean(new_obj[atr], bstring, bobj, barray)
//       }
//     }
//   }
//   else{
//   }
//   for(atr in new_obj){
//     if (JSON.stringify(new_obj[atr]) == JSON.stringify(bobj)){
//           delete new_obj[atr];
//         }
//     try {
//       new_obj[atr] = new_obj[atr].filter(function( element ) {
//             return element !== undefined;
//           });
//     }
//     catch(err) {
//
//     }
//     if (Array.isArray(new_obj[atr])){
//       if(JSON.stringify(new_obj[atr]) == JSON.stringify(barray)){
//         delete new_obj[atr];
//       }
//     }
//   }
//   return new_obj;
// }
// function updateArr(obj){
//   arr = [];
//   var list = document.getElementsByClassName('panel');
//   for (i = 0; i < list.length; i++){
//     arr.push(list[i].id);
//   }
//   if(arr.includes('listen')){
//     listen_index = document.getElementById("tasks").name.match(/(\d+)/)[0]
//     console.log(listen_index)
//     if(JSON.stringify(clean(obj["actions"][listen_index]["listen"], bstring, bobj, barray)) == JSON.stringify(bobj)){
//       obj["actions"][arr.indexOf('listen')]["listen"] = true;
//     }
//   }
//   return obj
// }
// function createJSON(){
//   // var list = document.getElementsByTagName("fieldset");
//   // var obj = {};
//   // console.log(list);
//   // console.log(list[0].name);
//   // obj[list[0].name] = schem[list[0].name]
//   // for (input in list[0].innerHTML.getElementsByTagName("input"))
//   // console.log(obj)
//   var obj = $('.form-horizontal').serializeObject();
//   var token = obj.csrfmiddlewaretoken;
//   delete obj.csrfmiddlewaretoken;
//   obj = updateArr(obj);
//   console.log(obj)
//   obj = clean(obj, bstring, bobj, barray);
//   console.log(obj);
//   $.post(window.location.href, {new_array:JSON.stringify({"arr":arr}),data:JSON.stringify(obj),csrfmiddlewaretoken:token}, function (data) {
//       window.location.reload()//add error here
//   }, "html")
// }

// $('#menu').toggle(false);
// $(document).ready(function(){
//       $(document).on("click", "#add-listen", function(){
//           $("#listen").append("<input type='text' id='tasks' name='actions["+ listen_index +"][listen][tasks][]' placeholder='task-x'/>");
//       });
//       $(document).on("dblclick", "#tasks" , function() {
//           $(this).remove();
//       });
//       $(document).on("click", "#action" , function() {
//           $(this).parent().remove();
//       });
//       $(document).on("click", "#new-action" , function() {
//           $('#menu').toggle();
//           $("#add-action").toggleClass('rotate');
//           var obj = $('.form-horizontal').serializeObject();
//           obj = updateArr(obj);
//           arr.push($(this).html())
//           console.log(arr)
//           var token = obj.csrfmiddlewaretoken;
//           var datos = {new_array:JSON.stringify({"arr":arr}),csrfmiddlewaretoken:token}
//           $.ajax({
//             url: window.location.href,
//             type: "POST",
//             dataType: "html",
//             data: datos,
//             success: function (data) {
//                 $("html").html(data);
//             }
//           });
//         });
//       $("#add-action").on('click', function() {
//         $('#menu').toggle();
//         $("#add-action").toggleClass('rotate');
//       });
//   });
