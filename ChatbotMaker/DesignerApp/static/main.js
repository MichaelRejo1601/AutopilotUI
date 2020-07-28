var children = document.getElementsByClassName("child");
var parents = document.getElementsByClassName("parent");
var parents_clean = [];
for (i = 0; i < parents.length; i++) {
  cleanParent(parents[i]);
}
for (i = 0; i < children.length; i++) {
  createEnd(children[i]);
}
function cleanParent(item){
  parents_clean.push(item.id.slice(0, -6));
  console.log(parents_clean);
}
function createEnd(item){
  console.log(item.id.slice(0, -5));
  console.log(parents_clean.includes(item.id.slice(0, -5)));
  if (!parents_clean.includes(item.id.slice(0, -5))){
    item.children[0].style.color = "red";
  }
}
function findParent(child) {
    var parent = document.getElementById(child+"parent");
    var current = document.getElementById("indicator");
    if (current != null){
      current.removeAttribute("id");
    }
    if (parent != null){
      parent.parentElement.parentElement.setAttribute('id','indicator');
    }
}
