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


valid_collections = {
    "phoneTablets": "PHONE_TABLETS",
    "electronics": "ELECTRONICS",
    "appliances": "APPLIANCES",
    "health-beauty": "HEALTH_BEAUTY",
    "home-office": "HOME_OFFICE",
    "fashion": "FASHION",
    "computing": "COMPUTING",
    "supermarket": "SUPERMARKET",
    "babyproducts": "BABY_PRODUCTS",
    "sportinggoods": "sporting-goods",
    "automobile": "AUTOMOBILE",
    "gaming": "GAMING",
    "gardenoutdoor": "GARDEN_OUTDOOR",
    "books_movie_music": "BOOKS_MOVIE_MUSIC",
    "livestock": "LIVESTOCK",
    "industrialscientific": "INDUSTRIAL_SCIENTIFIC",
    "miscellaneous": "MISCELLANEOUS",
    "musicalintruments": "MUSICAL_INSTRUMENTS",
    "petsupplies": "PET_SUPPLIES",
    "services": "SERVICES",
    "toys_games": "TOYS_GAMES",
    "other": "OTHER"
}