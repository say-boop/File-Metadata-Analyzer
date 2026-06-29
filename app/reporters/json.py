from datetime import datetime
from pathlib import Path
import json


def generate_json_report(results: list[dict], output_path: str = None) -> str:
	report = {
		"generated_at": datetime.now().isoformat(),
		"total_files": len(results),
		"files": results
	}

	if output_path is None:
		return json.dumps(report, ensure_ascii=False, indent=4)

	with open(output_path, "w", encoding="utf-8") as f:
		json.dump(report, f, ensure_ascii=False, indent=4)
