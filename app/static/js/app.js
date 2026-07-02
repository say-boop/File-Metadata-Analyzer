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


function showFileDetails(f) {
	console.log("Данные файла:", f);
	let html = "<div class='detail-panel'>";
	
	html += `<h3>${f.file_name}</h3>`;
	html += `<p><strong>Type:</strong> ${f.type}</p>`;
	html += `<p><strong>Size:</strong> ${(f.file_size / 1024).toFixed(2)} KB</p>`;
	
	if (f.type === "image") {
    html += `<p><strong>Camera:</strong> ${f.camera || "N/A"}</p>`;
    html += `<p><strong>Resolution:</strong> ${f.resolution || "N/A"}</p>`;
    html += `<p><strong>Date:</strong> ${f.date_taken || "N/A"}</p>`;
    html += `<p><strong>ISO:</strong> ${f.iso || "N/A"}</p>`;
    html += `<p><strong>Flash:</strong> ${f.flash || "N/A"}</p>`;
    html += `<p><strong>Orientation:</strong> ${f.orientation || "N/A"}</p>`;
    html += `<p><strong>White Balance:</strong> ${f.white_balance || "N/A"}</p>`;
    html += `<p><strong>Lens:</strong> ${f.lens || "N/A"}</p>`;
    html += `<p><strong>Software:</strong> ${f.software || "N/A"}</p>`;
    html += `<p><strong>Copyright:</strong> ${f.copyright || "N/A"}</p>`;
		html += `<img src="/preview?path=${encodeURIComponent(f.path || '')}" style="max-width:300px; border-radius:8px; margin-top:8px;">`;

    if (f.gps) {
      html += `<p><strong>GPS:</strong> ${f.gps.latitude}, ${f.gps.longitude}</p>`;
      html += `<div id="detail-map-${f.file_name.replace(/[^a-zA-Z0-9]/g, "_")}" style="height:300px; margin-top:12px; border-radius:8px;"></div>`;
    }
  } else if (f.type === "pdf") {
    html += `<p><strong>Author:</strong> ${f.author || "N/A"}</p>`;
    html += `<p><strong>Title:</strong> ${f.title || "N/A"}</p>`;
    html += `<p><strong>Pages:</strong> ${f.pages || "N/A"}</p>`;
    html += `<p><strong>Creator:</strong> ${f.creator || "N/A"}</p>`;
    html += `<p><strong>Subject:</strong> ${f.subject || "N/A"}</p>`;
    html += `<p><strong>Attachments:</strong> ${f.has_attachments ? "Yes" : "No"}</p>`;
    html += `<p><strong>Form fields:</strong> ${f.has_form_fields ? "Yes" : "No"}</p>`;
  } else if (f.type === "docx") {
    html += `<p><strong>Author:</strong> ${f.author || "N/A"}</p>`;
    html += `<p><strong>Created:</strong> ${f.created || "N/A"}</p>`;
    html += `<p><strong>Modified:</strong> ${f.modified || "N/A"}</p>`;
    html += `<p><strong>Paragraphs:</strong> ${f.paragraphs || "N/A"}</p>`;
    html += `<p><strong>Tables:</strong> ${f.tables_count || "N/A"}</p>`;
    html += `<p><strong>Images:</strong> ${f.images_count || "N/A"}</p>`;
    html += `<p><strong>Comments:</strong> ${f.has_comments ? "Yes" : "No"}</p>`;
  } else if (f.type === "audio") {
    html += `<p><strong>Artist:</strong> ${f.artist || "N/A"}</p>`;
    html += `<p><strong>Album:</strong> ${f.album || "N/A"}</p>`;
    html += `<p><strong>Title:</strong> ${f.title || "N/A"}</p>`;
    html += `<p><strong>Duration:</strong> ${f.duration || "N/A"}s</p>`;
    html += `<p><strong>Bitrate:</strong> ${f.bitrate || "N/A"} kbps</p>`;
    html += `<p><strong>Channels:</strong> ${f.channels || "N/A"}</p>`;
    html += `<p><strong>Has Cover:</strong> ${f.has_cover ? "Yes" : "No"}</p>`;
		html += `<audio controls style="width:100%; margin-top:8px;"><source src="/preview?path=${encodeURIComponent(f.path || '')}"></audio>`
  } else if (f.type === "exe") {
    html += `<p><strong>Version:</strong> ${f.version || "N/A"}</p>`;
    html += `<p><strong>Company:</strong> ${f.company || "N/A"}</p>`;
    html += `<p><strong>Compiled:</strong> ${f.compile_date || "N/A"}</p>`;
    html += `<p><strong>Architecture:</strong> ${f.architecture || "N/A"}</p>`;
    html += `<p><strong>Description:</strong> ${f.description || "N/A"}</p>`;
    html += `<p><strong>Copyright:</strong> ${f.copyright || "N/A"}</p>`;
  } else if (f.type === "archive") {
    html += `<p><strong>Format:</strong> ${f.format || "N/A"}</p>`;
    html += `<p><strong>Files inside:</strong> ${f.total_files || "N/A"}</p>`;
  } else if (f.type === "video") {
    html += `<p><strong>Format:</strong> ${f.format || "N/A"}</p>`;
    html += `<p><strong>Resolution:</strong> ${f.resolution || "N/A"}</p>`;
    html += `<p><strong>Video Codec:</strong> ${f.video_codec || "N/A"}</p>`;
    html += `<p><strong>Audio Codec:</strong> ${f.audio_codec || "N/A"}</p>`;
    html += `<p><strong>Duration:</strong> ${f.duration || "N/A"}s</p>`;
    html += `<p><strong>Bitrate:</strong> ${f.bitrate || "N/A"}</p>`;
    html += `<p><strong>Subtitles:</strong> ${f.subtitles || "N/A"}</p>`;
		html += `
        <video controls style="width: 100%; max-width: 400px; border-radius: 8px; margin-top: 12px; background-color: #000;">
            <source src="/preview?path=${encodeURIComponent(f.path)}" type="video/mp4">
        </video>`;
  }

  html += "</div>";
  return html;
}


