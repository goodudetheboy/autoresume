document.addEventListener("DOMContentLoaded", () => {
  initializeDefaultPresets();
  loadPresets();
});

const defaultPresets = {
  "Application question": "",
  "Write cold email": "Help me draft an email to cold email to ask for more information and possibly an interview about the application with the given job description."
};

function initializeDefaultPresets() {
  // Initialize the textarea with the text of the first default preset
  updateTextarea();
}

function addPreset() {
  const presetNameInput = document.getElementById("answer-question-preset-name");
  const presetName = presetNameInput.value.trim();
  const presetText = document.getElementById("answer-question-editor").value.trim();

  if (presetName === "" || presetText === "") return;

  const select = document.getElementById("answer-question-preset");

  // Prevent adding duplicates
  if (Array.from(select.options).some(option => option.value === presetName)) {
    toast(`Can't add duplicate preset with name "${presetName}".`, "error");
    return;
  }

  // Create a new option element
  const newOption = document.createElement("option");
  newOption.value = presetName;
  newOption.textContent = presetText;

  // Add the new option to the select element
  select.appendChild(newOption);

  // Set the newly added option as the selected option
  select.value = presetName;

  // Save to local storage
  savePreset(presetName, presetText);

  presetNameInput.value = "";
  toast(`Successfully added preset with name "${presetName}". Enjoy, nerd.`, "success");
}

function removePreset() {
  const select = document.getElementById("answer-question-preset");
  const selectedOption = select.options[select.selectedIndex];

  // Do not remove the default options
  if (selectedOption && !(selectedOption.value in defaultPresets)) {
    select.removeChild(selectedOption);
    removePresetFromStorage(selectedOption.value);
    toast(`Succesfully removed preset "${selectedOption.value}".`, "info");
  } else {
    toast("Can't remove default preset, cuh.", "error");
  }
}

function savePreset(name, text) {
  const presets = JSON.parse(localStorage.getItem("presets")) || {};
  presets[name] = text;
  localStorage.setItem("presets", JSON.stringify(presets));
}

function removePresetFromStorage(name) {
  const presets = JSON.parse(localStorage.getItem("presets"));
  if (presets) {
    delete presets[name];
    localStorage.setItem("presets", JSON.stringify(presets));
  }
}

function loadPresets() {
  const presets = JSON.parse(localStorage.getItem("presets"));
  if (presets) {
    const select = document.getElementById("answer-question-preset");
    for (const preset in presets) {
      const option = document.createElement("option");
      option.value = preset;
      option.textContent = preset;
      select.appendChild(option);
    }
  }
}

function updateTextarea() {
  const select = document.getElementById("answer-question-preset");
  const selectedPreset = select.value;

  const presets = JSON.parse(localStorage.getItem("presets")) || {};
  const presetText = presets[selectedPreset] || defaultPresets[selectedPreset] || "";

  document.getElementById("answer-question-editor").value = presetText;
}
