var map = L.map('map').setView([43.0001, -78.7865], 15)


L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);
//pin function

//var marker;

function x_marks_the_spot(x) {
    const lat = x.latlng.lat; 
    const long = x.latlng.lng; 
    var marker = L.marker([lat,long]).addTo(map).bindPopup("<button>Add Post</button>");
    document.getElementById('latVal').value = lat; 
    document.getElementById('longVal').value = long; 
    document.getElementById("addPost").style.display="block";    

    
}
map.on('click', x_marks_the_spot);

//code for when submission works this is so if someone clicks 'x' button a pin cannot be make to prevent empty pins
//commented out to show pin function does work
/*document.getElementById("closePop").addEventListener("click", popDown);
  function popDown(){
  document.getElementById("addPost").style.display="none";
  map.removeLayer(marker);
  }*/