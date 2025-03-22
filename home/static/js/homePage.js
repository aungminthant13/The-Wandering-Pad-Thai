document.addEventListener('DOMContentLoaded', function () {
    const startDateInput = document.getElementById('startDate');
    const returnDateInput = document.getElementById('returnDate');
    const tripDurationValue = document.getElementById('tripDurationValue');
    const getStartedBtn = document.getElementById('getStartedBtn');
    const tripForm = document.getElementById('tripForm');

    // Set min date for both inputs to today
    const today = new Date();
    const todayFormatted = today.toISOString().split('T')[0];
    startDateInput.min = todayFormatted;
    returnDateInput.min = todayFormatted;

    // Function to calculate trip duration
    function calculateDuration() {
        const startDate = new Date(startDateInput.value);
        const returnDate = new Date(returnDateInput.value);

        if (startDate && returnDate && !isNaN(startDate) && !isNaN(returnDate)) {
            if (returnDate < startDate) {
                tripDurationValue.textContent = "Return date must be after start date";
                tripDurationValue.style.color = "red";
                return false;
            }

            // Calculate the difference in days (inclusive of both start and end dates)
            const diffTime = Math.abs(returnDate - startDate);
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1; // +1 to make it inclusive

            tripDurationValue.textContent = diffDays + (diffDays === 1 ? " day" : " days");
            tripDurationValue.style.color = "black";
            return true;
        } else {
            tripDurationValue.textContent = "Please select both dates";
            tripDurationValue.style.color = "grey";
            return false;
        }
    }

    // Add event listeners to date inputs
    startDateInput.addEventListener('change', function () {
        calculateDuration();
        // Update min date for return input
        returnDateInput.min = startDateInput.value;
    });

    returnDateInput.addEventListener('change', calculateDuration);

    // Add event listener to the button
    getStartedBtn.addEventListener('click', function () {
        if (tripForm.checkValidity() && calculateDuration()) {
            alert("Trip details submitted!\n" +
                "Title: " + document.getElementById('tripTitle').value + "\n" +
                "Start Date: " + startDateInput.value + "\n" +
                "Return Date: " + returnDateInput.value + "\n" +
                "Duration: " + tripDurationValue.textContent);
            // Here you can add code to submit the form data
        } else {
            // Trigger browser's default validation
            tripForm.reportValidity();
        }
    });
});