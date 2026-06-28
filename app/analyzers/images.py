from PIL import Image
from pathlib import Path
import exifread


def analyze_image(file_path: str) -> dict:
	file_path_obj = Path(file_path)
	result = {
		"file_name": file_path_obj.name,
		"file_size": file_path_obj.stat().st_size,
		"type": "image"
	}

	try:
		with Image.open(file_path) as img:
			result["resolution"] = f"{img.width}x{img.height}"
			result["format"] = img.format
	except Exception:
		result["resolution"] = "Unknown"

	try:
		with open(file_path, "rb") as f:
			tags = exifread.process_file(f, details=False)
	except Exception:
		tags = {}

	if "Image Make" in tags and "Image Model" in tags:
		result["camera"] = f"{tags["Image Make"]} {tags["Image Model"]}".strip()

	if "EXIF DateTimeOriginal" in tags:
		result["date_taken"] = str(tags["EXIF DateTimeOriginal"])
	elif "Image DateTime" in tags:
		result["date_taken"] = str(tags["Image DateTime"])

	if "EXIF Flash" in tags:
		flash_value = tags["EXIF Flash"].values[0]
		result["flash"] = "Fired" if flash_value % 2 == 1 else "Not fired"

	if "EXIF ISOSpeedRatings" in tags:
		result["iso"] = str(tags["EXIF ISOSpeedRatings"])

	if "EXIF ExposureTime" in tags:
		result["exposure"] = str(tags["EXIF ExposureTime"])

	def convert_to_degrees(value):
		d = float(value.values[0].num) / float(value.values[0].den)
		m = float(value.values[1].num) / float(value.values[1].den)
		s = float(value.values[2].num) / float(value.values[2].den)
		return d + (m / 60.0) + (s / 3600.0)

	if "GPS GPSLatitude" in tags and "GPS GPSLongitude" in tags:
		lat = convert_to_degrees(tags["GPS GPSLatitude"])
		lon = convert_to_degrees(tags["GPS GPSLongitude"])

		if str(tags["GPS GPSLatitudeRef"]) == "S":
			lat = -lat
		if str(tags["GPS GPSLongitudeRef"]) == "W":
			lon = -lon

		result["gps"] = {
			"latitude": round(lat, 6),
			"longitude": round(lon, 6),
		}

	return result
