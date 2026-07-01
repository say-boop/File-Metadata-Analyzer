from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TPE1, TALB, TIT2
import pytest

from app.analyzers.audio import analyze_audio


def create_test_mp3(path, artist="Test Artist", album="Test Album", title="Test Song"):
	with open(path, "wb") as f:
		f.write(b'\xff\xfb\x90\x00' * 100)
	
	audio = MP3()
	audio.tags = ID3()
	audio.tags.add(TPE1(encoding=3, text=artist))
	audio.tags.add(TALB(encoding=3, text=album))
	audio.tags.add(TIT2(encoding=3, text=title))
	audio.save(path)
	return path


def test_analyze_audio_no_file():
	with pytest.raises(FileNotFoundError):
		analyze_audio("nonexsitent.mp3")


def test_analyze_audio_basic(tmp_path):
	audio_path = tmp_path / "test.mp3"
	create_test_mp3(str(audio_path))

	result = analyze_audio(str(audio_path))

	assert result["file_name"] == "test.mp3"
	assert result["type"] == "audio"
	assert "artist" in result
	assert "album" in result
	assert "title" in result
	assert "format" in result


def test_analyze_audio_fields(tmp_path):
	audio_path = tmp_path / "test.mp3"
	create_test_mp3(str(audio_path))

	result = analyze_audio(str(audio_path))

	assert "channels" in result
	assert "lyrics" in result
	assert "cover_extracted" in result
