from mutagen import File as MutagenFile
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from pathlib import Path


def analyze_audio(file_path: str) -> dict:
	path_obj = Path(file_path)

	base_result = {
		"file_name": path_obj.name,
		"file_size": path_obj.stat().st_size,
		"type": "audio",
		"format": "Unknown",
		"duration": "N/A",
		"bitrate": "N/A",
		"sample_rate": "N/A",
		"artist": "N/A",
		"album": "N/A",
		"title": "N/A",
		"genre": "N/A",
		"year": "N/A",
		"has_cover": False,
	}

	try:
		audio = MutagenFile(file_path)
		tags = audio.tags

		result = {
			**base_result,
		}

		if audio and audio.tags:
			result["format"] = type(audio).__name__
			result["duration"] = round(audio.info.length, 1) if hasattr(audio.info, "length") else "N/A"
			result["bitrate"] = round(audio.info.bitrate) if hasattr(audio.info, "bitrate") else "N/A"
			result["sample_rate"] = round(audio.info.sample_rate) if hasattr(audio.info, "sample_rate") else "N/A"
			result["artist"] = str(tags.get("TPE1", "N/A")) if "TPE1" in tags else str(tags.get("ARTIST", "N/A"))
			result["album"] = str(tags.get("TALB", "N/A")) if "TALB" in tags else str(tags.get("ALBUM", "N/A"))
			result["title"] = str(tags.get("TIT2", "N/A")) if "TIT2" in tags else str(tags.get("TITLE", "N/A"))
			result["genre"] = str(tags.get("TCON", "N/A")) if "TCON" in tags else str(tags.get("GENRE", "N/A"))
			result["year"] = str(tags.get("TDRC", "N/A")) if "TDRC" in tags else str(tags.get("DATE", "N/A"))
			result["has_cover"] = "APIC:" in str(tags) or "METADATA_BLOCK_PICTURE" in str(tags)
		
	except Exception:
		return base_result
