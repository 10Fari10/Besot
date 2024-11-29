

function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(submit);
  } 
}

function submit(position) {
  elem.innerHTML = "Latitude: " + position.coords.latitude + 
  "<br>Longitude: " + position.coords.longitude;
}
getLocation();