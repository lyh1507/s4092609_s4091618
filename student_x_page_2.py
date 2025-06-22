import sqlite3

def create_connection(db_file):
    try:
        return sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return None

def get_queensland_stations():
    conn = create_connection("climate.db")
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name, latitude, longitude 
            FROM weather_station 
            WHERE state_id = 4  -- Queensland
            LIMIT 5
        """)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"❌ Query error: {e}")
        return []
    finally:
        conn.close()

def get_page_html(form_data):
    stations = get_queensland_stations()
    
    return f"""
    <div class="dashboard-content">
        <div class="card">
            <h2>Brisbane Urban Planning</h2>
            
            <div class="button-group">
                <button class="btn action-btn" id="flood-map-btn" data-target="flood-map-container">
                    View Flood Zones
                </button>
                
                <button class="btn action-btn" onclick="alert('Heatwave analysis started... This would show detailed heat data.');">
                    Analyze Heatwaves
                </button>
            </div>
            
            <!-- Flood Map Container -->
            <div id="flood-map-container" class="tool-container" style="display:none;">
                <h3>Flood Risk Map</h3>
                <img src="/flood-map.png" alt="Brisbane Flood Zones" class="map-img">
                <div class="map-legend">
                    <div class="legend-item high-risk">High Risk</div>
                    <div class="legend-item medium-risk">Medium Risk</div>
                    <div class="legend-item low-risk">Low Risk</div>
                </div>
            </div>
            
            <!-- Weather Stations -->
            <div class="data-section">
                <h3>Queensland Weather Stations</h3>
                <ul class="station-list">
                    {"".join(
                        f'<li><strong>{name}</strong> (Lat: {lat}, Long: {lon})</li>'
                        for name, lat, lon in stations
                    ) if stations else "<li class='no-data'>No station data available</li>"}
                </ul>
            </div>
        </div>
    </div>
    """