

var map = L.map('map').setView([43.0001, -78.7865], 15);

// Add OpenStreetMap tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);


function fetchPinsAndReviews() {
    fetch('/pins/', {
        method: "GET",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': CSRF_TOKEN
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("ERROR!");
        }
        return response.json(); 
    })
    .then(data => {
        if (data.pins) {
            data.pins.forEach(pin => {
             marker = L.marker([pin.lat, pin.long]).addTo(map)
             .bindPopup(`
                <div>
                    <button id="viewReviewsButton" onclick="viewReviews(${pin.lat}, ${pin.long})">View Reviews</button>
                    <button id="addReviewButton" onclick = "addReview(${pin.lat}, ${pin.long})">Add Review</button>
                </div>
                `);
                if(pin.expire!=null){
                    marker._icon.style.filter = "hue-rotate(120deg)"
                }
            });
        }
    });
}
        

var marker;

function x_marks_the_spot(x) {
    const lat = x.latlng.lat; 
    const long = x.latlng.lng; 
   
    document.getElementById('latVal').value = lat; 
    document.getElementById('longVal').value = long; 
    document.getElementById("addPost").style.display = "block";    
}

function viewReviews(lat, long) {
    const dynamicContainer = document.getElementById("revcontainer");
    dynamicContainer.innerHTML = "";  
    pasteReviews(lat, long); 
}
function addReview(lat, long) {
    document.getElementById('latVal').value = lat; 
    document.getElementById('longVal').value = long; 
    document.getElementById("event").style.display="none";
    document.getElementById("addPost").style.display = "block";    
}

document.addEventListener('DOMContentLoaded', fetchPinsAndReviews);

map.on('click', x_marks_the_spot);
