import sqlite3

#Database connection and data retrieval for Frank 
def create_connection(db_file):
    try:
        return sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(f"❌ Error connecting to database: {e}")
    return None

def get_station_data():
    conn = create_connection("climate.db")  # Make sure this file is in your root directory
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
    print("About to return Frank Liu's Planner page...")

    stations = get_station_data()

    page_html = """
    <html>
    <head><title>Frank Liu - Infrastructure Risk Tools</title></head>
    <body>
        <h2>Welcome Frank Liu (Brisbane City Planner)</h2>
        <ul>
            <li> Flood Risk Zones – Brisbane Inner North</li>
            <li> 2050 Scenario Simulator</li>
            <li> Exportable Reports for Policy</li>
        </ul>
        <p>Geo-referenced overlays available for Council use.</p>
        <hr>
        <h3>Weather Stations (QLD)</h3>
        <ul>
    """

    if stations:
        for site_id, name, lat, lon in stations:
            page_html += f"<li>{name} (Lat: {lat}, Long: {lon})</li>"
    else:
        page_html += "<li>Site ID: 6011 | Name: CARNARVON AIRPORT | Latitude: -24.8878 | Longitude: 113.67 | Value1: 1 | Value2: 8</li>"
        page_html += "<li>Site ID: 6072 | Name: EMU CREEK STATION | Latitude: -23.0314 | Longitude: 115.0414 | Value1: 1 | Value2: 9</li>"

    page_html += """
        </ul>
    </body>
    </html>
    """
    return page_html
