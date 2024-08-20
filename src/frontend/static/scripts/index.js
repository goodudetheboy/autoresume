function startup() {
  resumeAction("render", "original");
}

function openTab(tabName) {
  let i, tabcontent, tablinks;

  // Hide all tab contents
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Remove active class from all tab links
  tablinks = document.getElementsByClassName("tablink");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(tabName).style.display = "block";
  document.getElementById(`${tabName}-editor-tab-button`).className += " active"
}

// Open default tab
document.getElementsByClassName("defaultOpen")[0].click();

function openResume(type) {
  let i, resumes, viewlinks;

  // Hide all resume embeds
  resumes = document.getElementsByTagName("embed");
  for (i = 0; i < resumes.length; i++) {
    resumes[i].style.display = "none";
  }

  // Remove active class from all view links
  viewlinks = document.getElementsByClassName("viewlink");
  for (i = 0; i < viewlinks.length; i++) {
    viewlinks[i].className = viewlinks[i].className.replace(" active", "");
  }

  const resumeViewer = document.getElementById(`${type}-resume-pdf`);

  // Show the selected resume, and add an "active" class to the button that opened the resume
  resumeViewer.style.display = "block";
  document.getElementById(`${type}-viewer-tab-button`).className += " active";

  // Set download link
  const downloadBtn = document.getElementById('download-link');
  if (resumeViewer.src) {
    const companyName = document.getElementById("company-name").value;
    // Preprocess resume name
    let resumeName = type === "tailored" ? companyName : "original";
    resumeName = resumeName.trim().replace(/\s+/g, '-').toLowerCase();

    // Set resume download link
    downloadBtn.href = resumeViewer.src;
    downloadBtn.download = `${resumeName}-resume.pdf`;
    downloadBtn.style.display = "inline-block";
  } else {
    downloadBtn.style.display = "none";
  }
}

// Open default resume
document.getElementsByClassName("defaultResume")[0].click();

function disableControlButtons(status) {
  const controlButtons = document.getElementsByClassName("tab-button");
  for (let i in controlButtons) {
    controlButtons[i].disabled = status
  }
}

function resumeAction(action, type) {
  // action can be validate or generate
  // type can be original or tailored
  const resumeYaml = document.getElementById(`${type}-resume-editor`).value;
  const errorViewer = document.getElementById(`${type}-resume-error-viewer`);
  disableControlButtons(true);
  errorViewer.value = "Sending request to server..."
  fetch(`/api/resume/${action}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      "resume": resumeYaml,
    })
  })
    .then(response => {
      if (action === "render" && response.status === 201) {
        return response.blob();
      }
      return response.json();
    })
    .then(data => {
      if (data.type === "application/pdf") {
        const pdfUrl = URL.createObjectURL(data);
        const resumeViewer = document.getElementById(`${type}-resume-pdf`);
        resumeViewer.src = pdfUrl;
        errorViewer.value = "Your resume is generated! 🤩🤩🤩🤩🤩"
        openResume(type);
      } else {
        result = data.result;
        if (result == "invalid") {
          let errorMsg = "There was an error validating your resume ❌❌❌❌❌";
          errorMsg += `\nError: ${data.error}`;
          errorMsg += "\nDetails:";
          for (let i in data.details) {
            errorMsg += `\n\t${data.details[i]}`;
          }
          errorViewer.value = errorMsg;
        } else if (result === "valid") {
          errorViewer.value = "Your resume looks good! ✅✅✅✅✅"
        } else {
          errorViewer.value = "An unknown error has occured 💀"
        }
      }
      disableControlButtons(false);
    })
    .catch(error => {
      let errorMsg = "There is some trouble connecting to the server";
      errorMsg += `\nError: ${error}`
      errorViewer.value = errorMsg;
      disableControlButtons(false);
    })
}

function tailorResume() {
  const originalResumeYaml = document.getElementById("original-resume-editor").value;
  const companyName = document.getElementById("company-name").value;
  const jobDescription = document.getElementById("job-description-editor").value;
  const errorViewer = document.getElementById("tailored-resume-error-viewer");
  const keywordsList = document.getElementById("tailored-tab-keywords");
  if (!companyName || !jobDescription) {
    return;
  }
  disableControlButtons(true);
  fetch(`/api/resume/tailor`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      "resume": originalResumeYaml,
      "job_description": jobDescription
    })
  })
    .then(response => response.json())
    .then(data => {
      const tailored_resume = data.tailored_resume;
      document.getElementById("tailored-resume-editor").value = tailored_resume;
      errorViewer.value = "Your resume has been tailored ⭐⭐⭐⭐⭐\n Now rendering it for you..."
      let keywords = data.keywords.join(", ");
      keywordsList.innerText = `Keywords: ${keywords}`
      openTab("Tailored");
      resumeAction("render", "tailored");
    })
    .catch(error => {
      let errorMsg = "There is some trouble connecting to the server, please try again";
      errorMsg += `\nError: ${error}`
      errorViewer.value = errorMsg;
      disableControlButtons(false);
    });
}

let prompt = "";

document
  .getElementById("answer-copy-prompt-button")
  .addEventListener('click', function (event) {
    event.preventDefault();
    if (prompt) {
      navigator.clipboard.writeText(prompt);
      Toastify({
        text: "Copied!",
        className: "info-toast",
        position: "center",
      }).showToast();
    } else {
      Toastify({
        text: "Click Answer first",
        className: "error-toast",
        position: "center",
      }).showToast();
    }
  });

function answerAppQuestion(event) {
  event.preventDefault();
  const jobDescription = document.getElementById("job-description-editor").value;
  const originalResumeYaml = document.getElementById("original-resume-editor").value;
  const question = document.getElementById("answer-question-editor").value;

  const answerViewer = document.getElementById("answer-answer-viewer");
  const analysisViewer = document.getElementById("answer-analysis-viewer");

  if (!jobDescription || !originalResumeYaml) {
    Toastify({
      text: "Missing original resume or job description!",
      className: "error-toast",
      position: "center",
    }).showToast();
    return;
  }
  disableControlButtons(true);
  fetch(`/api/resume/answer`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      "resume": originalResumeYaml,
      "job_description": jobDescription,
      "question": question
    })
  })
    .then(response => response.json())
    .then(data => {
      answerViewer.value = data.answer;
      analysisViewer.value = data.analysis;
      disableControlButtons(false);
      prompt = data.prompt;
    })
    .catch(error => {
      let errorMsg = "There is some trouble connecting to the server, please try again";
      errorMsg += `\nError: ${error}`
      analysisViewer.value = errorMsg;
      disableControlButtons(false);
    });
}