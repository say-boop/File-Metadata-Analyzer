from pathlib import Path
from datetime import datetime
import zipfile


def analyze_archive(file_path: str) -> dict:
	path_obj = Path(file_path)

	result = {
		"file_name": path_obj.name,
		"file_size": path_obj.stat().st_size,
		"type": "archive",
		"format": "ZIP" if path_obj.suffix.lower() == ".zip" else "RAR",
		"total_files": "N/A",
		"compression": "N/A",
		"files": "N/A",
		"total_size_uncompressed": "N/A",
		"total_size_compressed": "N/A",
	}

	try:
		with zipfile.ZipFile(file_path, "r") as zf:
			info_list = zf.infolist()
			result["total_files"] = len(info_list)
			result["compression"] = zf.compression
			result["files"] = [f.filename for f in info_list[:20]]
			result["total_size_uncompressed"] = sum(f.file_size for f in info_list)
			result["total_size_compressed"] = sum(f.compress_size for f in info_list)
	except Exception:
		return result

	return result
