// Добавление нового комментария
document.getElementById('add-comment-btn').addEventListener('click', function() {
    const text = document.getElementById('new-comment-text').value;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(window.location.href, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({ action: 'add', text: text })
    })
    .then(response => response.json())
    .then(data => {
if (data.success) {
            const createdAt = new Date(data.created_at);
            const formattedDate = createdAt.toLocaleString('ru-RU', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });

            const commentHtml = `
                <li class="list-group-item" id="comment-${data.comment_id}">
                    <strong>${data.username}:</strong><br> <span class="comment-text">${data.text}</span>
                    <br>
                    <small class="text-muted">${formattedDate}</small>
                    <div class="mt-2">
                        <button class="btn btn-sm btn-warning edit-comment-btn" data-id="${data.comment_id}">Редактировать</button>
                        <button class="btn btn-sm btn-danger delete-comment-btn" data-id="${data.comment_id}">Удалить</button>
                    </div>
                </li>
            `;

            // Добавляем комментарий в список
            const commentList = document.getElementById('comment-list');
            commentList.insertAdjacentHTML('beforeend', commentHtml);

            // Очищаем поле ввода
            document.getElementById('new-comment-text').value = '';
        } else {
            console.error('Ошибка добавления комментария:', data.error);
        }
    });
});

// Редактирование комментария
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('edit-comment-btn')) {
        const commentId = event.target.dataset.id;
        const commentTextSpan = document.querySelector(`#comment-${commentId} .comment-text`);
        const newText = prompt('Введите новый текст:', commentTextSpan.textContent);

        if (newText) {
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch(window.location.href, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ action: 'edit', comment_id: commentId, text: newText })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    commentTextSpan.textContent = newText;
                }
            });
        }
    }
});

// Удаление комментария
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('delete-comment-btn')) {
        const commentId = event.target.dataset.id;

        if (confirm('Вы уверены, что хотите удалить комментарий?')) {
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch(window.location.href, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ action: 'delete', comment_id: commentId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById(`comment-${commentId}`).remove();
                }
            });
        }
    }
});
