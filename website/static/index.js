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

/*--------------------- Toggle Projection Edit ---------------------*/

function toggleEdit() {
  const deleteSvg = document.querySelectorAll("#delete-svg");
  const borderToSmooth = document.querySelectorAll("#project-link");
  const editIcon = document.querySelector("#edit-project");

  if (editIcon.innerHTML.includes("M200-200h57l391")) {
    editIcon.innerHTML =
      '<path d="m622-453-56-56 82-82-57-57-82 82-56-56 195-195q12-12 26.5-17.5T705-840q16 0 31 6t26 18l55 56q12 11 17.5 26t5.5 30q0 16-5.5 30.5T817-647L622-453ZM200-200h57l195-195-28-29-29-28-195 195v57ZM792-56 509-338 290-120H120v-169l219-219L56-792l57-57 736 736-57 57Zm-32-648-56-56 56 56Zm-169 56 57 57-57-57ZM424-424l-29-28 57 57-28-29Z" />';
  } else {
    editIcon.innerHTML =
      '<path d="M200-200h57l391-391-57-57-391 391v57Zm-80 80v-170l528-527q12-11 26.5-17t30.5-6q16 0 31 6t26 18l55 56q12 11 17.5 26t5.5 30q0 16-5.5 30.5T817-647L290-120H120Zm640-584-56-56 56 56Zm-141 85-28-29 57 57-29-28Z" />';
  }

  deleteSvg.forEach((svg) => {
    svg.classList.toggle("hidden-svg");
  });
  borderToSmooth.forEach((a) => {
    a.classList.toggle("smooth-borders");
  });
}

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

const form = document.getElementById("form-sign-in-and-out");
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
