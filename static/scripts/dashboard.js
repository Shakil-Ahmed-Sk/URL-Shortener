document.addEventListener('DOMContentLoaded', function() {
    const sortSelect = document.getElementById('sort');
    const applySortButton = document.getElementById('apply-sort');

    // Immediately sort the table by timestamp when the page loads
    sortUrls('new');

    applySortButton.addEventListener('click', function() {
        const criteria = sortSelect.value;
        console.log('Applying sort with criteria:', criteria);
        sortUrls(criteria);
    });

    function sortUrls(criteria) {
        const rows = Array.from(document.querySelectorAll('tbody tr'));
        console.log('Initial rows:', rows);

        let sortedRows;
        if (criteria === 'click_count') {
            sortedRows = rows.sort((rowA, rowB) => {
                const clickCountA = parseInt(rowA.querySelector('.click-count').textContent);
                const clickCountB = parseInt(rowB.querySelector('.click-count').textContent);
                return clickCountB - clickCountA;
            });
        } else if (criteria === 'unclicked') {
            sortedRows = rows.filter(row => {
                const clickCount = parseInt(row.querySelector('.click-count').textContent);
                return clickCount === 0;
            });
        } else if (criteria === 'new') {
            sortedRows = rows.sort((rowA, rowB) => {
                const timestampA = new Date(rowA.querySelector('.timestamp').textContent);
                const timestampB = new Date(rowB.querySelector('.timestamp').textContent);
                return timestampB - timestampA;
            });
        }

        console.log('Sorted rows:', sortedRows);

        const tbody = document.querySelector('tbody');
        tbody.innerHTML = '';

        if (criteria === 'unclicked') {
            sortedRows.forEach(row => {
                tbody.appendChild(row);
            });
            const remainingRows = rows.filter(row => {
                const clickCount = parseInt(row.querySelector('.click-count').textContent);
                return clickCount !== 0;
            });
            remainingRows.forEach(row => {
                tbody.appendChild(row);
            });
        } else {
            sortedRows.forEach(row => {
                tbody.appendChild(row);
            });
        }

        console.log('Table sorted by', criteria);
    }
});
