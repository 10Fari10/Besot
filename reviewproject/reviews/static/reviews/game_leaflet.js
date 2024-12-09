document.addEventListener('DOMContentLoaded', function() {
    let mapLayoutElement = document.getElementById('map_layout');
    if (mapLayoutElement) {
        let mapLayout = JSON.parse(mapLayoutElement.textContent);
        console.log(mapLayout);

        var map = L.map('map').setView([43.002356, -78.777636], 13); 
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 18 }).addTo(map);
        var startIcon = L.icon({
            iconUrl: "/media/startpin.png", 
            iconSize: [70, 70], 
            iconAnchor: [25, 50]
            
        });

        for (let pinID in mapLayout) {
            let coords = mapLayout[pinID].coords;
            let hint = mapLayout[pinID].hint;
            let markerOptions = {};
            if (pinID === "r1") { 
                markerOptions.icon = startIcon;
            }

            let marker = L.marker(coords, markerOptions).addTo(map);
            marker.bindPopup(`</strong><br>${hint}`);
            marker.on('click', function() {
                selectPin(pinID);
        });
    }
    } else {
        console.error("map_layout element not found.");
    }
});


