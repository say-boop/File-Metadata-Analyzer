from app.analyzers.pdf import analyze_pdf


def test_analyze_pdf_basic(tmp_path):
	from PyPDF2 import PdfWriter

	pdf_path = tmp_path / "test.pdf"
	writer = PdfWriter()
	writer.add_blank_page(width=595, height=842)
	writer.add_metadata({
		"/Author": "Test Author",
		"/Title": "Test Document",
	})
	
	with open(pdf_path, "wb") as f:
		writer.write(f)

	result = analyze_pdf(str(pdf_path))

	assert result["file_name"] == "test.pdf"
	assert result["type"] == "pdf"
	assert result["pages"] == 1
	assert result["author"] == "Test Author"
	assert result["title"] == "Test Document"


def test_analyze_pdf_empty(tmp_path):
	from PyPDF2 import PdfWriter

	pdf_path = tmp_path / "empty.pdf"
	writer = PdfWriter()
	writer.add_blank_page(width=595, height=842)
	
	with open(pdf_path, "wb") as f:
		writer.write(f)

	result = analyze_pdf(str(pdf_path))

	assert result["type"] == "pdf"
	assert result["pages"] == 1


def test_analyze_pdf_no_file():
	import pytest
	with pytest.raises(FileNotFoundError):
		analyze_pdf("nonexistent.pdf")


def test_analyze_pdf_fields(tmp_path):
	from PyPDF2 import PdfWriter

	pdf_path = tmp_path / "fields.pdf"
	writer = PdfWriter()
	writer.add_blank_page(width=595, height=842)
	writer.add_blank_page(width=595, height=842)
	with open(pdf_path, "wb") as f:
		writer.write(f)

	result = analyze_pdf(str(pdf_path))

	assert "has_attachments" in result
	assert "has_signature" in result
	assert "extracted_text" in result
	assert "annotations" in result
	assert result["pages"] == 2
