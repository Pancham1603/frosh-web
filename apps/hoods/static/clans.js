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

const cards = document.querySelectorAll('.card');
const clearBtn = document.getElementById('clearBtn');
const submitBtn = document.getElementById('submitBtn');
let preferenceOrder = [];

cards.forEach((card, index) => {
    card.addEventListener('click', () => {
        if (card.classList.contains('selected')) {
            card.classList.remove('selected');
            preferenceOrder = preferenceOrder.filter(id => id !== card.id);
            updatePreferenceNumbers();
        } else {
            card.classList.add('selected');
            preferenceOrder.push(card.id);
            updatePreferenceNumbers();
        }
    });
});

function updatePreferenceNumbers() {
    cards.forEach((card, index) => {
        const prefNumber = card.querySelector('.pref-number');

        const prefIndex = preferenceOrder.indexOf(card.id);

        if (prefIndex !== -1) {
            prefNumber.textContent = (prefIndex + 1).toString();
              prefNumber.style.visibility = "visible"
        } else {
            prefNumber.textContent = '';
              prefNumber.style.visibility = "hidden"
        }

      
    });
}

clearBtn.addEventListener('click', () => {
    cards.forEach(card => {
        card.classList.remove('selected');
    });
    preferenceOrder = [];
    updatePreferenceNumbers();
});

submitBtn.addEventListener('click', () => {
    if (preferenceOrder.length !== 4) {
        toastr.warning('Please select preferences for all hoods');
    } else {
        toastr.info(preferenceOrder.join(', ')+'<button type="button" onclick="toastr.close()">Edit</button> <button type="button" onclick="submitPreferences()">Submit</button>' , 'Confirm Order:');
    }
});

updatePreferenceNumbers();

function submitPreferences() {
    $.ajax({
        method: "POST",
        url: "/hoods/initiation/",
        timeout: 20000,
        data: {
            'preferences':preferenceOrder.join(', '),
            'csrfmiddlewaretoken': document.getElementsByName('csrfmiddlewaretoken')[0].value	
        },
        success: function (response) {
            let res = JSON.parse(response).status;
            if (res) {
                toastr.success(JSON.parse(response).message);
                // document.getElementById("spinbox").style.display = "none"
            }
            else {
                toastr.error(JSON.parse(response).message);
                // document.getElementById("spinbox").style.display = "none"
            }

        },
        error: function (xhr, textStatus, errorThrown) {
            // document.getElementById("spinbox").style.display = "none";
            toastr.error("Something went wrong, please try again later");
        }
    });
}