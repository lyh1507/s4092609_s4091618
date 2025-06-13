import sqlite3

#Database connection and data retrieval for David dashboard
def create_connection(db_file):
    try:
        return sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(f"❌ Error connecting to database: {e}")
    return None

def get_weather_stations():
    conn = create_connection("climate.db")
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        # If you want to filter for Queensland, uncomment the WHERE clause below
        cursor.execute("""
            SELECT site_id, name, latitude, longitude 
            FROM weather_station
            -- WHERE state_id = 4
            LIMIT 20
        """)
        rows = cursor.fetchall()
        conn.close()
        return rows
    except sqlite3.Error as e:
        print(f"❌ Error fetching station data: {e}")
        return []

def get_page_html(form_data):
    print("About to return David Laid's Urban Planner page...")

    stations = get_weather_stations()

    page_html = """
    <html>
    <head><title>David Laid - Climate Planning</title></head>
    <body>
        <h2>Welcome David Laid (Brisbane City Council)</h2>
        <ul>
            <li> Flood-Risk Map: <a href='#'>View Zones</a></li>
            <li> Heatwave Impact Heatmap: Updated Weekly</li>
            <li> GIS API Integration Enabled</li>
        </ul>
        <p>Use the panel to simulate infrastructure impact and zoning risks.</p>
        <hr>
        <h3>Weather Stations</h3>
        <ul>
    """

    if stations:
        for site_id, name, lat, long in stations:
            page_html += f"<li>{name} (Lat: {lat}, Long: {long})</li>"
    else:
        page_html += "<li>Site ID: 3003 | Name: BROOME AIRPORT | Latitude: -17.9475 | Longitude: 122.2352 | Value1: 1 | Value2: 3</li>"
        page_html += "<li>Site ID: 3032 | Name: DERBY AERO | Latitude: -17.3706 | Longitude: 123.6611 | Value1: 1 | Value2: 4</li>"


    page_html += """
        </ul>
    </body>
    </html>
    """
    return page_html
