// DOM ELEMENTS
const modalImageSlider = document.querySelector(".modal-image-slider");
const modalImageSlides = document.querySelectorAll(".modal-image-slide");
const prevSlideBtn = document.querySelector(".prev-slide");
const nextSlideBtn = document.querySelector(".next-slide");
const modalImage = document.querySelector(".modal-large-photo");
const slideDotsContainer = document.querySelector(".slide-dots");

// MODAL FUNCTIONS
function openCommentPopup(postId) {
  const modal = document.getElementById("commentModal-" + postId);
  if (modal) {
    modal.style.display = "flex";
    document.body.style.overflow = "hidden";
  }
}

function closeCommentPopup(postId) {
  const modal = document.getElementById("commentModal-" + postId);
  if (modal) {
    modal.style.display = "none";
    document.body.style.overflow = "";
  }
}

// Close modal when clicking background
document.querySelectorAll("[id^='commentModal-']").forEach((modal) => {
  modal.addEventListener("click", function (e) {
    if (e.target === modal) {
      closeCommentPopup(modal.id.replace("commentModal-", ""));
    }
  });
});

// SLIDER LOGIC
let slideIndex = 0;

function showSlide(n) {
  if (!modalImageSlider || modalImageSlides.length === 0) return;
  slideIndex = n;
  if (slideIndex < 0) slideIndex = 0;
  if (slideIndex >= modalImageSlides.length)
    slideIndex = modalImageSlides.length - 1;

  modalImageSlider.style.transform = `translateX(-${slideIndex * 100}%)`;

  if (prevSlideBtn) prevSlideBtn.disabled = slideIndex === 0;
  if (nextSlideBtn)
    nextSlideBtn.disabled = slideIndex === modalImageSlides.length - 1;

  updateDots();
}

function nextSlide() {
  if (slideIndex < modalImageSlides.length - 1) {
    slideIndex++;
    showSlide(slideIndex);
  }
}

function prevSlide() {
  if (slideIndex > 0) {
    slideIndex--;
    showSlide(slideIndex);
  }
}

function createDots() {
  if (!slideDotsContainer || modalImageSlides.length === 0) return;
  slideDotsContainer.innerHTML = "";
  modalImageSlides.forEach((_, index) => {
    const dot = document.createElement("div");
    dot.classList.add("slide-dot");
    dot.addEventListener("click", () => showSlide(index));
    slideDotsContainer.appendChild(dot);
  });
  updateDots();
}

function updateDots() {
  const dots = document.querySelectorAll(".slide-dot");
  dots.forEach((dot, index) => {
    dot.classList.toggle("active", index === slideIndex);
  });
}

if (prevSlideBtn) prevSlideBtn.addEventListener("click", prevSlide);
if (nextSlideBtn) nextSlideBtn.addEventListener("click", nextSlide);

if (modalImageSlides.length > 0) {
  showSlide(slideIndex);
  if (prevSlideBtn) prevSlideBtn.disabled = true;
  createDots();
}

// AJAX COMMENT SUBMISSION
const commentSockets = {};

document.addEventListener("DOMContentLoaded", function () {
  const wsProtocol = window.location.protocol === "https:" ? "wss" : "ws";
  document.querySelectorAll(".comment-form").forEach((form) => {
    const postId = form.dataset.postId;

    // Avoid duplicate WebSocket
    if (!commentSockets[postId]) {
      commentSockets[postId] = new WebSocket(
        `${wsProtocol}://${window.location.host}/ws/comments/${postId}/`
      );

      commentSockets[postId].onmessage = function (e) {
        const data = JSON.parse(e.data);
        const commentSection = document.querySelector(
          `#commentModal-${postId} .modal-all-comments`
        );
        if (commentSection) {
          const noCommentsMsg =
            commentSection.querySelector(".no-comments-msg");
          if (noCommentsMsg) noCommentsMsg.style.display = "none";

          const newComment = document.createElement("div");
          newComment.classList.add("modal-comment");
          newComment.innerHTML = `
            <div class="modal-comment-avatar">
              <img src="${data.profile_img}" />
            </div>
            <div class="modal-comment-body">
              <p class="modal-comment-author">${data.username}</p>
              <p class="modal-comment-text">${data.text}</p>
            </div>
          `;
          commentSection.appendChild(newComment);
          commentSection.scrollTop = commentSection.scrollHeight;
        }
      };
    }

    const socket = commentSockets[postId];

    form.addEventListener("submit", async function (e) {
      e.preventDefault();

      const submitBtn = this.querySelector('button[type="submit"]');
      const textInput = this.querySelector('input[name="comment_text"]');
      const commentText = textInput.value.trim();
      const csrfToken = this.querySelector(
        'input[name="csrfmiddlewaretoken"]'
      ).value;

      const btnText = submitBtn.querySelector(".btn-text");
      const btnSpinner = submitBtn.querySelector(".btn-spinner");

      if (!commentText) return;

      // Show spinner
      submitBtn.disabled = true;
      btnText.style.display = "none";
      btnSpinner.style.display = "inline";

      try {
        const response = await fetch(this.action, {
          method: "POST",
          headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/x-www-form-urlencoded",
          },
          body: new URLSearchParams({ comment_text: commentText }),
        });

        if (response.ok) {
          if (socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({ text: commentText }));
          } else {
            alert("Comment socket not connected.");
          }
          textInput.value = "";
        } else {
          alert("Something went wrong when posting your comment.");
        }
      } catch (error) {
        alert("Failed to connect to server.");
        console.error(error);
      }

      // Restore button
      submitBtn.disabled = false;
      btnText.style.display = "inline";
      btnSpinner.style.display = "none";
    });
  });
});
