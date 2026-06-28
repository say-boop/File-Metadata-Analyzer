from PIL import Image
import os
import pytest

from app.analyzers.images import analyze_image


def test_analyze_image_basic(tmp_path):
	img_path = tmp_path / "test.jpg"
	img = Image.new("RGB", (100,200), color="red")
	img.save(img_path)

	result = analyze_image(str(img_path))

	assert result["file_name"] == "test.jpg"
	assert result["type"] == "image"
	assert result["resolution"] == "100x200"
	assert result["format"] == "JPEG"
	assert result["file_size"] > 0


def test_analyze_image_png(tmp_path):
	img_path = tmp_path / "test.png"
	img = Image.new("RGBA", (300,150), color="blue")
	img.save(img_path)

	result = analyze_image(str(img_path))

	assert result["file_name"] == "test.png"
	assert result["resolution"] == "300x150"
	assert result["format"] == "PNG"


def test_analyze_image_with_exif(tmp_path):
	from PIL.ExifTags import Base as Exiftags

	img_path = tmp_path / "exif_test.jpg"
	img = Image.new("RGB", (500,500), color="green")

	exif = img.getexif()
	exif[0x010F] = "Canon"
	exif[0x0110] = "EOS 5D"
	exif[0x9003] = "2026:01:15 12:30:00"
	exif[0x8827] = 400
	exif[0x9209] = 1

	img.save(img_path, exif=exif.tobytes())

	result = analyze_image(str(img_path))

	assert "Canon" in result.get("camera", "")
	assert "EOS 5D" in result.get("camera", "")


def test_analyze_image_no_file():
	with pytest.raises(FileNotFoundError):
		analyze_image("nonexistent.jpg")


def test_analyze_image_corrupted(tmp_path):
	img_path = tmp_path / "corrupted.jpg"
	img_path.write_text("not an image")

	result = analyze_image(str(img_path))

	assert result["file_name"] == "corrupted.jpg"
	assert result["type"] == "image"
