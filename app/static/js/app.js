document.getElementById("scan-form").addEventListener("submit", async function(e) {
	console.log("App.js loaded");
	e.preventDefault()
	
	const directory = document.getElementById("directory").value;
	const status = document.getElementById("status");
	const resultsDiv = document.getElementById("results");
	const submitBtn = document.getElementById("submit-btn");
	const exportBtns = document.getElementById("export-btns");
	
	submitBtn.classList.add("is-loading");
	submitBtn.disabled = true;
	directory.disabled = true;
	exportBtns.style.display = "none";
	
	console.log("Form submitted, directory:", directory);
	
	status.textContent = "Scanning...";
	resultsDiv.innerHTML = "";
	
	try {
		const response = await fetch("/scan", {
      method: "POST",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify({directory: directory})
    });
		
		const data = await response.json();
		
		if (data.status === "ok") {
			status.textContent = `Found ${data.total} files`;
			displayResults(data.files);
			document.getElementById("export-btns").style.display = "flex";
		}
	} catch (error) {
		status.textContent = "Error: " + error.message;
		console.error("Error:", error);
	} finally {
		submitBtn.classList.remove("is-loading");
		submitBtn.disabled = false;
		directory.disabled = false;
	}
});


function displayResults(files) {
	const resultsDiv = document.getElementById("results");
	
	let html = "<table><tr><th>File</th><th>Type</th><th>Details</th></tr>";
    
  files.forEach(f => {
    let details = "";
		const badgeClass = `badge badge-${f.type}`;
    if (f.type === "image") {
      details = f.camera || "";
      if (f.gps) details += ` GPS: ${f.gps.latitude}, ${f.gps.longitude}`;
    } else if (f.type === "pdf") {
      details = `Author: ${f.author || "N/A"}, Pages: ${f.pages || "N/A"}`;
    } else if (f.type === "docx") {
      details = `Author: ${f.author || "N/A"}, Paragraphs: ${f.paragraphs || "N/A"}`;
    } else if (f.type === "audio") {
      details = `Artist: ${f.artist || "N/A"}, Duration: ${f.duration || "N/A"}s`;
    }
        
    html += `<tr>
			<td style="font-weight:500;">${f.file_name}</td>
			<td><span class="${badgeClass}">${f.type}</span></td>
			<td style="color: var(--text-muted); font-size: 13px;">${details}</td>
		</tr>`;
  });
	
	html += "</table>";
	resultsDiv.innerHTML = html;
}
