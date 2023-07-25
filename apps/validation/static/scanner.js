
function openModal(title, name, id,phonenumber, imageUrl, addToCalender, book) {
    document.getElementById('eventModal').style.display = 'block';
    document.getElementById('title').innerHTML = title;
    document.getElementById('description').innerHTML = "";
    document.getElementById('description').innerHTML += "<b>Name:</b>"+name+"<br>";
    document.getElementById('description').innerHTML += "<b>Id:</b>"+id+"<br>";
    document.getElementById('description').innerHTML += "<b>Phone Number:</b>"+phonenumber+"<br>";
    document.getElementById('imageUrl').src = imageUrl;



    document.getElementById('book').onclick = function () {

    }
    document.getElementById('calender').onclick = function () {
    }


    document.getElementById('calender').innerHTML = "<i class='fa - regular fa - circle - xmark'></i>&nbsp; Reject";
    document.getElementById('book').innerHTML = `<i class="fa-solid fa-check white"></i>&nbsp;Accept`
    document.getElementById('book').classList.add("booked");
    document.getElementById('calender').classList.add("booked");

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