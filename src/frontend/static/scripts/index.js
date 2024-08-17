function openTab(evt, tabName) {
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
  evt.currentTarget.className += " active";
}

// Open default tab
document.getElementById("defaultOpen").click();

function openResume(evt, resumeId) {
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

  // Show the selected resume, and add an "active" class to the button that opened the resume
  document.getElementById(resumeId).style.display = "block";
  evt.currentTarget.className += " active";
}

// Open default resume
document.getElementById("defaultResume").click();

function validateResume() {
  const resumeYaml = document.getElementById("original-resume-editor").value;
  const errorViewer = document.getElementById("original-resume-error-viewer");
  const validateButton = document.getElementById("validate-button");
  validateButton.disabled = true;
  errorViewer.value = "Sending request to server..."
  fetch("/api/resume/validate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      "resume": resumeYaml
    })
  })
    .then(response => response.json())
    .then(data => {
      result = data.result;
      console.log(data);
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
      validateButton.disabled = false;
    })
    .catch(error => {
      let errorMsg = "There is some trouble connecting to the server";
      errorMsg += `\nError: ${error}`
      errorViewer.value = errorMsg;
      validateButton.disabled = false;
    })
}
