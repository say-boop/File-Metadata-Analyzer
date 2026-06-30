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

	".exe": "exe",
	".dll": "exe",
	".zip": "archive",
	".rar": "archive",
	".7z": "archive",
	".mp4": "video",
	".mkv": "video",
	".avi": "video",
	".mov": "video",
}


def get_file_type(file_path: str) -> str:
	expansion = Path(file_path).suffix.lower()

	if expansion in EXTENSION_MAP:
		return EXTENSION_MAP[expansion]

	return "unknown"
