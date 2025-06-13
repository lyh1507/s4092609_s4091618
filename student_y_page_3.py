import sqlite3

# database connection and data retrieval for Lucy 
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
    print("About to return Lucy White's Activist Tools...")

    stations = get_station_data()

    page_html = """
    <html>
    <head><title>Lucy White - Campaign Toolkit</title></head>
    <body>
        <h2>Welcome Lucy White (Climate NGO)</h2>
        <ul>
            <li> Visuals: Climate Change over 30 Years</li>
            <li> Auto-Generated Advocacy Texts</li>
            <li> Region Compare: VIC vs NSW trends</li>
        </ul>
        <p>Tools optimized for quick share/export for social media and policy engagement.</p>
        <hr>
        <h3>Weather Station</h3>
        <ul>
    """

    if stations:
        for site_id, name, lat, lon in stations:
            page_html += f"<li>{name} (Lat: {lat}, Long: {lon})</li>"
    else:
        page_html += "<li>Site ID: 7045 | Name: MEEKATHARRA AIRPORT | Latitude: -26.6136 | Longitude: 118.5372 | Value1:  | Value2: </li>"
        page_html += "<li>Site ID: 9021 | Name: PERTH AIRPORT | Latitude: 31.9275 | Longitude: 115.9764 | Value1:  | Value2: </li>"

    page_html += """
        </ul>
    </body>
    </html>
    """
    return page_html
