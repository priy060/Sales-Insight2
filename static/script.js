document.addEventListener("DOMContentLoaded", function () {
  console.log("Script loaded and DOMContentLoaded event fired.");

  // Retrieve the username from local storage
  const username = localStorage.getItem("userName");
  console.log("Retrieved username from local storage:", username);

  // Display a welcome message using the retrieved username
  const welcomeMessage = document.getElementById("welcomeMessage");
  welcomeMessage.textContent = `Welcome to Dashboard, ${username || "Guest"}`;

  const toggleContainer = document.getElementById("toggleContainer");
  const toggleSwitch = document.getElementById("toggleSwitch");

  toggleContainer.addEventListener("click", () => {
    toggleContainer.classList.toggle("active");
    toggleSwitch.classList.toggle("active");
  });

  const profileInput = document.getElementById("profileInput");

  profileInput.addEventListener("change", function (event) {
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onload = function () {
      const profileImage = document.querySelector(".profile-image");
      profileImage.src = reader.result;

      // Save the profile picture in local storage
      localStorage.setItem("profileImage", reader.result);
    };

    if (file) {
      reader.readAsDataURL(file);
    }
  });

  document.addEventListener("DOMContentLoaded", function () {
    // Retrieve the profile image URL from local storage
    const profileImage = localStorage.getItem("profileImage");
    const profileImageElement = document.querySelector(".profile-image");
    console.log("yes")
    // Set the profile image URL
    profileImageElement.src = profileImage || "../static/default-profile.jpg";
  });
});
