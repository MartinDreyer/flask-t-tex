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

    uploadedFiles.push(fileInput.files[0]);

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

    console.log(uploadedFiles);

    if (!fileList) {
      fileList = document.createElement("ul");
      fileList.className = "filelist";
      content.appendChild(fileList);
    }

    if (files.length > 1) {
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
    if (uploadedFiles.length > 1 && uploadedFiles.length < 5) {
      const formData = new FormData();

      uploadedFiles.forEach((file, index) => {
        // Post files to '/upload'
      });
    }
  } catch (error) {
    console.error(error);
  }
};
