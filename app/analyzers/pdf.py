from PyPDF2 import PdfReader
from pathlib import Path


def analyze_pdf(file_path: str) -> dict:
	path_obj = Path(file_path)
	
	try:
		reader = PdfReader(file_path)
		meta = reader.metadata

		return {
			"file_name": path_obj.name,
			"file_size": path_obj.stat().st_size,
			"type": "pdf",
			"author": meta.get("/Author", "N/A") if meta else "N/A",
			"creator": meta.get("/Creator", "N/A") if meta else "N/A",
			"producer": meta.get("/Producer", "N/A") if meta else "N/A",
			"subject": meta.get("/Subject", "N/A") if meta else "N/A",
			"title": meta.get("/Title", "N/A") if meta else "N/A",
			"pages": len(reader.pages),
		}
	except Exception:
		return {
			"file_name": path_obj.name,
			"file_size": path_obj.stat().st_size,
			"type": "pdf",
		}
