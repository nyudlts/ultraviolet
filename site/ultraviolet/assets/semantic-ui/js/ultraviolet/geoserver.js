import L from "leaflet"
import "leaflet/dist/leaflet.css";

const populateAttributeTable = (data) => {
    const attributesElement = document.getElementById("attributes");
    attributesElement.innerHTML = '';

    Object.keys(data.properties).sort().forEach(property => {
        const nameTd = document.createElement('td');
        nameTd.textContent = property
        const typeTd = document.createElement("td")
        typeTd.textContent = data.properties[property]

        const tr = document.createElement("tr")
        tr.appendChild(nameTd)
        tr.appendChild(typeTd)
        attributesElement.appendChild(tr)
    })
}

const describeFeatureType = (wfsUrl, layerNames) => {
    const attributesElement = document.getElementById("attributes");

    const formData = new FormData();
    formData.append("url", wfsUrl);
    formData.append("layers", layerNames);

    fetch("/geoserver/describe_feature_type", {
        method: "POST", body: formData
    })
        .then(response => response.json())
        .then(data => {
            const attributes = data.featureTypes[0].properties.sort((a, b) => {
                return a.name.localeCompare(b.name)
            })

            attributes.forEach(attribute => {
                const nameTd = document.createElement('td');
                nameTd.textContent = attribute.name
                const typeTd = document.createElement("td")
                typeTd.textContent = attribute.localType

                const tr = document.createElement("tr")
                tr.appendChild(nameTd)
                tr.appendChild(typeTd)
                attributesElement.appendChild(tr)
            })
        })
        .catch(error => {
            console.error('Error:', error);
        });
};

const addInspection = (map, url, layerId) => {
    map.on("click", async (e) => {
        const attributesElement = document.getElementById("attributes");
        attributesElement.innerHTML = '<tr><td colspan="2">Loading...</td>';

        const wmsoptions = {
            url: url,
            layers: layerId,
            bbox: map.getBounds().toBBoxString(),
            width: Math.round(document.getElementById("map").clientWidth),
            height: Math.round(document.getElementById("map").clientHeight),
            query_layers: layerId,
            x: Math.round(e.containerPoint.x),
            y: Math.round(e.containerPoint.y),
        };

        try {
            const response = await fetch("/geoserver/get_feature_info", {
                method: "POST", headers: {
                    "Content-Type": "application/json",
                }, body: JSON.stringify(wmsoptions),
            });

            if (!response.ok) throw new Error("Network response was not ok.");

            const response_data = await response.json();

            if (response_data.hasOwnProperty("error") || response_data.hasOwnProperty('exceptions') || response_data.features.length === 0) {
                const attributesElement = document.getElementById("attributes");
                attributesElement.innerHTML = '<tr><td colspan="2">No feature found</td>';

                return;
            }
            const data = response_data.features[0];

            populateAttributeTable(data);
        } catch (error) {
            console.error("Fetch error: ", error);
        }
    });
}

document.addEventListener("DOMContentLoaded", async () => {
    const mapElement = document.getElementById("map");
    const preview = mapElement.getAttribute("data-preview");
    const bounds = mapElement.getAttribute("data-bounds")

    const map = L.map('map').setView([0, 0], 13);

    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{retina}.png', {
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="http://carto.com/attributions">Carto</a>',
        maxZoom: 18,
        worldCopyJump: true,
        retina: "@2x",
    }).addTo(map);

    if (preview === "True") {
        const baseUrl = mapElement.getAttribute("data-wms-url")
        const layerName = mapElement.getAttribute("data-layer-name")

        const wmsLayer = L.tileLayer.wms(baseUrl, {
            layers: layerName,
            format: 'image/png',
            transparent: true,
            opacity: 0.75
        });

        wmsLayer.addTo(map);
        wmsLayer.setOpacity(0.75);

        const attributesElement = document.getElementById("attributes");
        const wfsUrl = attributesElement.getAttribute("data-wfs-url");
        const layerNames = attributesElement.getAttribute("data-layer-names");

        addInspection(map, wfsUrl, layerNames);
        describeFeatureType(wfsUrl, layerNames, attributesElement);
    }

    const regex = /ENVELOPE\(([-\d.]+), ([-\d.]+), ([-\d.]+), ([-\d.]+)\)/;
    const match = bounds.match(regex);

    if (match) {
        const minLon = parseFloat(match[1]);
        const maxLon = parseFloat(match[2]);
        const minLat = parseFloat(match[3]);
        const maxLat = parseFloat(match[4]);

        const bounds = [[minLat, minLon], [maxLat, maxLon]];

        map.fitBounds(bounds);

        if (preview === "False") {
            map.addLayer(L.rectangle(bounds, {color: "#3388FF", weight: 3}));
        }
    }
});
