/*
@File Name: index.js
@Description: This file contains the JavaScript functionality for the front-end of the web application.
*/

/* --------------------- Sidebar --------------------- */

const toggleButton = document.getElementById('toggle-btn');
const sidebar = document.getElementById('sidebar');

function toggleSidebar() {
  sidebar.classList.toggle('close');
  toggleButton.classList.toggle('rotate');

  closeSubMenus();
}

function toggleSubMenu(button) {
  if (!button.nextElementSibling.classList.contains('show')) {
    closeSubMenus();
  }
  button.nextElementSibling.classList.toggle('show');
  button.classList.toggle('rotate');

  if (sidebar.classList.contains('close')) {
    sidebar.classList.toggle('close');
    toggleButton.classList.toggle('rotate');
  }
}

function closeSubMenus() {
  Array.from(sidebar.getElementsByClassName('show')).forEach((uL) => {
    uL.classList.remove('show');
    uL.previousElementSibling.classList.remove('rotate');
  });
}

/*--------------------- Message Flashing ---------------------*/

// Utilized ChatGPT to help with the modification concept
document.addEventListener('DOMContentLoaded', function () {
  const flashContainer = document.getElementById('toggle-flash-container');
  const alerts = flashContainer.querySelectorAll('.alert');

  // If alerts > 0 then display the section alert-container
  if (alerts.length > 0) {
    flashContainer.style.display = 'flex';
  }

  // Close Alert
  var closeButtons = document.querySelectorAll('.alert .close');
  closeButtons.forEach(function (button) {
    button.addEventListener('click', function () {
      var alert = this.parentElement;
      alert.style.display = 'none';

      // Makes alert-container hidden again
      if (
        flashContainer.querySelectorAll("alert[style*='display: block']")
          .length === 0
      ) {
        flashContainer.style.display = 'none';
      }
    });
  });
});

