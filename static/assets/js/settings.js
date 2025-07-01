// DOM Elements
const elements = {
  fileInput: document.getElementById("profile-picture"),
  preview: document.getElementById("preview"),
  editBtn: document.getElementById("edit-picture-btn"),
  modal: document.getElementById("editModal"),
  closeModal: document.getElementById("closeModal"),
  saveCrop: document.getElementById("saveCrop"),
  draggableImage: document.getElementById("draggableImage"),
};

// State Management
let state = {
  isDragging: false,
  startX: 0,
  startY: 0,
  translateX: 0,
  translateY: 0,
  scale: 1,
  naturalWidth: 0,
  naturalHeight: 0,
};

// Event Listeners
elements.fileInput.addEventListener("change", handleFileSelect);
elements.editBtn.addEventListener("click", showEditModal);
elements.closeModal.addEventListener("click", hideModal);
elements.saveCrop.addEventListener("click", saveCroppedImage);
elements.draggableImage.addEventListener("mousedown", startDragging);
document.addEventListener("mousemove", handleDragging);
document.addEventListener("mouseup", stopDragging);

// Event Handlers
function handleFileSelect(e) {
  const file = e.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = (event) => {
    elements.preview.style.backgroundImage = `url(${event.target.result})`;
    elements.editBtn.classList.add("show");
    initCropping(event.target.result);
  };
  reader.readAsDataURL(file);
}

function initCropping(imageSrc) {
  const img = new Image();
  img.src = imageSrc;

  img.onload = () => {
    state.naturalWidth = img.naturalWidth;
    state.naturalHeight = img.naturalHeight;
    state.scale = Math.max(300 / state.naturalWidth, 300 / state.naturalHeight);

    elements.draggableImage.src = imageSrc;
    elements.draggableImage.style.width = `${
      state.naturalWidth * state.scale
    }px`;
    elements.draggableImage.style.height = `${
      state.naturalHeight * state.scale
    }px`;
    resetImagePosition();
  };
}

function showEditModal() {
  if (!elements.preview.style.backgroundImage) {
    alert("Please select a profile picture first.");
    return;
  }
  elements.modal.style.display = "flex";
}

function hideModal() {
  elements.modal.style.display = "none";
  resetImagePosition();
}

function startDragging(e) {
  state.isDragging = true;
  state.startX = e.clientX - state.translateX;
  state.startY = e.clientY - state.translateY;
  elements.draggableImage.style.cursor = "grabbing";
}

function handleDragging(e) {
  if (!state.isDragging) return;

  const newX = e.clientX - state.startX;
  const newY = e.clientY - state.startY;

  const maxX = 0;
  const maxY = 0;
  const minX = -(state.naturalWidth * state.scale - 300);
  const minY = -(state.naturalHeight * state.scale - 300);

  state.translateX = Math.max(minX, Math.min(maxX, newX));
  state.translateY = Math.max(minY, Math.min(maxY, newY));

  elements.draggableImage.style.transform = `translate(${state.translateX}px, ${state.translateY}px)`;
}

function stopDragging() {
  state.isDragging = false;
  elements.draggableImage.style.cursor = "grab";
}

function saveCroppedImage() {
  const canvas = document.createElement("canvas");
  canvas.width = canvas.height = 300;
  const ctx = canvas.getContext("2d");

  // Create circular mask
  ctx.beginPath();
  ctx.arc(150, 150, 150, 0, Math.PI * 2);
  ctx.closePath();
  ctx.clip();

  // Calculate source dimensions
  const sourceX = Math.abs(state.translateX) / state.scale;
  const sourceY = Math.abs(state.translateY) / state.scale;
  const sourceSize = 300 / state.scale;

  // Draw cropped image
  ctx.drawImage(
    elements.draggableImage,
    sourceX,
    sourceY,
    sourceSize,
    sourceSize,
    0,
    0,
    300,
    300
  );

  // Update preview
  elements.preview.style.backgroundImage = `url(${canvas.toDataURL()})`;
  hideModal();
}

function resetImagePosition() {
  state.translateX = 0;
  state.translateY = 0;
  elements.draggableImage.style.transform = "translate(0px, 0px)";
}
elements.draggableImage.addEventListener("mouseenter", () => {
  elements.draggableImage.style.cursor = "grab";
});

