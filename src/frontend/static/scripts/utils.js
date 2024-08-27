
function toast(text, type = "info") {
  Toastify({
    text: text,
    className: `${type}-toast`,
    position: "center",
  }).showToast();
}
