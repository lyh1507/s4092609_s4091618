import sqlite3
from datetime import datetime

def create_connection(db_file):
    try:
        return sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        return None

def get_climate_data():
    conn = create_connection("climate.db")
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT year, temperature_change, co2_levels 
            FROM climate_data 
            ORDER BY year DESC
            LIMIT 30
        """)
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"❌ Query error: {e}")
        return []
    finally:
        conn.close()

def get_region_comparison(region1, region2):
    conn = create_connection("climate.db")
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT region, AVG(temperature_change), AVG(rainfall_change)
            FROM regional_data
            WHERE region IN (?, ?)
            GROUP BY region
        """, (region1, region2))
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"❌ Comparison error: {e}")
        return None
    finally:
        conn.close()

def generate_petition(text):
    # In a real implementation, this would save to database
    return f"http://example.com/petition/{datetime.now().timestamp()}"

def get_page_html(form_data):
    climate_data = get_climate_data()
    
    # Handle form submissions
    generated_visual = ""
    petition_link = ""
    comparison_results = ""
    
    if 'generate_visuals' in form_data:
        generated_visual = "<div class='alert-box positive'>Climate visual generated! <a href='#'>Download Image</a></div>"
    
    if 'generate_petition' in form_data and form_data['petition_text']:
        petition_text = form_data['petition_text'][0]
        petition_link = generate_petition(petition_text)
        petition_link = f"<div class='alert-box positive'>Petition created! <a href='{petition_link}' target='_blank'>Share this link</a></div>"
    
    if 'compare_regions' in form_data and form_data['region1'] and form_data['region2']:
        region1 = form_data['region1'][0]
        region2 = form_data['region2'][0]
        results = get_region_comparison(region1, region2)
        if results:
            comparison_results = f"""
            <div class='data-section'>
                <h4>Comparison Results:</h4>
                <table class='data-table'>
                    <tr><th>Region</th><th>Avg Temp Change</th><th>Avg Rainfall Change</th></tr>
                    <tr><td>{results[0][0]}</td><td>{results[0][1]:.2f}°C</td><td>{results[0][2]:.2f}mm</td></tr>
                    <tr><td>{results[1][0]}</td><td>{results[1][1]:.2f}°C</td><td>{results[1][2]:.2f}mm</td></tr>
                </table>
            </div>
            """
    
    return f"""
    <div class="dashboard-content">
        <div class="card activist-card">
            <h2>Lucy White's Climate Activist Toolkit</h2>
            
            {generated_visual}
            {petition_link}
            
            <div class="alert-box danger">
                <span class="icon"></span> 
                <strong>Urgent Action Needed:</strong> CO2 levels at record highs
            </div>
            
            <div class="data-grid">
                <div class="data-card">
                    <h3>30-Year Trends</h3>
                    <p>+1.2 degrees celcius temperature rise</p>
                    <p class="trend-up">42% increase in extreme weather</p>
                </div>
                
                <div class="data-card">
                    <h3>Advocacy Tools</h3>
                    <p>12 pre-written templates</p>
                    <p>5 campaign toolkids</p>
                </div>
                
                <div class="data-card">
                    <h3>Regional Comparison</h3>
                    <p>VIC: +1.1 degrees celcius | NSW: +1.3 degrees celcius</p>
                    <p class="alert">Both above global average</p>
                </div>
            </div>
            
            <form method="GET">
                <div class="button-group">
                    <button type="submit" name="generate_visuals" value="1" class="btn action-btn">
                        Generate Visuals
                    </button>
                    <button type="button" onclick="document.getElementById('petition-tool').style.display='block'" 
                        class="btn action-btn">
                        Create Petition
                    </button>
                    <button type="button" onclick="document.getElementById('region-compare').style.display='block'" 
                        class="btn action-btn">
                        Compare Regions
                    </button>
                </div>
                
                <div class="tool-container" id="climate-visuals">
                    <h3>Climate Change Visuals (30 Years)</h3>
                    <div class="data-section">
                        <div class="climate-timeline">
                            {"".join(
                                f'<div class="timeline-item year-{year}">'
                                f'<span class="year">{year}</span>'
                                f'<span class="temp-change">{temp_change}°C</span>'
                                f'<span class="co2-level">{co2_level}ppm</span>'
                                '</div>'
                                for year, temp_change, co2_level in climate_data
                            )}
                        </div>
                    </div>
                </div>
                
                <div class="tool-container" id="petition-tool" style="display:none">
                    <h3>Petition Generator</h3>
                    <div class="data-section">
                        <textarea name="petition_text" class="petition-textarea" 
                            placeholder="Enter your petition text here..."></textarea>
                        <button type="submit" name="generate_petition" value="1" class="btn action-btn">
                            Generate Shareable Link
                        </button>
                    </div>
                </div>
                
                <div class="tool-container" id="region-compare" style="display:none">
                    <h3>Region Comparison Tool</h3>
                    <div class="data-section">
                        <div class="form-group">
                            <label for="region1">First Region:</label>
                            <select name="region1" id="region1" class="form-control">
                                <option value="VIC">Victoria</option>
                                <option value="NSW">New South Wales</option>
                                <option value="QLD">Queensland</option>
                                <option value="SA">South Australia</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="region2">Second Region:</label>
                            <select name="region2" id="region2" class="form-control">
                                <option value="NSW">New South Wales</option>
                                <option value="VIC">Victoria</option>
                                <option value="QLD">Queensland</option>
                                <option value="SA">South Australia</option>
                            </select>
                        </div>
                        <button type="submit" name="compare_regions" value="1" class="btn action-btn">
                            Compare Regions
                        </button>
                        {comparison_results}
                    </div>
                </div>
            </form>
            
            <div class="alert-box positive">
                <span class="icon"></span> 
                <strong>Success:</strong> Last petition gained 12,342 signatures
            </div>
        </div>
    </div>
    """