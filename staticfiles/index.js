function openModal(title, description, time, location, imageUrl, addToCalender, book) {
    document.getElementById('eventModal').style.display = 'block';
    document.getElementById('title').innerHTML = title;
    document.getElementById('description').innerHTML = description;
    document.getElementById('time').innerHTML = "&nbsp;" + time;
    document.getElementById('location').innerHTML = "&nbsp;" + location;
    document.getElementById('imageUrl').src = imageUrl;
    document.getElementById('link').href = addToCalender;

    document.getElementById('error').innerHTML = ""


    document.getElementById('book').onclick = function () {
        let slot = document.getElementById('field').value
        console.log("slot" + slot)
        if (slot == '') {
           // document.getElementById('error').innerHTML = "Please select a slot"
            toastr.error("Select a slot");
            return;
        }
        //slot has the value
        document.getElementById("spinbox").style.display = "flex"
        $.ajax({
            method: "POST",
            url: "register/" + title + '@Frosh23',
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
    }
    else {
        document.getElementById('book').classList.remove("booked");
        document.getElementById('calender').classList.remove("booked");
        document.getElementById('calender').innerHTML = "<i class='fa-regular fa-calendar-plus white'></i>";
        document.getElementById('book').innerHTML = `Book Now!`
        document.getElementById('link').style.width = "unset";
    }
}

// Function to close the modal
function closeModal() {
    document.getElementById('eventModal').style.display = 'none';

}
//close modal when clicked outside
window.onclick = function (event) {
    if (event.target == document.getElementById('eventModal')) {
        closeModal();
    }
}
