import sqlite3

def create_connection(db_file):
    try:
        return sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return None

def get_station_data():
    conn = create_connection("climate.db")
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name, latitude, longitude 
            FROM weather_station 
            WHERE state_id = 1  -- NSW stations
            LIMIT 5
        """)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"❌ Query error: {e}")
        return []
    finally:
        conn.close()

def get_page_html(form_data):
    stations = get_station_data()
    
    return f"""
    <div class="dashboard-content">
        <div class="card">
            <h2>Allen Donald's Farm Dashboard</h2>
            
            <div class="alert-box positive">
                <span class="icon"></span> 
                <strong>Optimal irrigation time:</strong> 6am to 8am tomorrow
            </div>
            
            <div class="data-grid">
                <div class="data-card">
                    <h3>Rainfall Forecast</h3>
                    <p>Next 7 days: 12mm expected</p>
                    <p class="trend-down">15% less than average</p>
                </div>
                
                <div class="data-card">
                    <h3>Frost Alerts</h3>
                    <p>Expected in 3 days</p>
                    <p class="alert">Prepare protection measures</p>
                </div>
                
                <div class="data-card">
                    <h3>Temperature Range</h3>
                    <p>Min: 8 degrees celcius | Max: 22 degrees celcius</p>
                    <p>Ideal for winter crops</p>
                </div>
            </div>
            
            <div class="data-section">
                <h3>NSW Weather Stations</h3>
                <ul class="station-list">
                    {"".join(
                        f'<li><strong>{name}</strong> (Lat: {lat}, Long: {lon})</li>'
                        for name, lat, lon in stations
                    ) if stations else "<li class='no-data'>No station data available</li>"}
                </ul>
            </div>
            
            <div class="alert-box">
                <span class="icon"></span> 
                <strong>Long-Term Trend:</strong> 2025 likely 8% drier than 2024
            </div>
        </div>
    </div>
    """