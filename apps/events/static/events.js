function toggleMobileMenu() {
    var mobileMenu = document.getElementById("mobileMenu");
    mobileMenu.style.display = mobileMenu.style.display === "block" ? "none" : "block";
}

function openModal(title, description, time, location, imageUrl, addToCalender, book) {
    document.getElementById('eventModal').style.display = 'block';
    document.getElementById('title').innerHTML = title;
    document.getElementById('description').innerHTML = description;
    document.getElementById('time').innerHTML = time;
    document.getElementById('location').innerHTML = location;
    document.getElementById('imageUrl').src = imageUrl;
    document.getElementById('link').href = addToCalender;

    
    document.getElementById('book').onclick = function () {
        $.ajax({
          method: "POST",
          url: "register/"+title+'@Frosh23',
          success: function (response) {
			let qr = JSON.parse(response).pass_qr
            document.getElementById('imageUrl').src = qr
            document.getElementById('calender').innerHTML = "<i class='fa-regular fa-calendar-plus white'></i>&nbsp; Reminder";
            document.getElementById('book').innerHTML = `<i class="fa-regular fa-square-check white"></i>&nbsp;Booked`
            document.getElementById('link').style.width = "45%";
            document.getElementById('book').classList.add("booked");
            document.getElementById('calender').classList.add("booked");
            $( "#event-grid" ).load(window.location.href + " #event-grid" );
          },
        });
    }


    if (book) {
        document.getElementById('calender').innerHTML = "<i class='fa-regular fa-calendar-plus white'></i>&nbsp; Reminder";
        document.getElementById('book').innerHTML = `<i class="fa-regular fa-square-check white"></i>&nbsp;Booked`
        document.getElementById('link').style.width = "45%";
        document.getElementById('book').classList.add("booked");
        document.getElementById('calender').classList.add("booked");
    }
    else{
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

