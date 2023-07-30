function openModal(title, description, time, location, slots, imageUrl, addToCalender, book) {

    document.getElementById('title').innerHTML = title;
    document.getElementById('description').innerHTML = description;
    document.getElementById('time').innerHTML = "&nbsp;" + time;
    document.getElementById('location').innerHTML = "&nbsp;" + location;
    document.getElementById('imageUrl').src = imageUrl;
    document.getElementById('link').href = addToCalender;
    document.getElementById('error').innerHTML = ""
    document.getElementById('field').innerHTML = `<option value="">Select one...</option>`;
    console.log(imageUrl)
    if (slots) {
        console.log(slots)
        let code = slots.substring(slots.indexOf(',') + 1).trim()
        let timer = slots.substring(0, slots.indexOf(','))
        console.log(code)

        document.getElementById('field').innerHTML += `<option value="register/` + title + `@Frosh23">` + time + `</option>`
        document.getElementById('field').innerHTML += `  <option value="register/` + title + `@Frosh23/` + code + `">` + timer + `</option>`
        document.getElementById('slots').style.display = "block"
        document.getElementById('details').style.marginTop = "0px"
    }
    else {
        document.getElementById('slots').style.display = "none"
        document.getElementById('details').style.marginTop = "20px"
    }

    document.getElementById('book').onclick = function () {
        let urls = "register/" + title + '@Frosh23'
        if (slots) {
            let slot = document.getElementById('field').value
            console.log("slot" + slot)
            if (slot == '') {

                document.getElementById('error').innerHTML = "Please select a slot"
                toastr.error("Select a slot");
                return;
            }
            urls = slot;
        }
        //slot has the value
        document.getElementById("spinbox").style.display = "flex"
        $.ajax({
            method: "POST",
            url: urls,
            timeout: 10000,
            success: function (response) {
                let res = JSON.parse(response).status;
                if (res) {
                    let qr = JSON.parse(response).pass_qr
                    document.getElementById('imageUrl').src = qr
                    document.getElementById('calender').innerHTML = "<i class='fa-regular fa-calendar-plus white'></i>&nbsp; Reminder";
                    document.getElementById('book').innerHTML = `<i class="fa-regular fa-square-check white"></i>&nbsp;Booked`
                    document.getElementById('link').style.width = "45%";
                    document.getElementById('book').classList.add("booked");
                    document.getElementById('calender').classList.add("booked");
                    $("#event-grid").load(window.location.href + " #event-grid");
                    document.getElementById("spinbox").style.display = "none"
                }
                else {
                    // Set the options that I want
                    toastr.options = {
                        "closeButton": true,
                        "newestOnTop": true,
                        "progressBar": true,
                        "positionClass": "toast-top-right",
                        "preventDuplicates": true,
                        "onclick": null,
                        "showDuration": "300",
                        "hideDuration": "1000",
                        "timeOut": "5000",
                        "extendedTimeOut": "1000",
                        "showEasing": "swing",
                        "hideEasing": "linear",
                        "showMethod": "fadeIn",
                        "hideMethod": "fadeOut"
                    }

                    toastr.error(JSON.parse(response).message);
                    document.getElementById("spinbox").style.display = "none"
                }

            },
            error: function (xhr, textStatus, errorThrown) {
                document.getElementById("spinbox").style.display = "none";
                toastr.error("Something went wrong, please try again later");
            }

        });
    }


    if (book) {
        document.getElementById('calender').innerHTML = "<i class='fa-regular fa-calendar-plus white'></i>&nbsp; Reminder";
        document.getElementById('book').innerHTML = `<i class="fa-regular fa-square-check white"></i>&nbsp;Booked`
        document.getElementById('link').style.width = "45%";
        document.getElementById('book').classList.add("booked");
        document.getElementById('calender').classList.add("booked");
        document.getElementById('imageUrl').src = imageUrl
    }
    else {
        document.getElementById('book').classList.remove("booked");
        document.getElementById('calender').classList.remove("booked");
        document.getElementById('calender').innerHTML = "<i class='fa-regular fa-calendar-plus white'></i>";
        document.getElementById('book').innerHTML = `Book Now!`
        document.getElementById('link').style.width = "unset";
    }
    document.getElementById('eventModal').style.display = 'block';

}

// Function to close the modal
function closeModal() {
    document.getElementById('eventModal').style.display = 'none';

}

window.addEventListener('click', function (event) {
    if (event.target == document.getElementById('eventModal')) {
        closeModal();
    }
    else if (event.target == document.getElementById('customTicketModal')) {
        closeCustomModal();
    }
});

window.addEventListener('touchstart', function (event) {
    if (event.target == document.getElementById('eventModal')) {
        closeModal();
    }
    else if (event.target == document.getElementById('customTicketModal')) {
        closeCustomModal();
    }
});

window.addEventListener('load', function (event) {
    const scrollableDiv = document.getElementById('scrollableDiv');

    scrollableDiv.addEventListener('wheel', function (event) {
        // Check if the mouse is over the scrollableDiv
        const rect = scrollableDiv.getBoundingClientRect();
        const mouseX = event.clientX;
        if (mouseX >= rect.left && mouseX <= rect.right) {
            event.preventDefault(); // Prevent vertical scrolling

            const scrollSpeed = 50; // Adjust the scrolling speed as needed
            scrollableDiv.scrollLeft += event.deltaY > 0 ? scrollSpeed : -scrollSpeed;
        }
    });
}
);