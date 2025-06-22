from student_x_page_1 import get_page_html as sarah_page
from student_x_page_2 import get_page_html as david_page
from student_y_page_1 import get_page_html as allen_page
from student_x_page_3 import get_page_html as scout_page
from student_y_page_2 import get_page_html as frank_page
from student_y_page_3 import get_page_html as lucy_page
import http.server
import socketserver
from urllib.parse import parse_qs, urlparse
import os

class UnifiedHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        query = parse_qs(urlparse(self.path).query)
        
        # Serve static files
        if path.endswith(('.css', '.png', '.jpg', '.jpeg')):
            super().do_GET()
            return
            
        current_page = query.get('page', ['sarah'])[0]
        
        # Get content from the right page
        if current_page == 'sarah':
            content = sarah_page({})
            title = "Sarah's Farm Dashboard"
        elif current_page == 'david':
            content = david_page({})
            title = "David's Urban Planner"
        elif current_page == 'allen':
            content = allen_page({})
            title = "Allen's Agri Dashboard"
        elif current_page == 'scout':
            content = scout_page({})
            title = "Scout's Activist Hub"
        elif current_page == 'frank':
            content = frank_page({})
            title = "Frank's Infrastructure Tools"
        elif current_page == 'lucy':
            content = lucy_page({})
            title = "Lucy's Activist Toolkit"
        else:
            content = "<h1>Page not found</h1>"
            title = "Error"
        
        # Build the page
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <link rel="stylesheet" href="/style.css">
    <script>
        // Global event handlers
        document.addEventListener('DOMContentLoaded', function() {{
            // Handle tool toggles
            document.querySelectorAll('[data-target]').forEach(btn => {{
                btn.addEventListener('click', function() {{
                    const target = document.getElementById(this.dataset.target);
                    if (target) {{
                        target.style.display = target.style.display === 'none' ? 'block' : 'none';
                        if (this.id === 'flood-map-btn') {{
                            this.textContent = target.style.display === 'none' 
                                ? 'View Flood Zones' 
                                : 'Hide Flood Zones';
                        }}
                    }}
                }});
            }});
            
            // Initialize all tools as hidden
            document.querySelectorAll('.tool-container').forEach(el => {{
                el.style.display = 'none';
            }});
        }});
    </script>
</head>
<body>
    <nav class="main-nav">
        <a href="/?page=sarah" class="nav-btn {'active' if current_page == 'sarah' else ''}">Sarah</a>
        <a href="/?page=david" class="nav-btn {'active' if current_page == 'david' else ''}">David</a>
        <a href="/?page=allen" class="nav-btn {'active' if current_page == 'allen' else ''}">Allen</a>
        <a href="/?page=scout" class="nav-btn {'active' if current_page == 'scout' else ''}">Scout</a>
        <a href="/?page=frank" class="nav-btn {'active' if current_page == 'frank' else ''}">Frank</a>
        <a href="/?page=lucy" class="nav-btn {'active' if current_page == 'lucy' else ''}">Lucy</a>
    </nav>
    
    <main class="content">
        {content}
    </main>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())

def run_server():
    PORT = 8000
    with socketserver.TCPServer(("", PORT), UnifiedHandler) as httpd:
        print(f"\n🌐 Climate Dashboard running at http://localhost:{PORT}")
        print("Available pages:")
        print(f"   - Sarah: http://localhost:{PORT}/?page=sarah")
        print(f"   - David: http://localhost:{PORT}/?page=david")
        print(f"   - Allen: http://localhost:{PORT}/?page=allen")
        print(f"   - Scout: http://localhost:{PORT}/?page=scout")
        print(f"   - Frank: http://localhost:{PORT}/?page=frank")
        print(f"   - Lucy: http://localhost:{PORT}/?page=lucy")
        print("\n🛑 Press Ctrl+C to stop")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()