/*--------------------- Login and Signup Pages ---------------------*/

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('form-sign-in-and-out');
  if (!form) return; // Exit if form does not exist

  const firstname_input = document.getElementById('firstname-input');
  const email_input = document.getElementById('email-input');
  const password_input = document.getElementById('password-input');
  const repeat_password_input = document.getElementById(
    'repeat-password-input'
  );
  const error_message = document.getElementById('error-message');
  const role_select = document.getElementById('role-select');
  let trade_input = document.getElementById('trade-input');

  /*----------- Addition to Registry -----------*/

  // If, on signup, user select subcontractors, then pop up additional form input called Trade
  // ChatGPT Assistance for adding trade input
  document
    .getElementById('role-select')
    .addEventListener('change', function () {
      // Producing a div to fit new input into
      let trade_div = document.getElementById('trade-div');

      if (this.value === 'subcontractor' && !trade_div) {
        // Create div
        trade_div = document.createElement('div');
        trade_div.id = 'trade-div'; // So we know how to remove it

        // Creating label for svg
        let trade_label = document.createElement('label');
        trade_label.setAttribute('for', 'trade-input');

        // Create svg
        let trade_svg = document.createElementNS(
          'http://www.w3.org/2000/svg',
          'svg'
        );
        trade_svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
        trade_svg.setAttribute('height', '24px');
        trade_svg.setAttribute('viewBox', '0 -960 960 960');
        trade_svg.setAttribute('width', '24px');

        // Creating svg path
        let trade_path = document.createElementNS(
          'http://www.w3.org/2000/svg',
          'path'
        );
        trade_path.setAttribute(
          'd',
          'M160-120q-33 0-56.5-23.5T80-200v-440q0-33 23.5-56.5T160-720h160v-80q0-33 23.5-56.5T400-880h160q33 0 56.5 23.5T640-800v80h160q33 0 56.5 23.5T880-640v440q0 33-23.5 56.5T800-120H160Zm0-80h640v-440H160v440Zm240-520h160v-80H400v80ZM160-200v-440 440Z'
        );

        // Appending path to svg
        trade_svg.appendChild(trade_path);

        // Appending svg to label
        trade_label.appendChild(trade_svg);

        // Create input field
        let trade_input = document.createElement('input');
        trade_input.type = 'text';
        trade_input.name = 'trade';
        trade_input.id = 'trade-input';
        trade_input.placeholder = 'Enter your trade';

        // Appending the new label and input to the new div, then append div to the form!
        trade_div.appendChild(trade_label);
        trade_div.appendChild(trade_input);
        form.insertBefore(trade_div, form.lastElementChild);
      } else if (this.value !== 'subcontractor') {
        // Remove it
        if (trade_div) {
          trade_div.remove();
        }
      }
    });

  /*----------- Registry Errors -----------*/

  form.addEventListener('submit', (e) => {
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
      e.preventDefault(); // Prevent form submission if errors exist
      error_message.innerText = errors.join('. '); // Reveal error
    }
  });

  function getSignupFormErrors(firstname, email, password, repeatPassword) {
    let errors = [];

    if (firstname === '' || firstname == null) {
      console.log('Hello, World!');

      errors.push('Firstname is required');
      firstname_input.parentElement.classList.add('incorrect');
    }
    if (email === '' || email == null) {
      errors.push('Email is required');
      email_input.parentElement.classList.add('incorrect');
    }
    if (password === '' || password == null) {
      errors.push('Password is required');
      password_input.parentElement.classList.add('incorrect');
    }
    if (password.length < 7) {
      errors.push('Password must have at least 7 characters');
      password_input.parentElement.classList.add('incorrect');
    }
    if (password !== repeatPassword) {
      errors.push('Password does not match repeated password');
      password_input.parentElement.classList.add('incorrect');
      repeat_password_input.parentElement.classList.add('incorrect');
    }

    // Role selection addition
    if (!role_select.value) {
      errors.push('Must select a role!');
      role_select.parentElement.classList.add('incorrect');
    }

    // Trade input validation (if it exists)
    trade_input = document.getElementById('trade-input');

    if (trade_input && trade_input.value.trim() === '') {
      errors.push('Trade is required for subcontractors');
      trade_input.parentElement.classList.add('incorrect');
    }

    return errors;
  }

  /*----------- Login Errors -----------*/

  function getLoginFormErrors(email, password) {
    let errors = [];

    if (email === '' || email == null) {
      errors.push('Email is required');
      email_input.parentElement.classList.add('incorrect');
    }
    if (password === '' || password == null) {
      errors.push('Password is required');
      password_input.parentElement.classList.add('incorrect');
    }
    return errors;
  }

  // Clearing error messages on input change
  const allInputs = [
    firstname_input,
    email_input,
    password_input,
    repeat_password_input,
    role_select,
  ].filter((input) => input != null);

  allInputs.forEach((input) => {
    input.addEventListener('input', () => {
      if (input.parentElement.classList.contains('incorrect')) {
        input.parentElement.classList.remove('incorrect');
        error_message.innerText = '';
      }
    });
  });
});

/*--------------------- Toggle Projection Edit ---------------------*/

function toggleEdit() {
  const deleteSvg = document.querySelectorAll('#delete-svg');
  const borderToSmooth = document.querySelectorAll('.date, #project-link');
  const mediaQuery = window.matchMedia('(max-width: 800px)');
  const leftBorderRadius = document.querySelectorAll('#project-link');
  const editIcon = document.querySelector('#edit-project');

  if (editIcon.innerHTML.includes('M200-200h57l391')) {
    editIcon.innerHTML =
      '<path d="m622-453-56-56 82-82-57-57-82 82-56-56 195-195q12-12 26.5-17.5T705-840q16 0 31 6t26 18l55 56q12 11 17.5 26t5.5 30q0 16-5.5 30.5T817-647L622-453ZM200-200h57l195-195-28-29-29-28-195 195v57ZM792-56 509-338 290-120H120v-169l219-219L56-792l57-57 736 736-57 57Zm-32-648-56-56 56 56Zm-169 56 57 57-57-57ZM424-424l-29-28 57 57-28-29Z" />';
  } else {
    editIcon.innerHTML =
      '<path d="M200-200h57l391-391-57-57-391 391v57Zm-80 80v-170l528-527q12-11 26.5-17t30.5-6q16 0 31 6t26 18l55 56q12 11 17.5 26t5.5 30q0 16-5.5 30.5T817-647L290-120H120Zm640-584-56-56 56 56Zm-141 85-28-29 57 57-29-28Z" />';
  }

  // Only for Project Overview
  const projectOverview = document.getElementById('project-section');
  if (projectOverview) {
    deleteSvg.forEach((svg) => {
      svg.classList.toggle('hidden-svg');
    });
    borderToSmooth.forEach((el) => {
      el.classList.toggle('smooth-borders');
    });
    if (mediaQuery.matches) {
      leftBorderRadius.forEach((el) => {
        el.classList.toggle('left-radius');
      });
    }
  }
}

