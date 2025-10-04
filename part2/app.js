// Wells Data Visualization Application
class WellsMap {
    constructor() {
        this.map = null;
        this.vectorSource = null;
        this.popup = null;
        this.overlay = null;
        this.wellsData = [];
        this.stimulatedData = [];
        this.init();
    }

    async init() {
        try {
            await this.loadData();
            this.initMap();
            this.addWellMarkers();
            this.hideLoading();
        } catch (error) {
            console.error('Error initializing map:', error);
            document.getElementById('loading').textContent = 'Error loading data. Please try again.';
        }
    }

    async loadData() {
        try {
            const [wellsResponse, stimulatedResponse] = await Promise.all([
                fetch('api/wells.php'),
                fetch('api/stimulated.php')
            ]);
            
            this.wellsData = await wellsResponse.json();
            this.stimulatedData = await stimulatedResponse.json();
        } catch (error) {
            console.error('Error loading data:', error);
            throw error;
        }
    }

    initMap() {
        // Create popup element
        this.popup = document.createElement('div');
        this.popup.className = 'popup';
        
        this.overlay = new ol.Overlay({
            element: this.popup,
            autoPan: {
                animation: {
                    duration: 250,
                }
            },
        });

        // Create vector source for markers
        this.vectorSource = new ol.source.Vector();

        // Initialize map
        this.map = new ol.Map({
            target: 'map',
            layers: [
                new ol.layer.Tile({
                    source: new ol.source.OSM()
                }),
                new ol.layer.Vector({
                    source: this.vectorSource,
                    style: this.getMarkerStyle.bind(this)
                })
            ],
            overlays: [this.overlay],
            view: new ol.View({
                center: ol.proj.fromLonLat([-103.6, 48.05]),
                zoom: 10
            })
        });

        // Add click handler
        this.map.on('click', this.handleMapClick.bind(this));
    }

    getMarkerStyle(feature) {
        const well = feature.get('wellData');
        let color = '#3498db'; // Default blue
        
        if (well.well_status) {
            switch (well.well_status.toLowerCase()) {
                case 'active':
                    color = '#27ae60'; // Green
                    break;
                case 'inactive':
                    color = '#e74c3c'; // Red
                    break;
                case 'abandoned':
                case 'plugged and abandoned':
                    color = '#95a5a6'; // Gray
                    break;
            }
        }

        return new ol.style.Style({
            image: new ol.style.Circle({
                radius: 8,
                fill: new ol.style.Fill({
                    color: color
                }),
                stroke: new ol.style.Stroke({
                    color: '#ffffff',
                    width: 2
                })
            })
        });
    }

    addWellMarkers() {
        this.wellsData.forEach(well => {
            if (well.lat_long) {
                const coords = this.parseCoordinates(well.lat_long);
                if (coords) {
                    const feature = new ol.Feature({
                        geometry: new ol.geom.Point(ol.proj.fromLonLat([coords.lng, coords.lat])),
                        wellData: well
                    });
                    this.vectorSource.addFeature(feature);
                }
            }
        });
    }

    parseCoordinates(latLongStr) {
        try {
            const parts = latLongStr.split(',');
            if (parts.length === 2) {
                const lat = parseFloat(parts[0].trim());
                const lng = parseFloat(parts[1].trim());
                if (!isNaN(lat) && !isNaN(lng)) {
                    return { lat, lng };
                }
            }
        } catch (error) {
            console.error('Error parsing coordinates:', latLongStr, error);
        }
        return null;
    }

    handleMapClick(event) {
        const feature = this.map.forEachFeatureAtPixel(event.pixel, (feature) => feature);
        
        if (feature) {
            const well = feature.get('wellData');
            this.showPopup(event.coordinate, well);
        } else {
            this.hidePopup();
        }
    }

    showPopup(coordinate, well) {
        const stimulatedInfo = this.stimulatedData.find(s => s.api_no === well.api_no);
        
        this.popup.innerHTML = this.generatePopupContent(well, stimulatedInfo);
        this.overlay.setPosition(coordinate);
    }

    hidePopup() {
        this.overlay.setPosition(undefined);
    }

    generatePopupContent(well, stimulatedInfo) {
        const statusClass = well.well_status ? 
            `status-${well.well_status.toLowerCase().replace(/\s+/g, '-')}` : '';

        return `
            <h3>${well.name || 'Unknown Well'}</h3>
            
            <div class="popup-section">
                <h4>Well Information</h4>
                <div class="popup-row">
                    <span class="popup-label">API No:</span>
                    <span class="popup-value">${well.api_no || 'N/A'}</span>
                </div>
                <div class="popup-row">
                    <span class="popup-label">Status:</span>
                    <span class="popup-value ${statusClass}">${well.well_status || 'N/A'}</span>
                </div>
                <div class="popup-row">
                    <span class="popup-label">Type:</span>
                    <span class="popup-value">${well.well_type || 'N/A'}</span>
                </div>
                <div class="popup-row">
                    <span class="popup-label">Location:</span>
                    <span class="popup-value">${well.closest_city || 'N/A'}</span>
                </div>
                <div class="popup-row">
                    <span class="popup-label">County:</span>
                    <span class="popup-value">${well.county || 'N/A'}</span>
                </div>
            </div>

            <div class="popup-section">
                <h4>Production Data</h4>
                <div class="popup-row">
                    <span class="popup-label">Oil Production:</span>
                    <span class="popup-value">${well.oil_prod || 0} bbls</span>
                </div>
                <div class="popup-row">
                    <span class="popup-label">Gas Production:</span>
                    <span class="popup-value">${well.gas_prod || 0} mcf</span>
                </div>
            </div>

            ${stimulatedInfo ? this.generateStimulatedContent(stimulatedInfo) : ''}
        `;
    }

    generateStimulatedContent(stimulatedInfo) {
        return `
            <div class="popup-section">
                <h4>Stimulation Data</h4>
                <div class="popup-row">
                    <span class="popup-label">Date Stimulated:</span>
                    <span class="popup-value">${stimulatedInfo.date_stimulated || 'N/A'}</span>
                </div>
                <div class="popup-row">
                    <span class="popup-label">Formation:</span>
                    <span class="popup-value">${stimulatedInfo.stimulated_formation || 'N/A'}</span>
                </div>
                <div class="popup-row">
                    <span class="popup-label">Stages:</span>
                    <span class="popup-value">${stimulatedInfo.stimulation_stages || 'N/A'}</span>
                </div>
                <div class="popup-row">
                    <span class="popup-label">Volume:</span>
                    <span class="popup-value">${stimulatedInfo.volume || 'N/A'} ${stimulatedInfo.volume_units || ''}</span>
                </div>
                <div class="popup-row">
                    <span class="popup-label">Treatment Type:</span>
                    <span class="popup-value">${stimulatedInfo.type_treatment || 'N/A'}</span>
                </div>
                <div class="popup-row">
                    <span class="popup-label">Max Pressure:</span>
                    <span class="popup-value">${stimulatedInfo.maximum_treatment_pressure_psi || 'N/A'} psi</span>
                </div>
            </div>
        `;
    }

    hideLoading() {
        document.getElementById('loading').style.display = 'none';
        document.getElementById('mapContainer').style.display = 'block';
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new WellsMap();
});