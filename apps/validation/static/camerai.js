document.getElementById("funcs").style.display = "none";
let activeCameraId = null;
function selectEvent() {
    eventName = document.getElementById("field").value;
    if (eventName == "") {
        document.getElementById("error").innerHTML = "Please select an event";
        document.getElementById("field").style.display = "block";
        document.getElementById("event-name").innerHTML = "Select Event";
        document.getElementById("funcs").style.display = "none";
    }
    else {
        eventkey = eventName;
        document.getElementById("error").innerHTML = "";
        document.getElementById("field").style.display = "none";
        document.getElementById("event-name").innerHTML = eventName;
        document.getElementById("funcs").style.display = "block";
        initializeScanner();
    }
}


function validate_pass(pass_id) {
    $.ajax({
        method: "POST",
        url: "/scanner/userdata/validate",
        data: {
            pass_id: pass_id
        },
        success: function (response) {
            vibrateForOneSecond()
            toastr.success(response)
            // console.log(response['username'], response['registration_id'], response['event']);
        },
        error: function (response) {
            vibrateForOneSecond()
            toastr.error("Invalid Pass");
        }
    });
}
// Function to start the camera stream
function startCamera() {
    navigator.mediaDevices.getUserMedia({
        video: {
            deviceId: activeCameraId ? { exact: activeCameraId } : undefined
        }
    }).then(function (stream) {
        const scannerElement = document.getElementById("scanner");
        scannerElement.srcObject = stream;
        scannerElement.play();

        // Load the latest version of ZXing dynamically from a CDN
        const script = document.createElement('script');
        script.src = 'https://unpkg.com/@zxing/library@latest';
        script.onload = function () {
            const codeReader = new ZXing.BrowserQRCodeReader();

            function scanQRCode() {
                codeReader.decodeOnceFromVideoDevice(activeCameraId, scannerElement)
                    .then(function (result) {
                        const code = result.text;
                        //alert(`QR Code Scanned: ${code}`);
                        getPassData(code);
                        //  scanQRCode(); // Call the function again for continuous scanning
                    })
                    .catch(function (error) {
                        console.error('Error decoding QR code:', error);
                        scanQRCode(); // Call the function again for continuous scanning
                    });
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
                            openModal(response.event, response.user, response.registration_id, response.image, "https://eitrawmaterials.eu/wp-content/uploads/2016/09/person-icon.png", "", pass_id)
                        } else {
                            toastr.error("Pass has already been used");
                        }
                        setTimeout(function () {
                            // Put the code you want to delay here
                            scanQRCode();
                            // You can place any code that needs to be delayed inside this function
                        }, 2000);

                    },
                    error: function (response) {
                        console
                        vibrateForOneSecond()
                        toastr.error("Invalid Pass");
                        setTimeout(function () {
                            // Put the code you want to delay here
                            scanQRCode();
                            // You can place any code that needs to be delayed inside this function
                        }, 2000);
                    }
                });
            }
            //close modal when clicked outside
            window.addEventListener('click', function (event) {
                if (event.target === document.getElementById('eventModal')) {
                    closeModal();
                    scanQRCode();
                }
            });

            window.addEventListener('touchstart', function (event) {
                if (event.target === document.getElementById('eventModal')) {
                    closeModal();
                    scanQRCode();
                }
            });
            scanQRCode(); // Start the continuous scanning process
        };
        document.head.appendChild(script);
    }).catch(function (error) {
        console.error('Error accessing camera:', error);
    });
}


// Function to stop the camera stream
function stopCamera() {
    const scannerElement = document.getElementById("scanner");
    if (scannerElement.srcObject) {
        const tracks = scannerElement.srcObject.getTracks();
        tracks.forEach(function (track) {
            track.stop();
        });
        scannerElement.srcObject = null;
    }
    //document.getElementById('startButton').style.display = 'block'; // Show the start button again
}

// Initialize the QR scanner
function initializeScanner() {
    // Get available cameras and start the camera stream when the page is loaded
    navigator.mediaDevices.enumerateDevices()
        .then(function (devices) {
            const cameras = devices.filter(device => device.kind === 'videoinput');
            if (cameras.length > 0) {
                activeCameraId = cameras[0].deviceId; // Use the first available camera
                startCamera();

                // Add buttons to switch between cameras
                const cameraButtonsDiv = document.getElementById('cameraButtons');
                cameras.forEach(function (camera) {
                    const button = document.createElement('button');
                    button.textContent = `Switch to ${camera.label}`;
                    button.addEventListener('click', function () {
                        activeCameraId = camera.deviceId;
                        stopCamera();
                        startCamera();
                    });
                    cameraButtonsDiv.appendChild(button);
                });
            } else {
                console.error('No cameras found.');
            }
        }).catch(function (error) {
            console.error('Error accessing cameras:', error);
        });
}