/*--------------------- Delete Projects ---------------------*/

function deleteProject(button) {
  const projectId = button.getAttribute('data-id');
  const projectName = button.getAttribute('data-name');
  const result = confirm(
    "Click 'OK' to delete the following project:\n\n" + projectName
  );
  if (result) {
    fetch('/delete-project', {
      method: 'POST',
      body: JSON.stringify({ projectId: projectId }),
    }).then((_res) => {
      window.location.href = '/';
    });
  }
}

/*--------------------- Project Details - File Select Work Around [Chat Assisted] ---------------------*/

document.addEventListener('DOMContentLoaded', function () {
  const sectionExists = document.getElementById('invoice-upload-sub-section');
  if (!sectionExists) return; // Exit if section does not exist

  const inputFile = document.getElementById('file');
  const inputInvoice = document.getElementById('invoice');
  const fileName = document.getElementById('file-name');
  const invoiceFileName = document.getElementById('invoice-file-name');

  inputFile.addEventListener('change', () => {
    fileName.textContent =
      inputFile.files.length > 0 ? inputFile.files[0].name : 'No File Selected';
  });
  inputInvoice.addEventListener('change', () => {
    invoiceFileName.textContent =
      inputInvoice.files.length > 0
        ? inputInvoice.files[0].name
        : 'No file chosen';
  });
});

/*--------------------- Project Details - Tab ---------------------*/

document.addEventListener('DOMContentLoaded', function () {
  const sectionExists = document.getElementById('project-details');
  if (!sectionExists) return; // Exit if section does not exist

  const buttons = document.querySelectorAll('.tab-btn');
  const contents = document.querySelectorAll('.tab-content');

  buttons.forEach((button) => {
    button.addEventListener('click', () => {
      // Remove active classes
      buttons.forEach((btn) => btn.classList.remove('active'));
      contents.forEach((content) => content.classList.remove('active'));

      // Add active class to clicked button and corresponding content
      button.classList.add('active');
      const targetTab = document.getElementById(button.dataset.tab);
      if (targetTab) {
        targetTab.classList.add('active');
      } else {
        console.error('No matching tab content found for:', button.dataset.tab);
      }
    });
  });
});

/*--------------------- Dynamic Calendar ---------------------*/

