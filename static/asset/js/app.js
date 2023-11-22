import { io } from "https://cdn.socket.io/4.4.1/socket.io.esm.min.js";

const socket = io("http://localhost:3000", {
  withCredentials: false,
});

const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute("content");

let name = $("#user_fullname").val();
let role = $("#user_role").val();
let id = $("#user_id").val();

socket.on("create-homework", (data) => {
  if (role == 0) return;

  $.ajax({
    url: "/noti/create_homework",
    type: "POST",
    headers: {
      "X-CSRFToken": csrfToken,
    },
    data: {
      class_id: data.class_id,
      name: data.name,
    },
    success: function (response) {
      if (response.status == "200") {
        console.log(response);
        toastr.success(response.data.content);
        let html = `<a href="${response.data.link}" class="d-flex justify-content-between">
        <p class="fs-3 text-danger"><i class="fas fa-bell"></i> ${response.data.content}</p>
        <p class="fs-3 text-secondary">Now</p>
        </a>`;
        // Lấy nội dung của phần tử #noti
        var currentContent = $("#noti").html();
        var expectedHtml = '<p class="fs-2 text-center">No notification</p>';
        if (currentContent.trim() === expectedHtml.trim()) {
          $("#noti").html(html);
        } else {
          $("#noti").prepend(html);
        }
      } else {
        console.log(response);
      }
    },
    error: function (error) {
      console.log(error);
    },
  });
});

socket.on("submit-homework", (data) => {
  if (role == 1) return;

  $.ajax({
    url: "/noti/submit_homework",
    type: "POST",
    headers: {
      "X-CSRFToken": csrfToken,
    },
    data: {
      homework_id: data.homework_id,
      name: data.name,
    },
    success: function (response) {
      if (response.status == "200") {
        console.log(response);
        toastr.success(response.data.content);
        let html = `<a href="${response.data.link}" class="d-flex justify-content-between">
            <p class="fs-3 text-danger"><i class="fas fa-bell"></i> ${response.data.content}</p>
            <p class="fs-3 text-secondary">Now</p>
            </a>`;
        // Lấy nội dung của phần tử #noti
        var currentContent = $("#noti").html();
        var expectedHtml = '<p class="fs-2 text-center">No notification</p>';
        if (currentContent.trim() === expectedHtml.trim()) {
          $("#noti").html(html);
        } else {
          $("#noti").prepend(html);
        }
      } else {
        console.log(response);
      }
    },
    error: function (error) {
      console.log(error);
    },
  });
});

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
      deadline: {
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
      deadline: {
        required: "Please enter your deadline",
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
            let class_id = $("#class_id").val();
            let user_id = $("#user_id").val();
            socket.emit("create-homework", {
              name: name,
              class_id: class_id,
              user_id: user_id,
            });
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

  $("#joinClass").validate({
    rules: {
      invite_code: {
        required: true,
      },
    },
    messages: {
      invite_code: {
        required: "Please enter your invite code",
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
        url: "/student/join_class",
        type: "POST",
        data: new FormData(form),
        processData: false,
        contentType: false,
        success: function (response) {
          if (response.status == "200") {
            $("#join-class").modal("hide");
            toastr.success(response.message);
            setInterval(() => {
              window.location.href = "/class";
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

  $("#submitHomework").validate({
    rules: {
      file: {
        required: true,
      },
    },
    messages: {
      file: {
        required: "Please select your file",
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
        url: "/student/submit_homework",
        type: "POST",
        data: new FormData(form),
        processData: false,
        contentType: false,
        success: function (response) {
          if (response.status == "200") {
            $("#submit-homework").modal("hide");
            toastr.success(response.message);
            setInterval(() => {
              location.reload();
            }, 1000);
            let homework_id = $("#homework_id").val();
            let user_id = $("#user_id").val();
            socket.emit("submit-homework", {
              name: name,
              homework_id: homework_id,
              user_id: user_id,
            });
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

  $("#scoreHomework").validate({
    rules: {
      score: {
        required: true,
        min: 0,
        max: 10,
      },
      comment: {
        required: true,
        minlength: 10,
      },
    },
    messages: {
      score: {
        required: "Please enter your score",
        min: "Please enter at least 0",
        max: "Please enter at most 10",
      },
      comment: {
        required: "Please enter your comment",
        minlength: "Please enter at least 10 characters",
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
        url: "/teacher/score_homework",
        type: "POST",
        data: new FormData(form),
        processData: false,
        contentType: false,
        success: function (response) {
          if (response.status == "200") {
            $("#score-homework").modal("hide");
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

  $("#updateHomework").validate({
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
        url: "/teacher/update_homework",
        type: "POST",
        data: new FormData(form),
        processData: false,
        contentType: false,
        success: function (response) {
          if (response.status == "200") {
            $("#update-homework").modal("hide");
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
