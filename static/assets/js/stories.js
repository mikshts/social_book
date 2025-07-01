let currentIndex = 0;
let storyInterval;
const swipeThreshold = 50;

function openStory(index) {
  clearInterval(storyInterval);
  currentIndex = index;
  document.getElementById("fullStoryImage").src = storyImages[currentIndex];
  document.getElementById("storyViewer").classList.remove("hidden");
  resetProgress();
}

function closeStory() {
  clearInterval(storyInterval);
  document.getElementById("storyViewer").classList.add("hidden");
  document.getElementById("fullStoryImage").src = "";
}

function nextStory() {
  currentIndex = (currentIndex + 1) % storyImages.length;
  document.getElementById("fullStoryImage").src = storyImages[currentIndex];
  resetProgress();
}

function prevStory() {
  currentIndex = (currentIndex - 1 + storyImages.length) % storyImages.length;
  document.getElementById("fullStoryImage").src = storyImages[currentIndex];
  resetProgress();
}

function resetProgress() {
  clearInterval(storyInterval); // clear previous interval to avoid duplicates

  const progress = document.querySelector(".progress");
  progress.style.animation = "none";
  void progress.offsetWidth; // trigger reflow
  progress.style.animation = "progressAnim 5s linear forwards";

  progress.onanimationend = () => {
    nextStory();
  };

  // Restart interval to call nextStory after 5 seconds, just as a fallback
  storyInterval = setInterval(nextStory, 5000);
}

document.addEventListener("DOMContentLoaded", () => {
  let touchStartX = 0;
  let touchEndX = 0;

  const storyContainer = document.querySelector(".story-container");
  if (storyContainer) {
    storyContainer.addEventListener("touchstart", (e) => {
      touchStartX = e.changedTouches[0].screenX;
    });

    storyContainer.addEventListener("touchend", (e) => {
      touchEndX = e.changedTouches[0].screenX;
      handleSwipeGesture();
    });
  }

  function handleSwipeGesture() {
    const swipeDistance = touchEndX - touchStartX;

    if (Math.abs(swipeDistance) > swipeThreshold) {
      if (swipeDistance > 0) {
        prevStory();
      } else {
        nextStory();
      }
    }
  }

  const prevBtn = document.querySelector(".prev-story");
  const nextBtn = document.querySelector(".next-story");
  const closeBtn = document.querySelector(".close-story");

  if (prevBtn) prevBtn.addEventListener("click", prevStory);
  if (nextBtn) nextBtn.addEventListener("click", nextStory);
  if (closeBtn) closeBtn.addEventListener("click", closeStory);
});
