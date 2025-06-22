import sqlite3

def create_connection(db_file):
    try:
        return sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

def get_station_data():
    conn = create_connection("climate.db")
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name, latitude, longitude FROM weather_station LIMIT 5")
        return cursor.fetchall()
    finally:
        conn.close()

def get_page_html(form_data):
    stations = get_station_data()
    
    return f"""
    <html>
    <head>
        <title>Sarah's Dashboard</title>
        <link rel="stylesheet" href="/style.css">
        <script>
            function refreshData() {{
                window.location.href = '/sarah?refresh=' + new Date().getTime();
            }}
            function showDetails(station) {{
                alert('Loading detailed data for: ' + station);
                // Implement actual detail loading here
            }}
        </script>
    </head>
    <body>
        <nav class="navbar">
            <a href="/sarah" class="nav-link active">Sarah's Dashboard</a>
            <a href="/david" class="nav-link">David's Planner</a>
        </nav>
        <div class="container">
            <div class="card">
                <h2>NSW Riverina Farm Analysis</h2>
                <div class="dashboard">
                    <div class="status-indicators">
                        <p>Drought Risk: <span class="status status-danger">High</span></p>
                        <p>Soil Moisture: <span class="status status-warning">29%</span></p>
                    </div>
                    <button onclick="refreshData()" class="btn">Refresh Data</button>
                </div>
                
                <h3>Nearby Weather Stations</h3>
                <ul class="station-list">
                    {"".join(
                        f'<li onclick="showDetails(\'{name}\')">{name} (Lat: {lat}, Long: {lon})</li>'
                        for name, lat, lon in stations
                    ) if stations else "<li>No station data available</li>"}
                </ul>
            </div>
        </div>
    </body>
    </html>
    """