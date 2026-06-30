import sys

from app.analyzers.exe import analyze_exe


def test_analyze_python_exe():
	python_exe = sys.executable

	result = analyze_exe(python_exe)

	assert result["file_name"].endswith(".exe")
	assert result["type"] == "exe"
	assert "version" in result
	assert "compile_date" in result


def test_analyze_exe_no_file():
	import pytest
	with pytest.raises(FileNotFoundError):
		analyze_exe("nonexistent.exe")
