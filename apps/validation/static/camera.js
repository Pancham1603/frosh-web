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
    startCamera(0);
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
        alert(camera.name + " " + index)
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

function startCamera() {
  const qrResult = document.getElementById("qr-result");
  qrResult.textContent = "Scanning...";

  const video = document.createElement("video");
  const cameraPreview = document.getElementById("camera-preview");
  cameraPreview.innerHTML = "";
  cameraPreview.appendChild(video);

  const constraints = {
    video: true
  };

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

      // Switch camera for iOS devices
      if (/iPhone|iPad|iPod/.test(navigator.userAgent)) {
        const track = stream.getVideoTracks()[0];
        if (track.getCapabilities && track.getCapabilities().facingMode) {
          const facingMode = track.getCapabilities().facingMode;
          const selectedCameraIndex = facingMode === "environment" ? 1 : 0;
          scanner.start(cameras[selectedCameraIndex]);
          currentCameraIndex = selectedCameraIndex;
        } else {
          scanner.start(cameras[currentCameraIndex]);
        }
      } else {
        // For non-iOS devices, use the selected camera index
        scanner.start(cameras[currentCameraIndex]);
      }
    })
    .catch(function (error) {
      console.error("Error accessing the camera:", error);
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
      pass_id: pass_id
    },
    success: function (response) {
      console.log(response)
      //alert(response)
      vibrateForOneSecond()
      response = JSON.parse(response)
      openModal(response.event, response.username, response.registration_id, "", "https://eitrawmaterials.eu/wp-content/uploads/2016/09/person-icon.png", "")
      // console.log(response['username'], response['registration_id'], response['event']);
    },
    error: function (response) {
      vibrateForOneSecond()
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
