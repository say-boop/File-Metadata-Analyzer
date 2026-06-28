from app.utils import get_file_type


def test_image_jpg():
	assert get_file_type("photo.jpg") == "image"

def test_image_jpeg():
	assert get_file_type("photo.jpeg") == "image"

def test_image_png():
	assert get_file_type("screenshot.png") == "image"

def test_pdf():
	assert get_file_type("document.pdf") == "pdf"

def test_docx():
	assert get_file_type("report.docx") == "docx"

def test_audio_mp3():
	assert get_file_type("song.mp3") == "audio"

def test_audio_flac():
	assert get_file_type("track.flac") == "audio"

def test_unknown():
	assert get_file_type("file.xyz") == "unknown"

def test_no_extension():
	assert get_file_type("README") == "unknown"

def test_uppercase():
	assert get_file_type("IMAGE.PNG") == "image"
