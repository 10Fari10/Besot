const postButton='<button id="anotherPost">Add Post</button>';
var map = L.map('map').setView([43.0001, -78.7865], 15)


L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);
//pin function
function x_marks_the_spot(x) {
    var marker = L.marker([x.latlng.lat,x.latlng.lng]).addTo(map).bindPopup(postButton);
    document.getElementById("addPost").style.display="block";  
    marker.on("popupopen",extraPost); 
}

map.on('click', x_marks_the_spot);
  //popDown fuction-click the 'x' for the post form to dissappear
  
  document.getElementById("closePop").addEventListener("click", popDown);
  function popDown(){
  document.getElementById("addPost").style.display="none";
  }
  //post through pin
  function extraPost(){
  document.getElementById("addPost").style.display="none";
  }