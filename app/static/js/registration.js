// registration.js

let otpSent = false;
let otpVerified = false; // Track whether OTP has been verified


function updatePrice() {
    const cameraPlan = document.getElementById('camera-plan');
    const selectedOption = cameraPlan.options[cameraPlan.selectedIndex].text; // Get selected option text
    const priceDisplay = document.getElementById('price');

    // Update price display
    priceDisplay.textContent = selectedOption.split(' - ')[1]; // Extract price from the option text
}

// Function to handle OTP sending
function sendOTP() {
    const email = document.getElementById('email').value;

    if (!email) {
        alert('Please enter your email address to receive the OTP.');
        return;
    }

    fetch('/auth/send_otp', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email: email })
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            if (data.message === `An OTP has been sent to ${email}. Please check your email.`) {
                otpSent = true;
                otpVerified = false; // Reset OTP verification status
                document.getElementById('otp-label').style.display = 'block';
                document.getElementById('otp').style.display = 'block';
                document.getElementById('verify-otp-btn').style.display = 'block';

                // Disable the OTP button and start the 60-second timer
                document.getElementById('send-otp-btn').disabled = true;

                setTimeout(() => {
                    if (!otpVerified) { // Re-enable button only if OTP is not verified
                        document.getElementById('send-otp-btn').disabled = false;
                    }
                }, 60000); // 60 seconds
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Function to handle OTP verification
function verifyOTP() {
    const otp = document.getElementById('otp').value;
    const email = document.getElementById('email').value;

    if (!otp) {
        alert('Please enter the OTP.');
        return;
    }

    fetch('/auth/verify_otp', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ otp: otp, email: email })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success === "OTP verified successfully!") {
                otpVerified = true;
                alert(data.success);
            } else {
                alert(data.failed);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}



document.getElementById('registration-form').addEventListener('submit', function (e) {
    // Clear any previous error messages
    document.querySelectorAll('.error-message').forEach(el => el.style.display = 'none');

    const name = document.getElementById('name').value.trim();
    const organization = document.getElementById('organization').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;

    let formIsValid = true;

    // Validate Name
    if (!name) {
        document.getElementById('name-error').textContent = 'Please enter your name.';
        document.getElementById('name-error').style.display = 'block';
        formIsValid = false;
    }

    // Validate Organization
    if (!organization) {
        document.getElementById('organization-error').textContent = 'Please enter your organization.';
        document.getElementById('organization-error').style.display = 'block';
        formIsValid = false;
    }

    // Validate Email
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // Basic email pattern
    if (!email) {
        document.getElementById('email-error').textContent = 'Please enter your email.';
        document.getElementById('email-error').style.display = 'block';
        formIsValid = false;
    } else if (!emailPattern.test(email)) {
        document.getElementById('email-error').textContent = 'Please enter a valid email address.';
        document.getElementById('email-error').style.display = 'block';
        formIsValid = false;
    }

    // Validate Password
    if (!password) {
        document.getElementById('password-error').textContent = 'Please enter your password.';
        document.getElementById('password-error').style.display = 'block';
        formIsValid = false;
    } else if (password.length < 8) {
        document.getElementById('password-error').textContent = 'Password must be at least 8 characters long.';
        document.getElementById('password-error').style.display = 'block';
        formIsValid = false;
    }

    // Validate Confirm Password
    if (password !== confirmPassword) {
        document.getElementById('confirm-password-error').textContent = 'Passwords do not match.';
        document.getElementById('confirm-password-error').style.display = 'block';
        formIsValid = false;
    }

    // Validate OTP
    if (!otpVerified) {
        alert('Please verify your email by entering the OTP sent to your email.');
        formIsValid = false;
    }

    // If any validation fails, prevent form submission
    if (!formIsValid) {
        e.preventDefault();
    }
});
