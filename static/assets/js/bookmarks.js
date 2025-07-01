// Set bookmarkData as empty for 'all' to test the empty message
const bookmarkData = {
  all: [], // Empty to simulate no bookmarks in the "All" category
  online: [],
  recent: [],
};

const container = document.getElementById("bookmarkContainer");
const noBookmarksText = document.getElementById("noBookmarks");
const buttons = document.querySelectorAll(".filter-btn");

function filterCards(filter) {
  const cards = document.querySelectorAll(".bookmark-card");

  cards.forEach((card) => {
    if (filter === "all" || card.classList.contains(filter)) {
      card.style.display = "block";
    } else {
      card.style.display = "none";
    }
  });

  // Toggle active button styling
  const buttons = document.querySelectorAll(".filter-btn");
  buttons.forEach((button) => button.classList.remove("active"));
  document
    .querySelector(`.filter-btn[onclick="filterCards('${filter}')"]`)
    .classList.add("active");

  // Show or hide "noBookmarks"
  const visible = [...cards].some((card) => card.style.display !== "none");
  document.getElementById("noBookmarks").style.display = visible ? "none" : "block";
}


// Initial load - filtering to 'all' for this example
filterCards("all");

