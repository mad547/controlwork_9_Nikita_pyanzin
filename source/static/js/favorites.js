document.querySelectorAll('.fav-btn').forEach(function (button) {
    button.addEventListener('click', function () {
        button.disabled = true;

        const url = button.dataset.url;

        fetch(url, {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken}
        })
            .then(function (response) {
                return response.json();
            })
            .then(function (data) {
                if (data.is_favorite) {
                    button.classList.add('is-favorite');
                    button.textContent = 'В избранном ✓';
                } else {
                    button.classList.remove('is-favorite');
                    button.textContent = 'В избранное';
                }
                button.disabled = false;
            })
            .catch(function () {
                button.disabled = false;
            });
    });
});