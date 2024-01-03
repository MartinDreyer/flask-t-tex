const uploadedFiles = [];

const replaceExtension = (fileName) => {
  try {
    const parts = fileName.split(".");
    if (parts.length > 1) {
      parts[parts.length - 1] = "srt";

      return parts.join(".");
    }
  } catch (error) {
    console.error(error);
  }
};

const checkExtension = (fileName) => {
  try {
    const parts = fileName.split(".");
    // Create allowed files in config and check those
    if (
      (parts[parts.length - 1] == "wav") |
      (parts[parts.length - 1] == "mp3") |
      (parts[parts.length - 1] == "mp4")
    ) {
      return true;
    } else {
      return false;
    }
  } catch (error) {
    console.error(error);
  }
};

const handleDragOver = (event) => {
  try {
    event.preventDefault();
    event.dataTransfer.dropEffect = "copy";
  } catch (error) {
    console.error(error);
  }
};

const handleDrop = (event) => {
  try {
    event.preventDefault();
    const fileInput = document.getElementById("fileInput");
    const dropArea = document.getElementById("dropArea");

    fileInput.files = event.dataTransfer.files;
    dropArea.style.border = "2px dashed #ccc";

    if (checkExtension(fileInput.files[0].name)) {
      displayFileNames(fileInput.files);
    } else {
      alert("Forkert filtype - upload mp3, mp4 eller wav");
    }
  } catch (error) {
    console.error(error);
  }
};

const handleFileSelection = (event) => {
  try {
    event.preventDefault();
    const fileInput = document.getElementById("fileInput");
    const dropArea = document.getElementById("dropArea");
    fileInput.files = event.target.files;

    if (uploadedFiles.length < 5) {
      uploadedFiles.push(fileInput.files[0]);
    } else {
      alert("Du kan maksimalt uploade fem filer.");
      return;
    }

    dropArea.style.border = "2px dashed #ccc";

    if (checkExtension(fileInput.files[0].name)) {
      displayFileNames(fileInput.files);
    } else {
      alert("Forkert filtype - upload mp3, mp4 eller wav");
    }
  } catch (error) {
    console.error(error);
  }
};

const addTranscribeButton = () => {
  const button = document.getElementById("transcribe-button");
  if (button == null) {
    const button = document.createElement("button");
    button.id = "transcribe-button";
    button.innerText = "Transkribér";

    button.addEventListener("click", () => submitForm());

    const content = document.getElementById("files");
    content.appendChild(button);
  } else {
    return;
  }
};

const displayFileNames = (files) => {
  try {
    const content = document.getElementById("files");
    let fileList = content.querySelector(".filelist");

    if (!fileList) {
      fileList = document.createElement("ul");
      fileList.className = "filelist";
      content.appendChild(fileList);
    }

    if (files.length > 1 && files.length < 5) {
      files.forEach((el) => {
        const filename = el.name;
        const listElement = document.createElement("li");
        listElement.innerText = filename;
        fileList.appendChild(listElement);
      });
    } else {
      const filename = files[0].name;
      const listElement = document.createElement("li");
      listElement.innerText = filename;
      fileList.appendChild(listElement);
    }

    addTranscribeButton();
  } catch (error) {
    console.error(error);
  }
};

const submitForm = () => {
  try {
    if (uploadedFiles.length >= 1 && uploadedFiles.length <= 5) {
      const formData = new FormData();

      const loader = document.getElementById("loader")
      const formContainer = document.getElementById("upload-form-container")
      loader.style.display = "flex"
      formContainer.style.display = "none"

      // Append each file to the formData object
      uploadedFiles.forEach((file, index) => {
        formData.append(`file${index}`, file);
      });

      // Make a single POST request with the formData containing all files
      fetch("/upload", {
        method: "POST",
        body: formData,
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          loader.style.display = "none"
          formContainer.style.display = "flex"
          window.location.href = response.url;

        })
        .catch((error) => {
          console.error("Error:", error);
        });
    } else {
      console.log("Invalid number of files");
    }
  } catch (error) {
    console.error("An error occurred:", error);
  }
};