document.addEventListener('DOMContentLoaded', function () {
  const calendar = document.getElementById('calendar-section');
  if (!calendar) return; // Exit if calendar page does not exist

  // DOM Elements
  const calendarEl = document.querySelector('.calendar');
  const dateEl = document.querySelector('.date');
  const daysContainer = document.querySelector('.days');
  const prevBtn = document.querySelector('.prev');
  const nextBtn = document.querySelector('.next');
  const todayBtn = document.querySelector('.today-btn');
  const gotoBtn = document.querySelector('.goto-btn');
  const dateInput = document.querySelector('.date-input');

  // Date State
  let today = new Date();
  let currentMonth = today.getMonth();
  let currentYear = today.getFullYear();
  let activeDay = null;

  const months = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December',
  ];

  // Render Calendar
  function renderCalendar() {
    const firstDay = new Date(currentYear, currentMonth, 1);
    const lastDay = new Date(currentYear, currentMonth + 1, 0);
    const prevMonthLastDay = new Date(currentYear, currentMonth, 0);

    const prevDaysCount = firstDay.getDay();
    const nextDaysCount = 6 - lastDay.getDay();
    const lastDate = lastDay.getDate();
    const prevLastDate = prevMonthLastDay.getDate();

    // Set Header
    dateEl.textContent = `${months[currentMonth]} ${currentYear}`;

    // Generate Days
    let daysHTML = '';

    // Previous month days
    for (let i = prevDaysCount; i > 0; i--) {
      daysHTML += `<div class="day prev-date">${prevLastDate - i + 1}</div>`;
    }

    // Current month days
    for (let i = 1; i <= lastDate; i++) {
      const isToday =
        i === today.getDate() &&
        currentMonth === today.getMonth() &&
        currentYear === today.getFullYear();

      const activeClass = isToday ? 'today active' : '';
      if (isToday) activeDay = i;

      daysHTML += `<div class="day ${activeClass}" data-day="${i}">${i}</div>`;
    }

    // Next month days
    for (let i = 1; i <= nextDaysCount; i++) {
      daysHTML += `<div class="day next-date">${i}</div>`;
    }

    daysContainer.innerHTML = daysHTML;
    attachDayClickListeners();
  }

  // Navigate Months
  function changeMonth(direction) {
    currentMonth += direction;

    if (currentMonth < 0) {
      currentMonth = 11;
      currentYear--;
    } else if (currentMonth > 11) {
      currentMonth = 0;
      currentYear++;
    }

    renderCalendar();
  }

  // Handle Day Selection
  function attachDayClickListeners() {
    document.querySelectorAll('.day').forEach((dayEl) => {
      dayEl.addEventListener('click', () => {
        const dayNumber = Number(dayEl.textContent);
        const isPrev = dayEl.classList.contains('prev-date');
        const isNext = dayEl.classList.contains('next-date');

        if (isPrev) {
          changeMonth(-1);
          setTimeout(() => selectDay(dayNumber), 50);
        } else if (isNext) {
          changeMonth(1);
          setTimeout(() => selectDay(dayNumber), 50);
        } else {
          selectDay(dayNumber);
        }
      });
    });
  }

  function selectDay(dayNumber) {
    activeDay = dayNumber;

    document.querySelectorAll('.day').forEach((dayEl) => {
      dayEl.classList.remove('active');
      if (
        !dayEl.classList.contains('prev-date') &&
        !dayEl.classList.contains('next-date') &&
        Number(dayEl.textContent) === dayNumber
      ) {
        dayEl.classList.add('active');
      }
    });
  }

  // Reset to Today
  todayBtn.addEventListener('click', () => {
    today = new Date();
    currentMonth = today.getMonth();
    currentYear = today.getFullYear();
    renderCalendar();
  });

  // Format and Validate Input
  dateInput.addEventListener('input', (e) => {
    let value = e.target.value.replace(/[^0-9]/g, '');
    if (value.length > 2) value = value.slice(0, 2) + '/' + value.slice(2);
    e.target.value = value.slice(0, 7);
  });

  // Go To Entered Date
  gotoBtn.addEventListener('click', () => {
    const [mm, yyyy] = dateInput.value.split('/');

    if (
      mm &&
      yyyy &&
      !isNaN(mm) &&
      !isNaN(yyyy) &&
      mm >= 1 &&
      mm <= 12 &&
      yyyy.length === 4
    ) {
      currentMonth = parseInt(mm) - 1;
      currentYear = parseInt(yyyy);
      renderCalendar();
    } else {
      alert('Entered an invalid date!');
    }
  });

  // Init
  renderCalendar();

  // Hook up prev and next buttons
  prevBtn.addEventListener('click', () => changeMonth(-1));
  nextBtn.addEventListener('click', () => changeMonth(1));

  // Keyboard Navigation
  document.addEventListener('keydown', (e) => {
    switch (e.key) {
      case 'ArrowLeft':
        changeMonth(-1);
        break;
      case 'ArrowRight':
        changeMonth(1);
        break;
      case 't':
      case 'T':
        todayBtn.click();
        break;
      case 'g':
      case 'G':
        dateInput.focus();
        break;
    }
  });
});
