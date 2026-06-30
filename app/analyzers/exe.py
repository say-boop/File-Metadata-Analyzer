from pathlib import Path
from datetime import datetime
import pefile


def analyze_exe(file_path: str) -> dict:
	path_obj = Path(file_path)

	result = {
		"file_name": path_obj.name,
		"file_size": path_obj.stat().st_size,
		"type": "exe" if path_obj.suffix.lower() == ".exe" else "dll",
		"company": "N/A",
		"description": "N/A",
		"version": "N/A",
		"product": "N/A",
		"copyright": "N/A",
		"compile_date": "N/A",
		"architecture": "N/A",
	}

	try:
		pe = pefile.PE(file_path)

		if pe.FILE_HEADER.Machine == 0x8664:
			result["architecture"] = "64-bit"
		elif pe.FILE_HEADER.Machine == 0x014c:
			result["architecture"] = "32-bit"
		else:
			result["architecture"] = f"Unknown (0x{pe.FILE_HEADER.Machine:X})"

		timestamp = pe.FILE_HEADER.TimeDateStamp
		if timestamp:
			result["compile_date"] = datetime.fromtimestamp(timestamp).isoformat()

		if hasattr(pe, "FileInfo"):
			for info in pe.FileInfo:
				for entry in info:
					if hasattr(entry, "StringTable"):
						for table in entry.StringTable:
							for key, value in table.entries.items():
								key_str = key.decode() if isinstance(key, bytes) else key
								val_str = value.decode() if isinstance(value, bytes) else value

								if key_str == "CompanyName":
									result["company"] = val_str
								elif key_str == "FileDescription":
									result["description"] = val_str
								elif key_str == "FileVersion":
									result["version"] = val_str
								elif key_str == "ProductName":
									result["product"] = val_str
								elif key_str == "LegalCopyright":
									result["copyright"] = val_str

		return result
	except Exception:
		return result
	
