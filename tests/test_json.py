import json

from app.reporters.json import generated_json_report


def test_generated_json_report_string():
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

	json_str = generated_json_report(results)

	assert isinstance(json_str, str)
	data = json.loads(json_str)
	assert data["total_files"] == 2
	assert len(data["files"]) == 2
	assert "generated_at" in data


def test_generate_json_report_file(tmp_path):
	results = [
		{
			"file_name": "test.jpg",
			"type": "image"
		}
	]

	output = tmp_path / "report.json"
	generated_json_report(results, str(output))

	assert output.exists()
	with open(output, "r") as f:
		data = json.load(f)
	assert data["total_files"] == 1
