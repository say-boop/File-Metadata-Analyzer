from pathlib import Path


EXTENSION_MAP = {
	".jpg": "image",
	".jpeg": "image",
	".png": "image",
	".tiff": "image",
	".bmp": "image",

	".pdf": "pdf",

	".docx": "docx",
	".doc": "docx",

	".mp3": "audio",
	".flac": "audio",
	".wav": "audio",
	".ogg": "audio",
}


def get_file_type(file_path: str) -> str:
	expansion = Path(file_path).suffix.lower()

	if expansion in EXTENSION_MAP:
		return EXTENSION_MAP[expansion]

	return "unknown"
