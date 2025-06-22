import sqlite3

def create_connection(db_file):
    try:
        return sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return None

def get_urban_data():
    sample_data = [
        (1001, "Brisbane CBD", 12500, "High"),
        (1002, "Fortitude Valley", 8200, "High"),
        (1003, "South Brisbane", 9500, "Medium"),
        (1004, "Newstead", 5400, "Medium"),
        (1005, "West End", 6800, "Low"),
        (1006, "Kelvin Grove", 4200, "Medium"),
        (1007, "Woolloongabba", 5800, "High"),
        (1008, "Teneriffe", 3100, "Low"),
        (1009, "Spring Hill", 3900, "Medium"),
        (1010, "Milton", 4700, "Low")
    ]
    
    try:
        conn = create_connection("climate.db")
        if not conn:
            return sample_data
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT site_id, name, population, risk_level 
            FROM urban_areas 
            WHERE state = 'QLD'
            ORDER BY risk_level DESC
            LIMIT 10
        """)
        results = cursor.fetchall()
        return results if results else sample_data
    except sqlite3.Error as e:
        print(f"❌ Query error: {e}")
        return sample_data
    finally:
        if 'conn' in locals():
            conn.close()

def get_page_html(form_data):
    urban_areas = get_urban_data()
    
    return f"""
    <div class="dashboard-content">
        <div class="card">
            <h2>Frank Liu - Brisbane Urban Planning Hub</h2>
            
            <div class="alert-box warning">
                <span class="icon"></span> 
                <strong>Planning Alert:</strong> {len([a for a in urban_areas if a[3] == 'High'])} high-risk zones identified in growth corridors
            </div>
            
            <div class="data-grid">
                <div class="data-card">
                    <h3>Population Growth</h3>
                    <p>2025 Projection: +2.3%</p>
                    <p class="trend-up">15% above state average</p>
                </div>
                
                <div class="data-card">
                    <h3>Infrastructure Projects</h3>
                    <p>{len(urban_areas)} active projects</p>
                    <p>${len(urban_areas)*240}M total investment</p>
                </div>
                
                <div class="data-card">
                    <h3>Climate Resilience</h3>
                    <p>{int(len(urban_areas)*4.2)}% of infrastructure rated</p>
                    <p class="alert">{int(len(urban_areas)*1.8)}% need upgrades</p>
                </div>
            </div>
            
            <div class="data-section">
                <h3>High Priority Urban Areas (QLD)</h3>
                <div class="data-notice">
                    <p>Displaying {'database' if len(urban_areas) > 0 and urban_areas[0][0] != 1001 else 'sample'} data</p>
                </div>
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Site ID</th>
                            <th>Area Name</th>
                            <th>Population</th>
                            <th>Risk Level</th>
                        </tr>
                    </thead>
                    <tbody>
                        {"".join(
                            f'<tr><td>{site_id}</td><td>{name}</td><td>{population}</td><td class="risk-{risk_level.lower()}">{risk_level}</td></tr>'
                            for site_id, name, population, risk_level in urban_areas
                        )}
                    </tbody>
                </table>
            </div>
            
            <div class="tool-container" id="data-export">
                <h3>Data Export Options</h3>
                <div class="data-section">
                    <button class="btn action-btn" onclick="exportData('csv')">Export as CSV</button>
                    <button class="btn action-btn" onclick="exportData('json')">Export as JSON</button>
                </div>
            </div>
            
            <div class="alert-box">
                <span class="icon"></span> 
                <strong>Upcoming Deadline:</strong> North Brisbane Corridor Plan due 15/07/2025
            </div>
        </div>
    </div>
    <script>
        function exportData(format) {{
            const urbanData = {urban_areas};
            let content, mimeType, filename;
            
            if (format === 'csv') {{
                const headers = ['Site ID', 'Area Name', 'Population', 'Risk Level'].join(',');
                const rows = urbanData.map(row => row.join(','));
                content = [headers, ...rows].join('\\n');
                mimeType = 'text/csv';
                filename = 'brisbane_urban_areas.csv';
            }} else {{
                content = JSON.stringify(urbanData.map(row => ({{
                    site_id: row[0],
                    name: row[1],
                    population: row[2],
                    risk_level: row[3]
                }})), null, 2);
                mimeType = 'application/json';
                filename = 'brisbane_urban_areas.json';
            }}
            
            const blob = new Blob([content], {{ type: mimeType }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }}
    </script>
    """