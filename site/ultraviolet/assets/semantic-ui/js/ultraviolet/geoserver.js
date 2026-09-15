import L from "leaflet"
import "leaflet/dist/leaflet.css";

const populateAttributeTable = (features) => {
    const featuresElement = document.getElementById("features");
    featuresElement.innerHTML = '';

    features.forEach(feature => {
        const featureHeader = document.createElement("h4");
        featureHeader.textContent = `${feature.id} (${feature.geometry.type})`;

        const table = document.createElement("table");
        table.className = "ui unstackable very compact table striped selectable";

        const tableHead = document.createElement("thead");
        table.appendChild(tableHead);
        const attributeHeader = document.createElement("th");
        attributeHeader.textContent = "Attribute";
        const valueHeader = document.createElement("th");
        valueHeader.textContent = "Value";
        const headerRow = document.createElement("tr");
        headerRow.appendChild(attributeHeader);
        headerRow.appendChild(valueHeader);
        tableHead.appendChild(headerRow);

        const tableBody = document.createElement("tbody")
        table.appendChild(tableBody)

        Object.keys(feature.properties).sort().forEach(key => {
            const nameTd = document.createElement('td');
            nameTd.textContent = key
            const typeTd = document.createElement("td")
            typeTd.textContent = feature.properties[key]

            const tr = document.createElement("tr")
            tr.appendChild(nameTd)
            tr.appendChild(typeTd)

            tableBody.appendChild(tr)
        })

        featuresElement.appendChild(featureHeader)
        featuresElement.appendChild(table);
    })
}

const addFeatureInspectionHandler = (map, url, layerNames) => {
    map.on("click", async (e) => {
        const featuresElement = document.getElementById("features");
        featuresElement.innerHTML = '<p>Loading...</p>';

        try {
            const response = await fetch("/geoserver/get_feature_info", {
                method: "POST", headers: {
                    "Content-Type": "application/json",
                }, body: JSON.stringify({
                    url: url,
                    layers: layerNames,
                    bbox: map.getBounds().toBBoxString(),
                    width: Math.round(document.getElementById("map").clientWidth),
                    height: Math.round(document.getElementById("map").clientHeight),
                    query_layers: layerNames,
                    x: Math.round(e.containerPoint.x),
                    y: Math.round(e.containerPoint.y),
                }),
            });

            if (!response.ok) throw new Error("Network response was not ok.");

            const response_data = await response.json();

            if (response_data.hasOwnProperty("error") || response_data.hasOwnProperty('exceptions') || response_data.features.length === 0) {
                const featuresElement = document.getElementById("features");
                featuresElement.innerHTML = '<tr><td colspan="2">No feature found</td>';

                return;
            }

            console.log(response_data);
            populateAttributeTable(response_data.features);
        } catch (error) {
            console.error("Fetch error: ", error);
        }
    });
}

const zoomMapToBoundingBox = (map) => {
    const mapElement = document.getElementById("map");
    const preview = mapElement.getAttribute("data-preview");
    const bounds = mapElement.getAttribute("data-bounds")

    const regex = /ENVELOPE\(([-\d.]+), ([-\d.]+), ([-\d.]+), ([-\d.]+)\)/;
    const match = bounds.match(regex);

    if (match) {
        let [_, minLon, maxLon, minLat, maxLat] = match;

        const bounds = [[minLat, minLon], [maxLat, maxLon]];

        map.fitBounds(bounds);

        if (preview === "False") {
            map.addLayer(L.rectangle(bounds, {color: "#3388FF", weight: 3}));
        }
    }
};

const addWmsLayer = (map) => {
    const mapElement = document.getElementById("map");
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
};

const addWfsInspection = map => {
    const mapElement = document.getElementById("map");

    if (mapElement) {
        const wmsUrl = mapElement.getAttribute("data-wms-url");
        const layerNames = mapElement.getAttribute("data-layer-name");

        addFeatureInspectionHandler(map, wmsUrl, layerNames);
    }
};

document.addEventListener("DOMContentLoaded", async () => {
    const mapElement = document.getElementById("map");

    if (mapElement) {
        const preview = mapElement.getAttribute("data-preview");

        const map = L.map('map').setView([0, 0], 13);

        L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{retina}.png?key=cb1_2hc3_1_1a81f66c5d346d83ee13dbbd', {
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="http://carto.com/attributions">Carto</a>',
            maxZoom: 18,
            worldCopyJump: true,
            retina: "@2x",
        }).addTo(map);

        if (preview === "True") {
            addWmsLayer(map);
            addWfsInspection(map);
        }

        zoomMapToBoundingBox(map);
    }
});
