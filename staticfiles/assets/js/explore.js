function showRanking(rankingType) {
  const container = event.target.closest(".profile-grid");
  const allSliders = container.querySelectorAll(".profile-slider");
  const allTabs = container.querySelectorAll(".tab");
  const allTables = container.querySelectorAll(".ranking-table");

  // Hide all elements
  allSliders.forEach((slider) => slider.classList.remove("active"));
  allTabs.forEach((tab) => tab.classList.remove("active"));
  allTables.forEach((table) => (table.style.display = "none"));

  // Show selected elements
  const activeSlider = container.querySelector(
    `[data-ranking="${rankingType}"]`
  );
  const activeTable = container.querySelector(`#${rankingType}`);
  if (activeSlider) activeSlider.classList.add("active");
  if (activeTable) activeTable.style.display = "table";
  event.target.classList.add("active");

  // Reset slider position
  if (activeSlider) {
    activeSlider.style.transform = "translateX(0)";
    initializeSlider(activeSlider.parentElement);
  }
}

function initializeSlider(container) {
  const slider = container.querySelector(".profile-slider.active");
  const prevBtn = container.querySelector(".prev-btn");
  const nextBtn = container.querySelector(".next-btn");
  if (!slider) return;

  const cardWidth = slider.querySelector(".profile-card").offsetWidth;
  let position = 0;

  function updateButtons() {
    prevBtn.disabled = position === 0;
    nextBtn.disabled = position <= -(slider.children.length - 1) * cardWidth;
  }

  nextBtn.onclick = () => {
    position -= cardWidth;
    slider.style.transform = `translateX(${position}px)`;
    updateButtons();
  };

  prevBtn.onclick = () => {
    position += cardWidth;
    slider.style.transform = `translateX(${position}px)`;
    updateButtons();
  };

  updateButtons();
}

// Initialize all sliders
document
  .querySelectorAll(".profile-slider-container")
  .forEach(initializeSlider);