function toggleFileDetails(row, index) {
	const existingPanel = row.nextElementSibling;
	if (existingPanel && existingPanel.classList.contains("detail-row")) {
		existingPanel.remove();
		return;
	}
	
	document.querySelectorAll(".detail-row").forEach(r => r.remove());
	
	const fileData = window.scannedFiles[index];
	
	const detailRow = document.createElement("tr");
	detailRow.classList.add("detail-row");
	detailRow.innerHTML = `<td colspan="3">${showFileDetails(fileData)}</td>`;
	
	row.parentNode.insertBefore(detailRow, row.nextSibling);
	
	if (fileData.gps) {
		const mapId = `detail-map-${fileData.file_name.replace(/[^a-zA-Z0-9]/g, "_")}`;
		setTimeout(() => {
			const map = L.map(mapId).setView([fileData.gps.latitude, fileData.gps.longitude], 13);
			L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map);
			L.marker([fileData.gps.latitude, fileData.gps.longitude]).addTo(map);
		}, 100)
	}
}


function displayResults(files) {
	const resultsDiv = document.getElementById("results");
	
	window.scannedFiles = files;
	
	let html = "<table>";
    
  files.forEach((f, i) => {
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
    } else if (f.type === "exe") {
			details = `Version: ${f.version || "N/A"}, Company: ${f.company || "N/A"}`;
    } else if (f.type === "archive") {
			details = `Files: ${f.total_files || "N/A"}, Format: ${f.format || "N/A"}`;
    } else if (f.type === "video") {
			details = `Resolution: ${f.resolution || "N/A"}, Codec: ${f.video_codec || "N/A"}, Duration: ${f.duration || "N/A"}s`;
    }
		
		html += `<tr class="file-row" onclick="toggleFileDetails(this, ${i})" data-file="${i}">
			<td class="file-name">${f.file_name}</td>
			<td><span class="badge badge-${f.type}">${f.type}</span></td>
			<td>${details}</td>
		</tr>`;
  });
	
	html += "</table>";
	resultsDiv.innerHTML = html;
}
