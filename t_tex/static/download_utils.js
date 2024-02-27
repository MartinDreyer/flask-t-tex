const download_srt = (id, title) => {
  const body = document.getElementById(id).innerText;
  const blob = new Blob([body], { type: "text/plain" });

  // Create a download link
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = title + ".srt";

  // Trigger a click on the link to start the download
  link.click();
};

const toggle_body = (id) => {
  const body = document.getElementById(id);
  const button = document.getElementById("button_" + id);
  if (!body.style.display.length || body.style.display == "none") {
    body.style.display = "block";
    button.innerText = "Skjul";
  } else if (body.style.display.length) {
    body.style.display = "none";
    button.innerText = "Vis";
  }
};
