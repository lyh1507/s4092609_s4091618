import sqlite3

#Database connection and data retrieval for Allen Donald 
def create_connection(db_file):
    try:
        return sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(f"❌ Error connecting to database: {e}")
    return None

def get_station_data():
    conn = create_connection("climate.db")  # Ensure this file is in your project root
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        # You can later add filtering for "NSW" stations if needed
        cursor.execute("SELECT site_id, name, latitude, longitude FROM weather_station LIMIT 20")
        rows = cursor.fetchall()
        conn.close()
        return rows
    except sqlite3.Error as e:
        print(f"❌ Error fetching station data: {e}")
        return []

def get_page_html(form_data):
    print("About to return Allen Donald's Agricultural Farmer page...")

    stations = get_station_data()

    page_html = """
    <html>
    <head><title>Allen Donald - Agri Dashboard</title></head>
    <body>
        <h2>Welcome Allen Donald (NSW Farmer)</h2>
        <ul>
            <li> Soil Forecast (Hyperlocal): <b>Optimal irrigation time: 6–8am</b></li>
            <li> Long-Term Trends: 2025 likely 8% drier than 2024</li>
            <li> Frost Alert: Expected in 3 days</li>
            <li> Simpler interface loaded – tailored for ease of use</li>
        </ul>
        <p>This dashboard uses local sensors to improve crop rotation planning.</p>
        <hr>
        <h3>Weather Stations</h3>
        <ul>
    """

    if stations:
        for site_id, name, lat, lon in stations:
            page_html += f"<li>{name} (Lat: {lat}, Long: {lon})</li>"
    else:
        page_html += "<li>Site ID: 5007 | Name: LEARMONTH AIRPORT | Latitude: -22.2406 | Longitude: 114.0967 | Value1: 1 | Value2: 6</li>"
        page_html += "<li>Site ID: 5008 | Name: MARDIE | Latitude: -21.1906 | Longitude: 115.9797 | Value1: 1 | Value2: 7</li>"

    page_html += """
        </ul>
    </body>
    </html>
    """
    return page_html
