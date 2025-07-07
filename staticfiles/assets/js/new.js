window.addEventListener("DOMContentLoaded", () => {
  // Sidebar
  const menuItems = document.querySelectorAll(".menu-item");

  // Messages
  const messageNotification = document.querySelector("#messages-notifications");
  const messages = document.querySelector(".messages");
  const messageSearch = document.querySelector("#message-search");
  const message = messages ? messages.querySelectorAll(".message") : [];

  // Theme
  const theme = document.querySelector("#theme");
  const themeModal = document.querySelector(".customize-theme");
  const fontSize = document.querySelectorAll(".choose-size span");
  const root = document.querySelector(":root");
  const colorPalette = document.querySelectorAll(".choose-color span");
  const Bg1 = document.querySelector(".bg-1");
  const Bg2 = document.querySelector(".bg-2");
  const Bg3 = document.querySelector(".bg-3");

  // ============== SIDEBAR ==============
  const changeActiveItem = () => {
    menuItems.forEach((item) => {
      item.classList.remove("active");
    });
  };

  menuItems.forEach((item) => {
    item.addEventListener("click", () => {
      changeActiveItem();
      item.classList.add("active");
      const notificationPopup = document.querySelector(".notifications-popup");

      if (item.id !== "notifications") {
        notificationPopup.style.display = "none";
      } else {
        notificationPopup.style.display =
          notificationPopup.style.display === "block" ? "none" : "block";
        document.querySelector(
          "#notifications .notification-count"
        ).style.display = "none";
      }
    });
  });

  // ============== MESSAGES ==============
  const searchMessage = () => {
    const val = messageSearch.value.toLowerCase();
    message.forEach((user) => {
      let name = user.querySelector("h5").textContent.toLowerCase();
      user.style.display = name.includes(val) ? "flex" : "none";
    });
  };

  if (messageSearch) {
    messageSearch.addEventListener("keyup", searchMessage);
  }

  let messagesVisible = false;

  if (messageNotification) {
    messageNotification.addEventListener("click", () => {
      if (!messagesVisible) {
        messages.style.display = "block";
        messages.style.boxShadow = "0 0 1rem var(--color-primary)";
        messageNotification.querySelector(".notification-count").style.display =
          "none";
        setTimeout(() => {
          messages.style.boxShadow = "none";
        }, 2000);
        messagesVisible = true;
      } else {
        messages.style.display = "none";
        messagesVisible = false;
      }
    });
  }

  if (messages) {
    messages.style.display = "none";
  }

  // ============== THEME / DISPLAY CUSTOMIZATION ==============

  // Opens Modal
  const openThemeModal = () => {
    themeModal.style.display = "grid";
  };

  // Closes Modal
  const closeThemeModal = (e) => {
    if (e.target.classList.contains("customize-theme")) {
      themeModal.style.display = "none";
    }
  };

  themeModal.addEventListener("click", closeThemeModal);
  theme.addEventListener("click", openThemeModal);

  // ============== FONT SIZE ==============

  // remove active class from spans or font size selectors
  const removeSizeSelectors = () => {
    fontSize.forEach((size) => {
      size.classList.remove("active");
    });
  };

  fontSize.forEach((size) => {
    size.addEventListener("click", () => {
      removeSizeSelectors();
      let fontSize;
      size.classList.toggle("active");

      if (size.classList.contains("font-size-1")) {
        fontSize = "10px";
        root.style.setProperty("----sticky-top-left", "5.4rem");
        root.style.setProperty("----sticky-top-right", "5.4rem");
      } else if (size.classList.contains("font-size-2")) {
        fontSize = "13px";
        root.style.setProperty("----sticky-top-left", "5.4rem");
        root.style.setProperty("----sticky-top-right", "-7rem");
      } else if (size.classList.contains("font-size-3")) {
        fontSize = "16px";
        root.style.setProperty("----sticky-top-left", "-2rem");
        root.style.setProperty("----sticky-top-right", "-17rem");
      } else if (size.classList.contains("font-size-4")) {
        fontSize = "19px";
        root.style.setProperty("----sticky-top-left", "-5rem");
        root.style.setProperty("----sticky-top-right", "-25rem");
      } else if (size.classList.contains("font-size-5")) {
        fontSize = "22px";
        root.style.setProperty("----sticky-top-left", "-12rem");
        root.style.setProperty("----sticky-top-right", "-35rem");
      }

      // change font size of the root html element
      document.querySelector("html").style.fontSize = fontSize;
    });
  });

  // Remove active class from colors
  const changeActiveColorClass = () => {
    colorPalette.forEach((colorPicker) => {
      colorPicker.classList.remove("active");
    });
  };

  // Change color primary
  colorPalette.forEach((color) => {
    color.addEventListener("click", () => {
      let primary;
      changeActiveColorClass();

      if (color.classList.contains("color-1")) {
        primaryHue = 252;
      } else if (color.classList.contains("color-2")) {
        primaryHue = 52;
      } else if (color.classList.contains("color-3")) {
        primaryHue = 352;
      } else if (color.classList.contains("color-4")) {
        primaryHue = 152;
      } else if (color.classList.contains("color-5")) {
        primaryHue = 202;
      }

      color.classList.add("active");
      root.style.setProperty("--primary-color-hue", primaryHue);
    });
  });
  //Theme Background Values
  let lightColorLightness;
  let whiteColorLightness;
  let darkColorLightness;

  // Changes background color
  const changeBG = () => {
    root.style.setProperty("--light-color-lightness", lightColorLightness);
    root.style.setProperty("--white-color-lightness", whiteColorLightness);
    root.style.setProperty("--dark-color-lightness", darkColorLightness);
  };

  Bg1.addEventListener("click", () => {
    // add active class
    Bg1.classList.add("active");
    // remove active class from the others
    Bg2.classList.remove("active");
    Bg3.classList.remove("active");
    //remove customized changes from local storage
    window.location.reload();
  });

  Bg2.addEventListener("click", () => {
    darkColorLightness = "95%";
    whiteColorLightness = "20%";
    lightColorLightness = "15%";

    // add active class
    Bg2.classList.add("active");
    // remove active class from the others
    Bg1.classList.remove("active");
    Bg3.classList.remove("active");
    changeBG();
  });

  Bg3.addEventListener("click", () => {
    darkColorLightness = "95%";
    whiteColorLightness = "10%";
    lightColorLightness = "0%";

    // add active class
    Bg3.classList.add("active");
    // remove active class from the others
    Bg1.classList.remove("active");
    Bg2.classList.remove("active");
    changeBG();

    // Apply saved background on load
    //const savedDarkLightness = localStorage.getItem("darkColorLightness");
    //const savedWhiteLightness = localStorage.getItem("whiteColorLightness");
    // const savedLightLightness = localStorage.getItem("lightColorLightness");

    //if (savedDarkLightness && savedWhiteLightness && savedLightLightness) {
    //darkColorLightness = savedDarkLightness;
    //whiteColorLightness = savedWhiteLightness;
    //lightColorLightness = savedLightLightness;
    //changeBG();

    // Update active class for background
    //document
    //.querySelectorAll(".choose-bg .active")
    //.forEach((item) => item.classList.remove("active"));
    //if (
    //savedDarkLightness === "95%" &&
    //savedWhiteLightness === "20%" &&
    //savedLightLightness === "15%"
    //) {
    // Bg2.classList.add("active");
    //} else if (
    //savedDarkLightness === "95%" &&
    //savedWhiteLightness === "10%" &&
    //savedLightLightness === "0%"
    //) {
    //Bg3.classList.add("active");
    //} else {
    //  Bg1.classList.add("active"); // Default if none match
    //}
    //} else {
    //Bg1.classList.add("active"); // Set default background active
    //}
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const openModal = document.getElementById("dating-open-modal");
  const modalOverlay = document.getElementById("dating-post-modal");
  const closeModal = modalOverlay
    ? modalOverlay.querySelector(".dating-close-btn")
    : null;

  let subscriptionPopupActive = true; // Initially true to block modal

  if (openModal && modalOverlay && closeModal) {
    // Open Create Post Modal only if subscription popup is not active
    openModal.addEventListener("click", () => {
      if (!subscriptionPopupActive) {
        modalOverlay.style.display = "flex";
        document.body.style.overflow = "hidden"; // prevent scrolling
      }
    });

    // Close Modal
    closeModal.addEventListener("click", () => {
      modalOverlay.style.display = "none";
      document.body.style.overflow = "";
    });

    // Close modal when clicking outside the box
    modalOverlay.addEventListener("click", (e) => {
      if (e.target === modalOverlay) {
        modalOverlay.style.display = "none";
        document.body.style.overflow = "";
      }
    });
  }

  // Handle subscription popup logic
  const popup = document.getElementById("popup");
  const closePopup = document.getElementById("close-popup");
  const subscribeButton = document.getElementById("subscribe-button");

  if (popup && closePopup && subscribeButton) {
    // Show popup after delay
    window.addEventListener("load", () => {
      setTimeout(() => {
        popup.style.display = "flex";
      }, 5000);
    });

    // Close popup manually
    closePopup.addEventListener("click", () => {
      popup.style.display = "none";
      subscriptionPopupActive = false; // Allow modal after popup closes
    });

    // Subscription confirm
    subscribeButton.addEventListener("click", () => {
      const selectedPlan = document.querySelector(
        'input[name="subscription_plan"]:checked'
      );
      if (selectedPlan) {
        console.log("Subscribed to:", selectedPlan.value); // Optional log

        document.getElementById("subscription-options").style.display = "none";
        subscribeButton.style.display = "none";
        document.getElementById("subscription-confirmation").style.display =
          "block";

        // Hide popup after confirmation delay
        setTimeout(() => {
          popup.style.display = "none";
          subscriptionPopupActive = false; // Now allow modal
        }, 1500);
      }
    });
  } else {
    // If popup elements are missing, allow modal
    subscriptionPopupActive = false;
  }
});
//for posting in feed --------------------------------
const postsSocket = new WebSocket(
  (window.location.protocol === "https:" ? "wss://" : "ws://") +
  window.location.host +
  "/ws/posts_feed/"
);

postsSocket.onmessage = function (e) {
  const data = JSON.parse(e.data);

  const postList = document.getElementById("posts-list"); // The parent container
  const tempDiv = document.createElement("div");
  tempDiv.innerHTML = data.html;

  postList.prepend(tempDiv.firstElementChild); // Insert the post
};
//end of the post--------------------------
document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("create-post-form");

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const formData = new FormData(form);
    const postUrl = form.getAttribute("data-url"); // ← fixed URL from HTML

    fetch(postUrl, {
      method: "POST",
      body: formData,
      headers: {
        "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]")
          .value,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          //location.reload(); // Reload the page after successful post

          form.reset();
          document.getElementById("dating-post-modal").style.display = "none";
          document.body.style.overflow = "";

          // Create flash bubble
          const bubbleContainer = document.createElement("div");
          bubbleContainer.className = "flash-bubble-container";

          const bubble = document.createElement("div");
          bubble.className = "flash-bubble success";
          bubble.innerText = "Post created successfully!";

          bubbleContainer.appendChild(bubble);
          document.body.appendChild(bubbleContainer);

          // Remove after animation ends (4s from your CSS)
          setTimeout(() => {
            bubbleContainer.remove();
          }, 4000);
        }
      });
  });
});

