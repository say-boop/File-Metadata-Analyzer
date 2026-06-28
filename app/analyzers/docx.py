from docx import Document
from pathlib import Path


def analyze_docx(file_path: str) -> dict:
	path_obj = Path(file_path)
	
	try:
		doc = Document(file_path)
		props = doc.core_properties

		return {
			"file_name": path_obj.name,
			"file_size": path_obj.stat().st_size,
			"type": "docx",
			"author": props.author or "N/A",
			"created": str(props.created) if props.created else "N/A",
			"modified": str(props.modified) if props.modified else "N/A",
			"last_modified_by": props.last_modified_by or "N/A",
			"revision": props.revision or "N/A",
			"paragraphs": len(doc.paragraphs),
		}
	except Exception:
		return {
			"file_name": path_obj.name,
			"file_size": path_obj.stat().st_size,
			"type": "docx",
		}
