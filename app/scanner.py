from pathlib import Path
from app.utils import get_file_type


def scan_directory(directory: str) -> list[dict]:
	result = []
	for file_path in Path(directory).rglob("*"):
		if file_path.is_file():
			file_type = get_file_type(str(file_path))
			if file_type != "unknown":
				result.append({
					"path": str(file_path),
					"type": file_type,
					"name": Path(file_path).name,
					"size": Path(file_path).stat().st_size
				})

	return result
