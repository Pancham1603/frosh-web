
toastr.options = {
    "closeButton": true,
    "newestOnTop": true,
    "progressBar": true,
    "positionClass": "toast-top-full-width",
    "preventDuplicates": false,
    "onclick": null,
    "showDuration": "300",
    "hideDuration": "1000",
    "timeOut": "2000",
    "extendedTimeOut": "1000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
    
}


function openModal(title, name, id, imageUrl, addToCalender, book, pass_id) {
    document.getElementById('eventModal').style.display = 'block';
    document.getElementById('title').innerHTML = title;
    document.getElementById('description').innerHTML = "";
    document.getElementById('description').innerHTML += "<b>Name: </b>" + name + "<br>";
    document.getElementById('description').innerHTML += "<b>Id: </b>" + id + "<br>";
    document.getElementById('imageUrl').src = imageUrl;


    console.log("pass_id" + pass_id)
    document.getElementById('book').onclick = function () {
        validate_pass(pass_id)
        delayExecutionByOneSecond();
    }
    document.getElementById('calender').onclick = function () {
        closeModal()
        delayExecutionByOneSecond();
    }


    // document.getElementById('calender').innerHTML = "<i class='fa - regular fa - circle - xmark'></i>&nbsp; Reject";
    // document.getElementById('book').innerHTML = `<i class="fa-solid fa-check white"></i>&nbsp;Accept`
    document.getElementById('book').classList.add("booked");
    document.getElementById('calender').classList.add("booked");

}

// Function to close the modal
function closeModal() {
    document.getElementById('eventModal').style.display = 'none';

}
//close modal when clicked outside
window.addEventListener('click', function (event) {
    if (event.target === document.getElementById('eventModal')) {
        closeModal();
    }
});

window.addEventListener('touchstart', function (event) {
    if (event.target === document.getElementById('eventModal')) {
        closeModal();
    }
});


function vibrateForOneSecond() {
    // Check if the Vibration API is supported by the browser
    if ("vibrate" in navigator) {
        // Vibrate for 200ms (shorter duration to avoid annoyance)
        navigator.vibrate(200);

        // Check if the Audio API is supported by the browser
        if ("Audio" in window) {
            var beepSound = new Audio('../static/beep.mp3');
            beepSound.play().catch(error => {
                // Autoplay is blocked, handle the error here
                alert("Audio playback was blocked. Please click on the page to start audio playback.");
                console.error("Audio playback was blocked:", error);
            });
        } else {
            // Fallback if Audio API is not supported
            console.log("Audio API is not supported in this browser.");
        }
    } else {
        // Fallback if Vibration API is not supported
        console.log("Vibration API is not supported in this browser.");
    }
}