//account_actions js ----------------------------
// Initialize elements
// Function to open a specific modal
function openMyCustomModal(modalId) {
  document.getElementById(modalId).style.display = "flex"; // Use flex to show and center
}

// Function to close a specific modal
function closeMyCustomModal(modalId) {
  document.getElementById(modalId).style.display = "none";
}

// Function to open the deactivation modal and pass the selected period
function openDeactivateAccountModal() {
  const selectedPeriod = document.getElementById("deactivation_period").value;
  document.getElementById("modalDeactivationPeriod").value = selectedPeriod; // Set hidden input value
  openMyCustomModal("deactivateAccountModal");
}

// Close modals when clicking outside of them
window.onclick = function (event) {
  if (event.target.classList.contains("my-custom-modal")) {
    event.target.style.display = "none";
  }
};
// --------------------------------------------
// JS REACT HEART SECTION (LIKE SYSTEM)
// --------------------------------------------
const likeSockets = {}; // ✅ Cache active WebSocket connections

function toggleLike(postId) {
  fetch(`/like/${postId}/`)
    .then((response) => response.json())
    .then((data) => {
      const heartBtn = document
        .getElementById(`like-btn-${postId}`)
        .querySelector("i");
      heartBtn.classList.toggle("liked", data.status === "liked");
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

document.addEventListener("DOMContentLoaded", function () {
  const protocol = window.location.protocol === "https:" ? "wss" : "ws"; // ✅ handle secure protocol

  document.querySelectorAll(".like-section").forEach((section) => {
    const postId = section.getAttribute("data-post-id");

    // ✅ Avoid duplicate socket connections
    if (likeSockets[postId]) return;

    const socket = new WebSocket(
      `${protocol}://${window.location.host}/ws/like/${postId}/`
    );
    likeSockets[postId] = socket;

    socket.onmessage = function (e) {
      const data = JSON.parse(e.data);
      const likeSectionToUpdate = document.getElementById(
        `liked-by-${data.post_id}`
      );

      if (likeSectionToUpdate) {
        let newContent = "";
        if (data.recent_likers && data.recent_likers.length > 0) {
          newContent += '<div class="like-section-content">';
          newContent += "<span>Liked by</span>";
          newContent += '<div class="like-section-users">';
          data.recent_likers.forEach((user) => {
            newContent += `<img src="${user.profile_img}" alt="${user.username}" />`;
          });
          newContent += "</div>";
          newContent += `<span>and</span><span id="like-count-${data.post_id}">${data.likes_count}</span><span>others</span>`;
          newContent += "</div>";
        } else {
          newContent += `<div class="like-section-content"><span id="like-count-${data.post_id}">${data.likes_count}</span> likes</div>`;
        }

        likeSectionToUpdate.innerHTML = newContent;

        const heartBtnIcon = document
          .getElementById(`like-btn-${data.post_id}`)
          .querySelector("i");
        if (heartBtnIcon && data.is_liked_by_current_user !== undefined) {
          heartBtnIcon.classList.toggle("liked", data.is_liked_by_current_user);
        }
      }
    };

    socket.onopen = () =>
      console.log(`✅ Like socket for post ${postId} opened`);
    socket.onclose = (e) =>
      console.warn(
        `❌ Like socket for post ${postId} closed. Code: ${e.code}, Reason: ${e.reason}`
      );
    socket.onerror = (e) =>
      console.error(`🔥 Like socket error (post ${postId}):`, e);
  });
});

// ✅ Optional cleanup: Close all sockets on page unload (browser safety)
// ✅ Unified cleanup for all WebSockets before page unload
window.addEventListener("beforeunload", () => {
  // Close post feed socket
  if (postFeedSocket && postFeedSocket.readyState === WebSocket.OPEN) {
    postFeedSocket.close();
  }

  // Close all like sockets
  Object.values(likeSockets).forEach((socket) => {
    if (socket.readyState === WebSocket.OPEN) {
      socket.close();
    }
  });
});

// --------------------------------------------
// POST FEED WebSocket - Handles new & deleted posts
// --------------------------------------------
let postFeedSocket = null;

document.addEventListener("DOMContentLoaded", function () {
  const protocol = window.location.protocol === "https:" ? "wss" : "ws";
  const socketUrl = `${protocol}://${window.location.host}/ws/posts_feed/`;

  if (!postFeedSocket || postFeedSocket.readyState !== WebSocket.OPEN) {
    postFeedSocket = new WebSocket(socketUrl);

    postFeedSocket.onopen = () => console.log("✅ Post feed socket connected.");

    postFeedSocket.onmessage = function (e) {
      const data = JSON.parse(e.data);
      console.log("WS message received:", data);

      if (data.action === "new_post") {
        const feed = document.getElementById("posts-list");
        if (feed) {
          const tempDiv = document.createElement("div");
          tempDiv.innerHTML = data.html;

          const newPostElement = tempDiv.firstElementChild;
          const postId = newPostElement?.id;
          
          if (!document.getElementById(postId)) {
            feed.insertAdjacentElement("afterbegin", newPostElement);

            const newPostId = postId?.replace("post-", "");
            if (newPostId) {
              initLikeSocketForNewPost(newPostId);
              initializePostButtons(newPostElement);
            }
          }
        }
      }

      if (data.action === "delete_post") {
        console.log("Deleting post with ID:", data.post_id);
        const postElement = document.getElementById(`post-${data.post_id}`);
        if (postElement) {
          postElement.remove();
        }
      }
    };

    postFeedSocket.onclose = (e) =>
      console.warn(`⚠️ Post feed socket closed. Code: ${e.code}, Reason: ${e.reason}`);

    postFeedSocket.onerror = (e) =>
      console.error("🔥 Post feed socket error:", e);
  }

  // Initialize existing posts
  initializeExistingPosts();
});

// Initialize buttons for existing posts on page load
function initializeExistingPosts() {
  document.querySelectorAll('[id^="post-"]').forEach(postElement => {
    initializePostButtons(postElement);
  });
}

function initializePostButtons(postElement) {
  const postId = postElement.id.replace("post-", "");

  // Comment button handler
  const commentBtn = postElement.querySelector(".comment-btn, .uil-comment-dots");
  if (commentBtn) {
    // Remove existing listeners to prevent duplicates
    commentBtn.removeEventListener("click", handleCommentClick);
    commentBtn.addEventListener("click", handleCommentClick);
    
    function handleCommentClick(e) {
      e.preventDefault();
      e.stopPropagation();
      openCommentPopup(postId);
    }
  }

  // Initialize modal for this post
  const modal = document.getElementById(`commentModal-${postId}`);
  if (modal) {
    // Close button
    const closeBtn = modal.querySelector(".modal-close-btn");
    if (closeBtn) {
      closeBtn.removeEventListener("click", handleCloseClick);
      closeBtn.addEventListener("click", handleCloseClick);
      
      function handleCloseClick(e) {
        e.preventDefault();
        closeCommentPopup(postId);
      }
    }

    // Click outside to close
    modal.removeEventListener("click", handleModalClick);
    modal.addEventListener("click", handleModalClick);
    
    function handleModalClick(e) {
      if (e.target === modal) {
        closeCommentPopup(postId);
      }
    }

    // Initialize comment form for this post
    initializeCommentForm(postId);
  }
}

// Like button delegation (keep existing)
document.getElementById("posts-list").addEventListener("click", function (e) {
  const likeBtn = e.target.closest(".like-btn");
  if (likeBtn) {
    const postId = likeBtn.getAttribute("data-post-id");
    if (postId) {
      toggleLike(postId);
    }
  }
});

// Comment form initialization
function initializeCommentForm(postId) {
  const form = document.querySelector(`#commentModal-${postId} .comment-form`);
  if (!form) return;

  // Initialize WebSocket for comments if not already done
  if (!commentSockets[postId]) {
    const wsProtocol = window.location.protocol === "https:" ? "wss" : "ws";
    commentSockets[postId] = new WebSocket(
      `${wsProtocol}://${window.location.host}/ws/comments/${postId}/`
    );

    commentSockets[postId].onopen = () => {
      console.log(`✅ Comment socket connected for post ${postId}`);
    };

    commentSockets[postId].onmessage = function (e) {
      const data = JSON.parse(e.data);
      console.log("Comment received:", data);
      
      const commentSection = document.querySelector(
        `#commentModal-${postId} .modal-all-comments`
      );
      
      if (commentSection) {
        const noCommentsMsg = commentSection.querySelector(".no-comments-msg");
        if (noCommentsMsg) noCommentsMsg.style.display = "none";

        const newComment = document.createElement("div");
        newComment.classList.add("modal-comment");
        newComment.innerHTML = `
          <div class="modal-comment-avatar">
            <img src="${data.profile_img || '/static/blank_profile_picture.png'}" />
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

    commentSockets[postId].onerror = (e) => {
      console.error(`Comment socket error for post ${postId}:`, e);
    };

    commentSockets[postId].onclose = (e) => {
      console.warn(`Comment socket closed for post ${postId}:`, e);
    };
  }

  // Form submission handler
  form.removeEventListener("submit", handleFormSubmit);
  form.addEventListener("submit", handleFormSubmit);

  async function handleFormSubmit(e) {
    e.preventDefault();

    const submitBtn = form.querySelector('button[type="submit"]');
    const textInput = form.querySelector('input[name="comment_text"]');
    const commentText = textInput.value.trim();
    const csrfToken = form.querySelector('input[name="csrfmiddlewaretoken"]').value;

    const btnText = submitBtn.querySelector(".btn-text");
    const btnSpinner = submitBtn.querySelector(".btn-spinner");

    if (!commentText) return;

    // Show loading state
    submitBtn.disabled = true;
    if (btnText) btnText.style.display = "none";
    if (btnSpinner) btnSpinner.style.display = "inline";

    try {
      const response = await fetch(form.action, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken,
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({ comment_text: commentText }),
      });

      if (response.ok) {
        const socket = commentSockets[postId];
        if (socket && socket.readyState === WebSocket.OPEN) {
          socket.send(JSON.stringify({ text: commentText }));
        } else {
          console.error("Comment socket not connected for post:", postId);
          // Fallback: reload the modal content
          location.reload();
        }
        textInput.value = "";
      } else {
        const errorData = await response.json();
        alert(errorData.message || "Failed to post comment");
      }
    } catch (error) {
      console.error("Comment submission error:", error);
      alert("Failed to connect to server.");
    } finally {
      // Restore button state
      submitBtn.disabled = false;
      if (btnText) btnText.style.display = "inline";
      if (btnSpinner) btnSpinner.style.display = "none";
    }
  }
}

// Modal functions
function openCommentPopup(postId) {
  const modal = document.getElementById(`commentModal-${postId}`);
  if (modal) {
    modal.style.display = "flex";
    document.body.style.overflow = "hidden";
    
    // Initialize slider for this modal
    initializeSlider(postId);
    
    console.log(`Opening modal for post ${postId}`);
  } else {
    console.error(`Modal not found for post ${postId}`);
  }
}

function closeCommentPopup(postId) {
  const modal = document.getElementById(`commentModal-${postId}`);
  if (modal) {
    modal.style.display = "none";
    document.body.style.overflow = "";
  }
}

// Slider initialization per modal
function initializeSlider(postId) {
  const modal = document.getElementById(`commentModal-${postId}`);
  if (!modal) return;

  const slider = modal.querySelector(".modal-image-slider");
  const slides = modal.querySelectorAll(".modal-image-slide");
  const prevBtn = modal.querySelector(".prev-slide");
  const nextBtn = modal.querySelector(".next-slide");
  const dotsContainer = modal.querySelector(".slide-dots");

  if (!slider || slides.length === 0) return;

  let currentSlide = 0;

  function showSlide(n) {
    currentSlide = Math.max(0, Math.min(n, slides.length - 1));
    slider.style.transform = `translateX(-${currentSlide * 100}%)`;
    
    if (prevBtn) prevBtn.disabled = currentSlide === 0;
    if (nextBtn) nextBtn.disabled = currentSlide === slides.length - 1;
    
    updateDots();
  }

  function updateDots() {
    const dots = modal.querySelectorAll(".slide-dot");
    dots.forEach((dot, index) => {
      dot.classList.toggle("active", index === currentSlide);
    });
  }

  function createDots() {
    if (!dotsContainer) return;
    dotsContainer.innerHTML = "";
    slides.forEach((_, index) => {
      const dot = document.createElement("div");
      dot.classList.add("slide-dot");
      dot.addEventListener("click", () => showSlide(index));
      dotsContainer.appendChild(dot);
    });
  }

  // Event listeners
  if (prevBtn) {
    prevBtn.removeEventListener("click", prevSlide);
    prevBtn.addEventListener("click", prevSlide);
  }
  
  if (nextBtn) {
    nextBtn.removeEventListener("click", nextSlide);
    nextBtn.addEventListener("click", nextSlide);
  }

  function prevSlide() {
    showSlide(currentSlide - 1);
  }

  function nextSlide() {
    showSlide(currentSlide + 1);
  }

  // Initialize
  createDots();
  showSlide(0);
}

// Comment sockets object
const commentSockets = {};

// Delete post function
function deletePost(postId) {
  if (!confirm("Are you sure you want to delete this post?")) return;

  fetch(`/post/${postId}/delete/`, {
    method: "POST",
    headers: { "X-CSRFToken": getCSRFToken() },
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.status === "success") {
        if (postFeedSocket && postFeedSocket.readyState === WebSocket.OPEN) {
          postFeedSocket.send(
            JSON.stringify({
              action: "delete_post",
              post_id: data.post_id,
              username: data.username,
            })
          );
        }
      } else {
        alert(data.message);
      }
    })
    .catch(() => alert("Error deleting post."));
}

// Time update function
function updateTimeSince() {
  document.querySelectorAll(".post-time").forEach((el) => {
    const createdAt = new Date(el.dataset.createdAt);
    const now = new Date();
    const seconds = Math.floor((now - createdAt) / 1000);

    let timeString = "";
    if (seconds < 60) {
      timeString = `${seconds}s ago`;
    } else if (seconds < 3600) {
      timeString = `${Math.floor(seconds / 60)}m ago`;
    } else if (seconds < 86400) {
      timeString = `${Math.floor(seconds / 3600)}h ago`;
    } else {
      timeString = `${Math.floor(seconds / 86400)}d ago`;
    }

    el.textContent = timeString;
  });
}

// Utility functions
function getCSRFToken() {
  const cookie = document.cookie
    .split(";")
    .find((c) => c.trim().startsWith("csrftoken="));
  return cookie ? cookie.split("=")[1] : "";
}

// Initialize time updates
setInterval(updateTimeSince, 60000);
updateTimeSince();

// Close sockets on page unload
window.addEventListener("beforeunload", () => {
  Object.values(commentSockets).forEach(socket => {
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.close();
    }
  });
  
  if (postFeedSocket && postFeedSocket.readyState === WebSocket.OPEN) {
    postFeedSocket.close();
  }
});