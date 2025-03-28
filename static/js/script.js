// Form validation
document.addEventListener("DOMContentLoaded", function () {
  const forms = document.querySelectorAll("form");

  forms.forEach((form) => {
    form.addEventListener("submit", function (event) {
      const passwordField = form.querySelector('input[name="password"]');
      const confirmPasswordField = form.querySelector(
        'input[name="confirm_password"]'
      );

      // Password confirmation validation
      if (passwordField && confirmPasswordField) {
        if (passwordField.value !== confirmPasswordField.value) {
          event.preventDefault();
          alert("Passwords do not match!");
        }
      }
    });
  });

  // Auto-hide alerts after 5 seconds
  const alerts = document.querySelectorAll(".alert");
  alerts.forEach((alert) => {
    setTimeout(() => {
      if (alert) {
        const closeButton = alert.querySelector(".close");
        if (closeButton) closeButton.click();
      }
    }, 5000);
  });

  // Password strength meter
  const passwordInput = document.querySelector('input[name="password"]');
  if (passwordInput) {
    const strengthMeter = document.querySelector(".strength-meter-bar");
    const strengthText = document.querySelector(".strength-text");

    passwordInput.addEventListener("input", function () {
      const val = passwordInput.value;
      let strength = 0;
      let message = "";

      if (val.length >= 8) strength += 25;
      if (val.match(/[a-z]/) && val.match(/[A-Z]/)) strength += 25;
      if (val.match(/\d/)) strength += 25;
      if (val.match(/[^a-zA-Z\d]/)) strength += 25;

      if (strength <= 25) {
        message = "Too weak";
        strengthMeter.style.backgroundColor = "#dc3545";
      } else if (strength <= 50) {
        message = "Could be stronger";
        strengthMeter.style.backgroundColor = "#ffc107";
      } else if (strength <= 75) {
        message = "Strong password";
        strengthMeter.style.backgroundColor = "#17a2b8";
      } else {
        message = "Very strong password";
        strengthMeter.style.backgroundColor = "#28a745";
      }

      strengthMeter.style.width = strength + "%";
      strengthText.textContent = "Password strength: " + message;
    });
  }

  // Toggle switch label between Enable/Disable
  const initSwitchLabel = function (switchId) {
    const switchElement = document.getElementById(switchId);
    if (switchElement) {
      const switchLabel = document.querySelector(`label[for="${switchId}"]`);

      // Set initial label text
      if (switchLabel) {
        switchLabel.textContent = switchElement.checked ? "Enable" : "Disable";

        // Add change event listener
        switchElement.addEventListener("change", function () {
          switchLabel.textContent = this.checked ? "Enable" : "Disable";
        });
      }
    }
  };

  // Initialize all switches on the page
  initSwitchLabel("twoFactorSwitch");
  initSwitchLabel("emailNotifSwitch");
});

// Toggle password visibility
function togglePassword(inputId) {
  const passwordInput = document.getElementById(inputId);
  const toggleIcon = passwordInput.nextElementSibling.querySelector("i");

  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    toggleIcon.classList.remove("fa-eye");
    toggleIcon.classList.add("fa-eye-slash");
  } else {
    passwordInput.type = "password";
    toggleIcon.classList.remove("fa-eye-slash");
    toggleIcon.classList.add("fa-eye");
  }
}
