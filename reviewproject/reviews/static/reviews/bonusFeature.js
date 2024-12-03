const holder=[];
function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(store_n_pop);
  }
}

function store_n_pop(point) {
  
  
  holder.push(point.coords.latitude,point.coords.longitude);
  document.getElementById("addLoco").style.display="block";

 
  
}

var change=document.getElementById("val");
var t_range=document.getElementById("time").oninput=function(){
  change.innerHTML=this.value;
}

getLocation();