from PyPDF2 import PdfReader
from pathlib import Path


def analyze_pdf(file_path: str) -> dict:
	path_obj = Path(file_path)

	result = {
		"file_name": path_obj.name,
		"file_size": path_obj.stat().st_size,
		"type": "pdf",
		"author": "N/A",
		"creator": "N/A",
		"producer": "N/A",
		"subject": "N/A",
		"title": "N/A",
		"has_attachments": False,
		"has_signature": False,
		"has_form_fields": False,
		"extracted_text": "",
		"annotations": 0,
		"pages": "N/A",
	}
	
	try:
		reader = PdfReader(file_path)
		meta = reader.metadata

		result["author"] = meta.get("/Author", "N/A") if meta else "N/A"
		result["creator"] = meta.get("/Creator", "N/A") if meta else "N/A"
		result["producer"] = meta.get("/Producer", "N/A") if meta else "N/A"
		result["subject"] = meta.get("/Subject", "N/A") if meta else "N/A"
		result["title"] = meta.get("/Title", "N/A") if meta else "N/A"
		result["pages"] = len(reader.pages)
		result["has_attachments"] = True if reader.attachments else False
		result["has_form_fields"] = True if reader.get_fields() else False

		try:
			text = ""
			for page in reader.pages[:3]:
				text += page.extract_text() or ""
			result["extracted_text"] = text[:500]
		except Exception:
			pass

		return result
	except Exception:
		return result
