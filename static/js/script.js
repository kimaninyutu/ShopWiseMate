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
