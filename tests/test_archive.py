import zipfile

from app.analyzers.archive import analyze_archive


def test_analyze_zip(tmp_path):
	zip_path = tmp_path / "test.zip"

	with zipfile.ZipFile(zip_path, "w") as zf:
		zf.writestr("file1.txt", "Hello World")
		zf.writestr("folder/file2.txt", "Test content")

	result = analyze_archive(str(zip_path))

	assert result["file_name"] == "test.zip"
	assert result["type"] == "archive"
	assert result["format"] == "ZIP"
	assert result["total_files"] == 2
	assert len(result["files"]) == 2


def test_analyze_archive_no_file():
	import pytest
	with pytest.raises(FileNotFoundError):
		analyze_archive("nonexistent.zip")
