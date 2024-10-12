var map = L.map('map').setView([43.0001, -78.7865], 15)


L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);
//pin function
function x_marks_the_spot(x) {
    var marker = L.marker([x.latlng.lat,x.latlng.lng]).addTo(map);
    document.getElementById("addPost").style.display="block";   

}

map.on('click', x_marks_the_spot);