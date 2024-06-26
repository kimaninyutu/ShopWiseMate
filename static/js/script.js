document.addEventListener('DOMContentLoaded', function () {
    var loadMoreButton = document.querySelector('.seymour-container .button-collection');
    var hiddenItems = document.querySelectorAll('.collections-grid .collections--ul li:nth-child(n+7)');

    // Hide all items beyond the first 6
    hiddenItems.forEach(function (item) {
        item.style.display = 'none';
    });

    loadMoreButton.addEventListener('click', function () {
        hiddenItems.forEach(function (item) {
            item.style.display = 'flex'; // Display the hidden items
        });
        loadMoreButton.style.display = 'none'; // Hide the "Load More" button
    });
});

// Get references to the search button and overlay
const searchBtn = document.getElementById("search-btn");
const overlay = document.getElementById("overlay");

// Add event listener to the search button
searchBtn.addEventListener("click", function() {
    // Toggle the visibility of the overlay
    overlay.classList.toggle("show");

    // If the overlay is now visible, focus on the search input
    if (overlay.classList.contains("show")) {
        document.querySelector(".search-input").focus();
    }
});

// Add event listener to the search input to shrink the overlay when focus is lost
document.querySelector(".search-input").addEventListener("blur", function() {
    // Hide the overlay
    overlay.classList.remove("show");
});


document.addEventListener('DOMContentLoaded', function() {
    var viewProductForm = document.getElementById('viewProductForm');

    if (viewProductForm) {
        viewProductForm.addEventListener('submit', function(event) {
            event.preventDefault(); // Prevent the form from submitting in the traditional way
            var productLink = this.querySelector('input[name="product_link"]').value;
            window.open(productLink, '_blank'); // Open the link in a new tab
        });
    }
});
