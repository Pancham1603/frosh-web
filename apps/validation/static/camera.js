let scanner = null;
let cameras = []; // Store available cameras
let eventkey = "";

function selectEvent() {
  eventName = document.getElementById("field").value;
  if (eventName == "") {
    document.getElementById("error").innerHTML = "Please select an event";
    document.getElementById("field").style.display = "block";
    document.getElementById("field").disabled = false;
    document.getElementById("event-name").innerHTML = "Select Event";
    document.getElementById("funcs").style.display = "none";
  }
  else {
    eventkey = eventName;
    document.getElementById("error").innerHTML = "";
    document.getElementById("field").disabled = true;
    document.getElementById("field").style.display = "none";
    document.getElementById("event-name").innerHTML = eventName;
    document.getElementById("funcs").style.display = "flex";
    startCamera(1);
  }
}
function getCameras() {
  Instascan.Camera.getCameras()
    .then(function (availableCameras) {
      cameras = availableCameras;
      // Display camera options
      const switchButton = document.getElementById("switch-button");
      switchButton.textContent = "Switch Camera";
      switchButton.disabled = false;

      const cameraOptions = cameras.map((camera, index) => {
        // alert(camera.name + " " + index)
        return `<option value="${index}">${camera.name}</option>`;
      });

      const cameraSelect = document.createElement("select");
      cameraSelect.innerHTML = cameraOptions.join("");
      cameraSelect.addEventListener("change", function () {
        stopCamera();
        startCamera(this.value);
      });
    })
    .catch(function (error) {
      console.error("Error getting cameras:", error);
    });
}

function startCamera(selectedCameraIndex) {
  const qrResult = document.getElementById("qr-result");
  qrResult.textContent = "Scanning...";

  const video = document.createElement("video");
  const cameraPreview = document.getElementById("camera-preview");
  cameraPreview.innerHTML = "";
  cameraPreview.appendChild(video);

  if (!selectedCameraIndex) {
    selectedCameraIndex = 1; // Use the first camera by default
  }

  const constraints = {
    video: {
      facingMode: "environment",
      deviceId: {
        exact: cameras[selectedCameraIndex].id,
      },
      facingMode: {
        exact: "environment" // Use the rear camera if available
      }
    },
  };

  // Request permission to access the camera
  navigator.mediaDevices
    .getUserMedia(constraints)
    .then(function (stream) {
      qrResult.textContent = "Camera started, scanning...";
      video.srcObject = stream;
      video.setAttribute("playsinline", true); // Required to tell iOS Safari we don't want fullscreen
      video.play();
      scanner = new Instascan.Scanner({ video: video });
      scanner.addListener("scan", function (content) {
        console.log(content);
        getPassData(content);
      });

      scanner.start(cameras[selectedCameraIndex]); // Start the selected camera
    })
    .catch(function (error) {
      switchCamera();
    });
}


// Call getCameras when the page loads
getCameras();

function stopCamera() {
  if (scanner) {
    scanner.stop();
    scanner = null;
  }
}

function getPassData(pass_id) {
  $.ajax({
    method: "POST",
    url: "/scanner/userdata",
    data: {
      pass_id: pass_id,
      event_id: document.getElementById("event-name").innerHTML
    },
    success: function (response) {
      response = JSON.parse(response)
      if (response.valid) {
        vibrateForOneSecond()
        // toastr.success(response.message)
        openModal(response.event, response.user, response.registration_id, response.image, "https://eitrawmaterials.eu/wp-content/uploads/2016/09/person-icon.png", "",pass_id)
      } else {
        toastr.error(response.message)
      }
    },
    error: function (response) {
      vibrateForOneSecond()
      toastr.error("Invalid Pass");
    }
  });
}

function validate_pass(pass_id) {
  $.ajax({
    method: "POST",
    url: "/scanner/userdata/validate",
    data: {
      pass_id: pass_id,
      event_id: document.getElementById("event-name").innerHTML
    },
    success: function (response) {
      toastr.success(response)
      // console.log(response['username'], response['registration_id'], response['event']);
    },
    error: function (response) {
      toastr.error("Invalid Pass");
    }
  });
}


let facingMode = "environment"; // Default camera facing mode

let currentCameraIndex = 0;

function switchCamera() {
  if (cameras.length > 1) {
    const selectedCameraIndex = (currentCameraIndex + 1) % cameras.length;
    currentCameraIndex = selectedCameraIndex;
    stopCamera();
    startCamera(selectedCameraIndex);
  }
}
