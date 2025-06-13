import sqlite3

#database connection and data retrieval for Scout Mollun's
def create_connection(db_file):
    try:
        return sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(f"❌ Error connecting to database: {e}")
    return None

def get_station_data():
    conn = create_connection("climate.db")  # Ensure this file is in the project root
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT site_id, name, latitude, longitude FROM weather_station LIMIT 20")
        rows = cursor.fetchall()
        conn.close()
        return rows
    except sqlite3.Error as e:
        print(f"❌ Error fetching station data: {e}")
        return []

def get_page_html(form_data):
    print("About to return Scout Mollun's Activist page...")

    stations = get_station_data()

    page_html = """
    <html>
    <head><title>Scout Mollun - Climate Activism Hub</title></head>
    <body>
        <h2>Welcome Scout Mollun</h2>
        <ul>
            <li> Draft a Petition: <a href='#'>Launch Tool</a></li>
            <li> Local Alerts: New flood warning in QLD</li>
            <li> Downloadable Climate Infographics</li>
        </ul>
        <p>Use these tools to mobilize awareness and pressure policy change.</p>
        <hr>
        <h3>Weather Stations</h3>
        <ul>
    """

    if stations:
        for site_id, name, lat, lon in stations:
            page_html += f"<li>{name} (Lat: {lat}, Long: {lon})</li>"
    else:
        page_html += "<li>Site ID: 4019 | Name: MANDORA | Latitude: -19.7419 | Longitude: 120.8433 | Value1: 1 | Value2: 3</li>"
        page_html += "<li>Site ID: 4032 | Name: PORT HEDLAND AIRPORT | Latitude: -20.3725 | Longitude: 118.6317 | Value1: 1 | Value2: 5</li>"

    page_html += """
        </ul>
    </body>
    </html>
    """
    return page_html
