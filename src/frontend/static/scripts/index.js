function openTab(evt, tabName) {
  var i, tabcontent, tablinks;

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
  var i, resumes, viewlinks;

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
  const resume_yaml = document.getElementById("original_resume").value;
  console.log(resume_yaml);
  fetch("/api/resume/validate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      "resume": resume_yaml
    })
  })
    .then(response => response.json())
    .then(data => {
      result = data.result;
      if (result == "invalid") {
        alert(`There was an error validating your resume, error ${data.details}`);
      } else if (result === "valid") {
        alert("Your resume looks good!");
      } else {
        alert("An unknown error has occured");
      }
    })
    .catch(error => {
      console.error(error);
    })
}
