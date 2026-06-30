from pymediainfo import MediaInfo
from pathlib import Path


def analyze_video(file_path: str) -> dict:
	path_obj = Path(file_path)

	result = {
		"file_name": path_obj.name,
		"file_size": path_obj.stat().st_size,
		"type": "video",
		"format": "N/A",
		"duration": "N/A",
		"resolution": "N/A",
		"video_codec": "N/A",
		"audio_codec": "N/A",
		"bitrate": "N/A",
		"subtitles": "N/A",
	}

	try:
		media_info = MediaInfo.parse(file_path)

		for track in media_info.tracks:
			if track.track_type == "General":
				result["format"] = track.format
				result["duration"] = track.duration
				result["bitrate"] = track.overall_bit_rate
			elif track.track_type == "Video":
				result["resolution"] = f"{track.width}x{track.height}"
				result["video_codec"] = track.codec_id
			elif track.track_type == "Audio":
				result["audio_codec"] = track.codec_id
			elif track.track_type == "Text":
				result["subtitles"] += 1
	except Exception:
		return result

	return result