//account_actions js ----------------------------
// Initialize elements
// Function to open a specific modal
// Function to open a specific modal
function toggleLike(postId) {
  fetch(`/like/${postId}/`, {
    method: "POST",
    headers: {
      "X-CSRFToken": getCSRFToken(), // Make sure you get the CSRF token
      "Content-Type": "application/json",
    },
    credentials: "include", // Important for session authentication
  })
    .then((response) => response.json())
    .then((data) => {
      const heartIcon = document.querySelector(`#like-btn-${postId} i`);
      const likeCount = document.getElementById(`like-count-${postId}`);
      const likeSection = document.getElementById(`liked-by-${postId}`);

      // Toggle the 'liked' class
      if (data.status === "liked") {
        heartIcon.classList.add("liked");
      } else {
        heartIcon.classList.remove("liked");
      }

      // Update like count
      if (likeCount) {
        likeCount.textContent = data.likes_count;
      }

      // Update the recent likers
      if (likeSection && data.recent_likers.length > 0) {
        let likerHTML = data.recent_likers
          .map(
            (user) => `<img src="${user.profile_img}" alt="${user.username}" />`
          )
          .join("");

        likeSection.innerHTML = `
          <div class="like-section-content">
            <span>Liked by</span>
            <div class="like-section-users">
              ${likerHTML}
            </div>
            <span>and</span>
            <span id="like-count-${postId}">${data.likes_count}</span>
            <span>others</span>
          </div>
        `;
      } else {
        // Fallback for no likes
        likeSection.innerHTML = `
          <div class="like-section-content">
            <span id="like-count-${postId}">0</span> likes
          </div>
        `;
      }
    })
    .catch((error) => console.error("Error liking post:", error));
}
function getCSRFToken() {
  const cookieValue = document.cookie
    .split("; ")
    .find((row) => row.startsWith("csrftoken="));
  return cookieValue ? cookieValue.split("=")[1] : "";
}

// Utility to open a modal
function openMyCustomModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.style.display = "flex";
  }
}

// Utility to close a modal
function closeMyCustomModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.style.display = "none";
  }
}

// Open Deactivate Modal and pass selected period
function openDeactivateAccountModal() {
  const selectedPeriod = document.getElementById("deactivation_period").value;
  const displayDays = document.getElementById("deactivationDaysDisplay");
  const modalInput = document.getElementById("modalDeactivationPeriod");

  // Display selected period in the confirmation modal
  displayDays.textContent = `${selectedPeriod} days`;
  modalInput.value = selectedPeriod;

  openMyCustomModal("deactivateAccountModal");
}

// Close modal when clicking outside modal content
window.addEventListener("click", function (event) {
  const deactivateModal = document.getElementById("deactivateAccountModal");
  const deleteModal = document.getElementById("deleteAccountModal");

  if (event.target === deactivateModal) {
    closeMyCustomModal("deactivateAccountModal");
  }
  if (event.target === deleteModal) {
    closeMyCustomModal("deleteAccountModal");
  }
});

document.addEventListener("DOMContentLoaded", function () {
  const imageContainer = document.querySelector(".image-upload-container");
  const fileInput = document.getElementById("id_profileimg");
  const currentImg = document.getElementById("current-profile-img");
  const noImagePlaceholder = document.getElementById("no-image-placeholder");

  if (imageContainer && fileInput) {
    imageContainer.addEventListener("click", function () {
      fileInput.click();
    });

    fileInput.addEventListener("change", function (e) {
      const file = e.target.files[0];
      if (file) {
        if (file.size > 5 * 1024 * 1024) {
          alert("File size must be less than 5MB");
          fileInput.value = "";
          return;
        }

        const reader = new FileReader();
        reader.onload = function (e) {
          if (currentImg) {
            currentImg.src = e.target.result;
          } else {
            // If no current image, create and append it
            const newImg = document.createElement("img");
            newImg.src = e.target.result;
            newImg.className = "preview-img";
            noImagePlaceholder.innerHTML = "";
            noImagePlaceholder.appendChild(newImg);
          }
        };
        reader.readAsDataURL(file);
      }
    });
  }

  // Bio character counter
  const bioTextarea = document.getElementById("id_bio");
  const charCounter = document.getElementById("bio-count");

  if (bioTextarea && charCounter) {
    const updateCharCount = () => {
      const count = bioTextarea.value.length;
      charCounter.textContent = count;
      charCounter.style.color =
        count > 900 ? "#dc2626" : count > 800 ? "#f59e0b" : "#6b7280";
    };
    updateCharCount();
    bioTextarea.addEventListener("input", updateCharCount);
  }

  // Form loading state
  const form = document.getElementById("profile-form");
  const saveBtn = document.getElementById("save-btn");
  const btnText = saveBtn?.querySelector(".btn-text");
  const loadingSpinner = saveBtn?.querySelector(".loading-spinner");

  if (form && saveBtn) {
    form.addEventListener("submit", function () {
      saveBtn.disabled = true;
      if (btnText) btnText.style.display = "none";
      if (loadingSpinner) loadingSpinner.style.display = "inline-block";
    });
  }
});

function resetForm() {
  if (confirm("Are you sure you want to reset all changes?")) {
    document.getElementById("profile-form").reset();

    // Reset bio character counter
    const charCounter = document.getElementById("bio-count");
    if (charCounter) {
      charCounter.textContent = "0";
      charCounter.style.color = "#6b7280";
    }

    // Reset profile image
    const currentImg = document.getElementById("current-profile-img");
    if (currentImg && currentImg.dataset.originalSrc) {
      currentImg.src = currentImg.dataset.originalSrc;
    }
  }
}
