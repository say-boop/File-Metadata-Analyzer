from app.reporters.html import generate_html_report


def test_generate_html_report_string():
	results = [
    {
			"file_name": "test.jpg", 
			"type": "image", "gps": 
			{
				"latitude": 55.75, 
				"longitude": 37.61
			}
		},
    {
			"file_name": "doc.pdf", 
			"type": "pdf", 
			"author": "Test"
		}
  ]

	html = generate_html_report(results)

	assert isinstance(html, str)
	assert "<html" in html.lower()
	assert "test.jpg" in html
	assert "55.75" in html


def test_generate_html_report_file(tmp_path):
	results = [
		{
			"file_name": "test.jpg",
			"type": "image"
		}
	]

	output = tmp_path / "report.html"
	generate_html_report(results, str(output))

	assert output.exists()
	content = output.read_text(encoding="utf-8")
	assert "test.jpg" in content


def test_generate_html_no_gps():
	results = [
		{
			"file_name": "doc.pdf",
			"type": "pdf"
		}
	]

	html = generate_html_report(results)
	assert 'id="map"' not in html.lower()
