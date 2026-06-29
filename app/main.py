from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import Response, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.scanner import scan_directory
from app.analyzers.images import analyze_image
from app.analyzers.pdf import analyze_pdf
from app.analyzers.docx import analyze_docx
from app.analyzers.audio import analyze_audio
from app.reporters.html import generate_html_report
from app.reporters.json import generate_json_report

from app.schemas.schem import ScanRequest


app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

last_results = []


@app.get("/")
def root(request: Request):
	return templates.TemplateResponse(
		request=request,
		name="index.html"
	)


@app.post("/scan")
def scan_file(req: ScanRequest):
	directory = req.directory
	files = scan_directory(directory)
	
	results = []
	
	for f in files:
		path = f["path"]
		file_type = f["type"]

		if file_type == "image":
			result = analyze_image(path)
		elif file_type == "pdf":
			result = analyze_pdf(path)
		elif file_type == "docx":
			result = analyze_docx(path)
		elif file_type == "audio":
			result = analyze_audio(path)
		else:
			result = f

		results.append(result)

	global last_results
	last_results = results
	return {
		"status": "ok",
		"total": len(results),
		"files": results
	}


@app.get("/report/json")
def report_json():
	if not last_results:
		return {
			"error": "No scan results. Run /scan first/"
		}
	json_str = generate_json_report(last_results)
	
	return Response(
		content=json_str,
		media_type="application/json",
		headers={
			"Content-Disposition": "attachment; filename=report.json"
		}
	)


@app.get("/report/html")
def report_html():
	if not last_results:
		return {
			"error": "No scan results. Run /scan first/"
		}

	html_str = generate_html_report(last_results)

	return HTMLResponse(
		content=html_str,
		headers={
			"Content-Disposition": "attachment; filename=report.html"
		}
	)
