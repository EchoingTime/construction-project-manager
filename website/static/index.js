/*
@File Name: index.js
@Description: This file contains the JavaScript functionality for the front-end of the web application.
*/

/* --------------------- Navbar --------------------- */
function showNavSidebar() {
  const sidebar = document.querySelector(".nav-sidebar");
  sidebar.style.display = "flex";
}

function hideNavSidebar() {
  const sidebar = document.querySelector(".nav-sidebar");
  sidebar.style.display = "none";
}

/* --------------------- Sidebar --------------------- */

const toggleButton = document.getElementById("toggle-btn");
const sidebar = document.getElementById("default-asidebar");

function toggleSidebar() {
  sidebar.classList.toggle("close");
  toggleButton.classList.toggle("rotate");

  closeSubMenus();
}

function toggleSubMenu(button) {
  if (!button.nextElementSibling.classList.contains("show")) {
    closeSubMenus();
  }
  button.nextElementSibling.classList.toggle("show");
  button.classList.toggle("rotate");

  if (sidebar.classList.contains("close")) {
    sidebar.classList.toggle("close");
    toggleButton.classList.toggle("rotate");
  }
}

function closeSubMenus() {
  Array.from(sidebar.getElementsByClassName("show")).forEach((uL) => {
    uL.classList.remove("show");
    uL.previousElementSibling.classList.remove("rotate");
  });
}

/*--------------------- Message Flashing ---------------------*/

// Utilized ChatGPT to help with the modification concept
document.addEventListener("DOMContentLoaded", function () {
  const flashContainer = document.getElementById("toggle-flash-container");
  const alerts = flashContainer.querySelectorAll(".alert");

  // If alerts > 0 then display the section alert-container
  if (alerts.length > 0) {
    flashContainer.style.display = "flex";
  }

  // Close Alert
  var closeButtons = document.querySelectorAll(".alert .close");
  closeButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      var alert = this.parentElement;
      alert.style.display = "none";

      // Makes alert-container hidden again
      if (
        flashContainer.querySelectorAll("alert[style*='display: block']")
          .length === 0
      ) {
        flashContainer.style.display = "none";
      }
    });
  });
});

/*--------------------- Delete Projects ---------------------*/

function deleteProject(button) {
  const projectId = button.getAttribute("data-id");
  const projectName = button.getAttribute("data-name");
  const result = confirm(
    "Click 'OK' to delete the following project:\n\n" + projectName
  );
  if (result) {
    fetch("/delete-project", {
      method: "POST",
      body: JSON.stringify({ projectId: projectId }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }
}

/*--------------------- Login and Signup Pages ---------------------*/

const form = document.getElementById("form");
const firstname_input = document.getElementById("firstname-input");
const email_input = document.getElementById("email-input");
const password_input = document.getElementById("password-input");
const repeat_password_input = document.getElementById("repeat-password-input");
const error_message = document.getElementById("error-message");

form.addEventListener("submit", (e) => {
  let errors = [];

  if (firstname_input) {
    // If we have a firstname input then we are in the signup
    errors = getSignupFormErrors(
      firstname_input.value,
      email_input.value,
      password_input.value,
      repeat_password_input.value
    );
  } else {
    // If we don't have a firstname input then we are in the login
    errors = getLoginFormErrors(email_input.value, password_input.value);
  }

  if (errors.length > 0) {
    // If there are any errors
    e.preventDefault();
    error_message.innerText = errors.join(". ");
  }
});

function getSignupFormErrors(firstname, email, password, repeatPassword) {
  let errors = [];

  if (firstname === "" || firstname == null) {
    errors.push("Firstname is required");
    firstname_input.parentElement.classList.add("incorrect");
  }
  if (email === "" || email == null) {
    errors.push("Email is required");
    email_input.parentElement.classList.add("incorrect");
  }
  if (password === "" || password == null) {
    errors.push("Password is required");
    password_input.parentElement.classList.add("incorrect");
  }
  if (password.length < 7) {
    errors.push("Password must have at least 7 characters");
    password_input.parentElement.classList.add("incorrect");
  }
  if (password !== repeatPassword) {
    errors.push("Password does not match repeated password");
    password_input.parentElement.classList.add("incorrect");
    repeat_password_input.parentElement.classList.add("incorrect");
  }

  return errors;
}

function getLoginFormErrors(email, password) {
  let errors = [];

  if (email === "" || email == null) {
    errors.push("Email is required");
    email_input.parentElement.classList.add("incorrect");
  }
  if (password === "" || password == null) {
    errors.push("Password is required");
    password_input.parentElement.classList.add("incorrect");
  }

  return errors;
}

const allInputs = [
  firstname_input,
  email_input,
  password_input,
  repeat_password_input,
].filter((input) => input != null);

allInputs.forEach((input) => {
  input.addEventListener("input", () => {
    if (input.parentElement.classList.contains("incorrect")) {
      input.parentElement.classList.remove("incorrect");
      error_message.innerText = "";
    }
  });
});
