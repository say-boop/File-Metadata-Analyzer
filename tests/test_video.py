import pytest

from app.analyzers.video import analyze_video


def test_analyze_video_no_file():
	with pytest.raises(FileNotFoundError):
		analyze_video("nonexistent.mp4")
