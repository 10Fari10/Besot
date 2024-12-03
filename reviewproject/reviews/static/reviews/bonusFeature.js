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
document.getElementById('timeform').addEventListener('submit', t_submit);

async function t_submit(event) {
if(holder.length==0 || holder.length==1){
alert("Error no location found");

}
else{
  const lat =holder[0];
  const long = holder[1];
  const time=document.getElementById(time).value;
  const data_to_send = {
    latVal: lat,
    longVal: long,
    duration:time,
};
send(data_to_send);
}
}

async function send(data_to_send) {
  try {
      const response = await fetch('/map_post/', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': CSRF_TOKEN
          },
          body: JSON.stringify(data_to_send)
      });
      
      if (response.ok) {
          const sent_data = await response.json();
          console.log("Location pinned to map", sent_data);
          /*there should be a function here to fetch the location pins like the fetch function for review pins
           but I don't remember if these pins will be sent to the same db w/ review pin or will be stored and handled differently
          */
          document.getElementById("addLoco").style.display="none"; 
      } else {
          alert("Failed to pin your location");
          document.getElementById("addLoco").style.display="none"; 
      }
  } catch (error) {
      console.error("ERROR:", error);
      alert("An error occurred while pinning your location");
      document.getElementById("addLoco").style.display="none";
  }
}

getLocation();