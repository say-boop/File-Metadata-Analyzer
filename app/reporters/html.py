from datetime import datetime
from pathlib import Path


def generate_html_report(results: list[dict], output_path: str = None) -> str:
	gps_points = []
	
	for r in results:
		if "gps" in r and r["gps"]:
			gps_points.append({
				"lat": r["gps"]["latitude"],
				"lon": r["gps"]["longitude"],
				"name": r["file_name"]
			})

	rows = ""

	for r in results:
		badge_class = f"badge badge-{r["type"]}"
		
		if r["type"] == "image":
			info = f"<div><strong>Camera:</strong> {r.get('camera', 'N/A')}</div><div><strong>Date:</strong> {r.get('date_taken', 'N/A')}</div>"
			if "gps" in r and r["gps"]:
				info += f"<div class='gps-meta'><strong>GPS:</strong> {r['gps']['latitude']}, {r['gps']['longitude']}</div>"
		elif r["type"] == "pdf":
			info = f"<div><strong>Author:</strong> {r.get('author','N/A')}</div><div><strong>Pages:</strong> {r.get('pages', 'N/A')}</div>"
		elif r["type"] == "docx":
			info = f"<div><strong>Author:</strong> {r.get('author', 'N/A')}</div><div><strong>Paragraphs:</strong> {r.get('paragraphs', 'N/A')}</div>"
		elif r["type"] == "audio":
			info = f"<div><strong>Artist:</strong> {r.get('artist', 'N/A')}</div><div><strong>Album:</strong> {r.get('album', 'N/A')}</div><div><strong>Duration:</strong> {r.get('duration', 'N/A')}s</div>"
		else:
			info = "N/A"

		rows += f"""<tr>
      <td class="file-name">{r['file_name']}</td>
      <td><span class="{badge_class}">{r['type']}</span></td>
      <td class="meta-cell">{info}</td>
    </tr>"""

	map_html = ""

	if gps_points:
		map_html = f'''
      <h2>📍 File Geo-Locations</h2>
      <div id="map"></div>
      <script>
        var map = L.map("map").setView([{gps_points[0]["lat"]}, {gps_points[0]["lon"]}], 4);
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png').addTo(map);
    '''

		for p in gps_points:
			map_html += f"L.marker([{p["lat"]}, {p["lon"]}]).addTo(map).bindPopup('{p["name"]}');\n"

		map_html += "</script>"

	html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Metadata Analysis Report</title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <style>
    :root {{
      --bg-color: #0f172a;
      --card-bg: #1e293b;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --accent: #3b82f6;
      --border-color: #334155;
    }}

    body {{
      font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background-color: var(--bg-color);
      color: var(--text-main);
      margin: 0;
      padding: 40px 20px;
      display: flex;
      flex-direction: column;
      align-items: center;
    }}

    .report-container {{
      width: 100%;
      max-width: 1000px;
    }}

    h1 {{
      font-size: 2.2rem;
      font-weight: 700;
      margin-bottom: 8px;
    }}

    h2 {{
      font-size: 1.5rem;
      font-weight: 600;
      margin-top: 40px;
      margin-bottom: 16px;
      color: var(--text-main);
    }}

    .meta-summary {{
      display: flex;
      gap: 24px;
      color: var(--text-muted);
      font-size: 14px;
      margin-bottom: 32px;
      background: var(--card-bg);
      padding: 12px 20px;
      border-radius: 8px;
      border: 1px solid var(--border-color);
      width: fit-content;
    }}

    .meta-summary span strong {{
      color: var(--text-main);
    }}

    table {{
      width: 100%;
      border-collapse: separate;
      border-spacing: 0;
      background-color: var(--card-bg);
      border-radius: 12px;
      border: 1px solid var(--border-color);
      overflow: hidden;
      box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
      margin-bottom: 30px;
    }}

    th, td {{
      padding: 14px 20px;
      text-align: left;
      font-size: 14px;
    }}

    th {{
      background-color: #151f32;
      color: var(--text-muted);
      font-weight: 600;
      text-transform: uppercase;
      font-size: 11px;
      letter-spacing: 0.05em;
      border-bottom: 1px solid var(--border-color);
    }}

    td {{
      border-bottom: 1px solid var(--border-color);
      color: var(--text-main);
      vertical-align: top;
    }}

    tr:last-child td {{
      border-bottom: none;
    }}

    .file-name {{
      font-weight: 500;
      max-width: 300px;
      word-break: break-all;
    }}

    .meta-cell {{
      font-size: 13px;
      color: var(--text-muted);
      line-height: 1.5;
    }}
    .meta-cell strong {{
      color: #cbd5e1;
    }}
    .gps-meta {{
      color: #60a5fa;
      margin-top: 4px;
    }}
    .na-text {{
      color: #475569;
      font-style: italic;
    }}

    .badge {{
      display: inline-block;
      padding: 4px 8px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }}
    .badge-image {{ background: rgba(16, 185, 129, 0.15); color: #10b981; }}
    .badge-pdf   {{ background: rgba(239, 68, 68, 0.15);  color: #ef4444; }}
    .badge-docx  {{ background: rgba(59, 130, 246, 0.15); color: #3b82f6; }}
    .badge-audio {{ background: rgba(245, 158, 11, 0.15); color: #f59e0b; }}
    .badge-other {{ background: rgba(148, 163, 184, 0.15); color: #94a3b8; }}

    #map {{
      height: 450px;
      border-radius: 12px;
      border: 1px solid var(--border-color);
      box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
    }}
    
    .leaflet-tile-container {{
      filter: invert(100%) hue-rotate(180deg) brightness(95%) contrast(90%);
    }}
    .leaflet-container {{
      background: #0b0f19 !important;
    }}
    .leaflet-popup-content-wrapper, .leaflet-popup-tip {{
      background: var(--card-bg) !important;
      color: var(--text-main) !important;
      border: 1px solid var(--border-color);
    }}
  </style>
</head>
<body>
  <div class="report-container">
    <h1>📄 Metadata Analysis Report</h1>
    
    <div class="meta-summary">
      <span><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span>
      <span><strong>Total Files:</strong> {len(results)}</span>
    </div>
      
    <table>
      <thead>
        <tr>
          <th style="width: 35%;">File</th>
          <th style="width: 15%;">Type</th>
          <th style="width: 50%;">Metadata</th>
        </tr>
      </thead>
      <tbody>
        {rows}
      </tbody>
    </table>
      
    {map_html}
  </div>
</body>
</html>"""

	if output_path:
		with open(output_path, "w", encoding="utf-8") as f:
			f.write(html)

	return html
