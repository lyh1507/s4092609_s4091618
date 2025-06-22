import sqlite3

def create_connection(db_file):
    """Create a database connection to the SQLite database"""
    try:
        return sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(f"❌ Database connection error: {e}")
        return None

def get_station_data():
    """Query Western Australia weather stations from the database"""
    conn = create_connection("climate.db")
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name, latitude, longitude 
            FROM weather_station 
            WHERE state_id = 6  -- Western Australia
            LIMIT 5
        """)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"❌ Database query error: {e}")
        return []
    finally:
        conn.close()

def get_page_html(form_data):
    """Generate HTML content for Scout's Activist Hub"""
    stations = get_station_data()
    
    return f"""
    <div class="dashboard-content">
        <div class="card">
            <h2><span class="icon"></span> Climate Activism Hub</h2>
            
            <div class="button-group">
                <button class="btn action-btn" data-target="petition-tool">
                    <span class="icon"></span> Draft Petition
                </button>
                
                <button class="btn action-btn" data-target="infographics">
                    <span class="icon"></span> View Infographics
                </button>
            </div>
            
            <!-- Petition Tool (hidden by default) -->
            <div id="petition-tool" class="tool-container" style="display:none;">
                <h3>Petition Builder</h3>
                <textarea class="petition-textarea" 
                          placeholder="Enter your climate petition text here..."></textarea>
                <button class="btn submit-btn">
                    <span class="icon"></span> Publish Petition
                </button>
            </div>
            
            <!-- Infographics (hidden by default) -->
            <div id="infographics" class="tool-container" style="display:none;">
                <h3>Climate Change Infographics</h3>
                <img src="/climate-infographic.png" 
                     alt="Climate Data Visualizations" 
                     class="infographic-img">
                <a href="/climate-infographic.png" 
                   download 
                   class="btn download-btn">
                    <span class="icon"></span> Download Infographic
                </a>
            </div>
            
            <!-- Weather Stations Data -->
            <div class="data-section">
                <h3><span class="icon"></span> Western Australia Weather Stations</h3>
                <ul class="station-list">
                    {"".join(
                        f'<li><strong>{name}</strong> (Lat: {lat}, Long: {lon})</li>'
                        for name, lat, lon in stations
                    ) if stations else "<li class='no-data'>No station data available</li>"}
                </ul>
            </div>
            
            <!-- Alert Box -->
            <div class="alert-box">
                <span class="icon"></span> 
                <strong>Local Alert:</strong> New flood warning for Queensland coastal areas
            </div>
        </div>
    </div>
    """