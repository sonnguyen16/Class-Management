let toggleBtn = document.getElementById("toggle-btn");
let body = document.body;
let darkMode = localStorage.getItem("dark-mode");

const enableDarkMode = () => {
  toggleBtn.classList.replace("fa-sun", "fa-moon");
  body.classList.add("dark");
  localStorage.setItem("dark-mode", "enabled");
};

const disableDarkMode = () => {
  toggleBtn.classList.replace("fa-moon", "fa-sun");
  body.classList.remove("dark");
  localStorage.setItem("dark-mode", "disabled");
};

if (darkMode === "enabled") {
  enableDarkMode();
}

toggleBtn.onclick = (e) => {
  darkMode = localStorage.getItem("dark-mode");
  if (darkMode === "disabled") {
    enableDarkMode();
  } else {
    disableDarkMode();
  }
};

let profile = document.querySelector(".header .flex .profile");

document.querySelector("#user-btn").onclick = () => {
  profile.classList.toggle("active");
  search.classList.remove("active");
};

let search = document.querySelector(".header .flex .search-form");

document.querySelector("#search-btn").onclick = () => {
  search.classList.toggle("active");
  profile.classList.remove("active");
};

let sideBar = document.querySelector(".side-bar");

document.querySelector("#menu-btn").onclick = () => {
  sideBar.classList.toggle("active");
  body.classList.toggle("active");
};

document.querySelector("#close-btn").onclick = () => {
  sideBar.classList.remove("active");
  body.classList.remove("active");
};

window.onscroll = () => {
  profile.classList.remove("active");
  search.classList.remove("active");

  if (window.innerWidth < 1200) {
    sideBar.classList.remove("active");
    body.classList.remove("active");
  }
};

$(document).ready(function () {
  $("#updateForm").validate({
    rules: {
      full_name: {
        required: true,
        minlength: 6,
      },
      email: {
        required: true,
        email: true,
      },
      date_of_birth: {
        required: true,
      },
    },
    messages: {
      email: {
        required: "Please enter your email",
        email: "Please enter a valid email",
      },
      full_name: {
        required: "Please enter your full name",
        minlength: "Please enter at least 6 characters",
      },
      date_of_birth: {
        required: "Please enter your date of birth",
      },
    },
    errorElement: "span",
    errorPlacement: function (error, element) {
      error.addClass("invalid-feedback");
      element.closest(".form-group").append(error);
    },
    highlight: function (element, errorClass, validClass) {
      $(element).addClass("is-invalid");
    },
    unhighlight: function (element, errorClass, validClass) {
      $(element).removeClass("is-invalid");
    },
    submitHandler: function (form) {
      $.ajax({
        url: "/update_profile",
        type: "POST",
        data: new FormData(form),
        processData: false,
        contentType: false,
        success: function (response) {
          if (response.status == "200") {
            $("#update-user-info-modal").modal("hide");
            toastr.success(response.message);
            setInterval(() => {
              location.reload();
            }, 1000);
          } else {
            toastr.error(response.message);
          }
        },
        error: function (error) {
          $("#submit").html("Login");
          toastr.error("Something went wrong");
        },
      });
    },
  });

  $("#createClass").validate({
    rules: {
      name: {
        required: true,
        minlength: 6,
      },
    },
    messages: {
      name: {
        required: "Please enter your class name",
        minlength: "Please enter at least 6 characters",
      },
    },
    errorElement: "span",
    errorPlacement: function (error, element) {
      error.addClass("invalid-feedback");
      element.closest(".form-group").append(error);
    },
    highlight: function (element, errorClass, validClass) {
      $(element).addClass("is-invalid");
    },
    unhighlight: function (element, errorClass, validClass) {
      $(element).removeClass("is-invalid");
    },
    submitHandler: function (form) {
      $.ajax({
        url: "/teacher/create_class",
        type: "POST",
        data: new FormData(form),
        processData: false,
        contentType: false,
        success: function (response) {
          if (response.status == "200") {
            $("#create-class").modal("hide");
            toastr.success(response.message);
            setInterval(() => {
              location.reload();
            }, 1000);
          } else {
            toastr.error(response.message);
          }
        },
        error: function (error) {
          $("#submit").html("Login");
          toastr.error("Something went wrong");
        },
      });
    },
  });

  $("#createHomework").validate({
    rules: {
      title: {
        required: true,
      },
      description: {
        required: true,
      },
    },
    messages: {
      title: {
        required: "Please enter your class name",
      },
      description: {
        required: "Please enter your class description",
      },
    },
    errorElement: "span",
    errorPlacement: function (error, element) {
      error.addClass("invalid-feedback");
      element.closest(".form-group").append(error);
    },
    highlight: function (element, errorClass, validClass) {
      $(element).addClass("is-invalid");
    },
    unhighlight: function (element, errorClass, validClass) {
      $(element).removeClass("is-invalid");
    },
    submitHandler: function (form) {
      $.ajax({
        url: "/teacher/create_homework",
        type: "POST",
        data: new FormData(form),
        processData: false,
        contentType: false,
        success: function (response) {
          if (response.status == "200") {
            $("#create-homework").modal("hide");
            toastr.success(response.message);
            setInterval(() => {
              location.reload();
            }, 1000);
          } else {
            toastr.error(response.message);
          }
        },
        error: function (error) {
          toastr.error("Something went wrong");
        },
      });
    },
  });
});
