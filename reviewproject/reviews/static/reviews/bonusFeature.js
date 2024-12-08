const holder=[];
function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(store_n_pop);
  }
}

function store_n_pop(point) { 
  holder.push(point.coords.latitude,point.coords.longitude);
}

var change=document.getElementById("val");
var t_range=document.getElementById("time").oninput=function(){
  change.innerHTML=this.value;
}
document.getElementById('timeform').addEventListener('submit', t_submit);

async function t_submit(event) {
event.preventDefault();
if(holder.length==0 || holder.length==1){
  console.log(holder)
alert("Error no location found");

}
else{
  const lat =holder[0];
  const long = holder[1];
  const time=document.getElementById("time").value;
  
  document.getElementById("timeToSend").value = time
  document.getElementById("latVal").value = lat
  document.getElementById("longVal").value = long

}
timePopDown()
}

function timePopDown(){
  document.getElementById("addLoco").style.display="none";
  }

function timePopUp(){
  document.getElementById("addLoco").style.display="block";
  }

getLocation();