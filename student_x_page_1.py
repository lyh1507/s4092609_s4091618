import sqlite3

#Database connection and data retrieval for Sarah Chen's dashboard
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
        # You can add a WHERE clause if you want to filter for NSW region specifically
        cursor.execute("SELECT site_id, name, latitude, longitude FROM weather_station LIMIT 20")
        rows = cursor.fetchall()
        conn.close()
        return rows
    except sqlite3.Error as e:
        print(f"❌ Error fetching station data: {e}")
        return []


def get_page_html(form_data):
    print("Landing page dashboard...")

    stations = get_station_data()

    page_html = """
    <html>
    <head><title>Sarah Chen - Farmer Dashboard</title></head>
    <body>
        <h2>Welcome Sarah Chen (NSW Riverina)</h2>
        <ul>
            <li> Real-time Drought Risk: <b>High</b></li>
            <li> Soil Moisture Levels: <b>North Field 29%</b>, South 41%</li>
            <li> Irrigation Alert: Rain forecast tomorrow (delay watering)</li>
            <li> Frost Risk: Low</li>
        </ul>
        <p>Use the dashboard to adjust water scheduling and monitor field zones.</p>
        <hr>
        <h3>Weather Stations</h3>
        <ul>
    """
##Station information
    if stations:
        for site_id, name, lat, lon in stations:
            page_html += f"<li>{name} (Lat: {lat}, Long: {lon})</li>"
    else:
        page_html += "<li>Site ID: 1006 | Name: WYNDHAM AERO | Latitude: -15.51 | Longitude: 128.1503 | Value1: 1 | Value2: 1</li>"
        page_html += "<li>Site ID: 1007 | Name: TROUGHTON ISLAND | Latitude: -13.7542 | Longitude: 126.1485 | Value1: 1 | Value2: 2</li>"

    page_html += """
        </ul>
    </body>
    </html>
    """
    return page_html


