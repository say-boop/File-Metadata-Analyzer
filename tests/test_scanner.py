from app.scanner import scan_directory


def test_can_empty_directory(tmp_path):
	result = scan_directory(str(tmp_path))
	assert result == []


def test_scan_with_images(tmp_path):
	(tmp_path / "photo.jpg").write_text("fake")
	(tmp_path / "screenshot.jpeg").write_text("fake")
	(tmp_path / "readme.txt").write_text("fake")

	result = scan_directory(str(tmp_path))
	assert len(result) == 2
	types = {r["type"] for r in result}
	assert types == {"image"}


def test_scan_mixed(tmp_path):
	(tmp_path / "doc.pdf").write_text("fake")
	(tmp_path / "song.mp3").write_text("fake")
	(tmp_path / "notes.txt").write_text("fake")

	result = scan_directory(str(tmp_path))
	assert len(result) == 2
	types = {r["type"] for r in result}
	assert types == {"pdf", "audio"}


def test_scan_nested_folders(tmp_path):
	subdir = tmp_path / "subfolder"
	subdir.mkdir()
	(subdir / "image.jpg").write_text("fake")
	(subdir / "main.pdf").write_text("fake")

	result = scan_directory(str(tmp_path))
	assert len(result) == 2
