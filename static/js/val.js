document.addEventListener("DOMContentLoaded", function () {

  const correctColor = "#0d755f";
  const errorColor = "#7d091c";

  // ------------------ TARGET ALL FORMS ------------------
  const forms = document.querySelectorAll("form");

  forms.forEach(form => {

    const inputs = form.querySelectorAll("input, select");

    inputs.forEach(input => {

      // Skip submit & hidden
      if (input.type === "submit" || input.type === "hidden") return;

      // Remove native browser validation
      input.removeAttribute("required");

      // Validate while typing
      input.addEventListener("input", function () {
        validateField(input);
      });

      // Validate on blur
      input.addEventListener("blur", function () {
        validateField(input);
      });

    });

    // Form submit validation
    form.addEventListener("submit", function (e) {
      let isValid = true;

      inputs.forEach(input => {
        if (input.type === "submit" || input.type === "hidden") return;
        if (!validateField(input)) isValid = false;
      });

      if (!isValid) {
        e.preventDefault();
      }
    });

  });

  // ------------------ VALIDATION RULES ------------------
  function validateField(field) {
    const value = field.value.trim();
    const name = field.name.toLowerCase();

    // optional field
    if (name === "middle_name") {
      clearField(field);
      return true;
    }

    // EMPTY FIELD CHECK
    if (value === "") {
      showError(field, "(This field is required)");
      return false;
    }

    // PHONE VALIDATION
    if (name.includes("phone")) {
      const phoneRegex = /^\+256\d{9}$/;
      if (!phoneRegex.test(value)) {
        showError(field, "(Phone example +256 000 000000)");
        return false;
      }
    }

    // EMAIL VALIDATION
    if (field.type === "email") {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(value)) {
        showError(field, "(Enter valid email address e.g. example@email.com)");
        return false;
      }
    }

    showSuccess(field);
    return true;
  }

  // ------------------ HELPER FUNCTIONS ------------------
  function showError(field, message) {
    field.style.borderColor = errorColor;
    removeError(field);

    const error = document.createElement("p");
    error.className = "text-sm mt-1";
    error.style.color = errorColor;
    error.innerText = message;

    field.parentNode.appendChild(error);
  }

  function showSuccess(field) {
    field.style.borderColor = correctColor;
    removeError(field);
  }

  function clearField(field) {
    field.style.borderColor = "";
    removeError(field);
  }

  function removeError(field) {
    const existingError = field.parentNode.querySelector("p");
    if (existingError) existingError.remove();
  }

  // ------------------ APPLY TO MODAL FORMS ------------------
  // This ensures the Add Institution & Add Course modals use the same rules
  const modalForms = ["instModal", "courseModal"];
  modalForms.forEach(modalId => {
    const modal = document.getElementById(modalId);
    if (modal) {
      const form = modal.querySelector("form");
      if (form) form.dispatchEvent(new Event("submit", { cancelable: true }));
    }
  });

});