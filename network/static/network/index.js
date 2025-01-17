document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.comment-button').forEach(button => {
        button.addEventListener('click', compose_comment);
    });
});

function compose_comment(event) {
    const postId = event.target.closest('form').querySelector('input[name="post_id"]').value;
    const commentUrl = event.target.dataset.url;

    // Create a pop-up text box for the comment
    let commentBox = document.createElement('div');
    commentBox.innerHTML = `
        <div class="comment-popup">
            <textarea id="comment-text" placeholder="Write your comment here..."></textarea>
            <button id="save-comment" class="btn btn-primary">Save</button>
            <button id="cancel-comment" class="btn btn-secondary">Cancel</button>
        </div>
    `;
    const popupContainer = document.querySelector(`#comment-popup-container-${postId}`);
    if (!popupContainer) {
        console.error(`#comment-popup-container-${postId} not found.`);
        return;
    }
    popupContainer.appendChild(commentBox);

    // Add event listeners for save and cancel buttons
    document.querySelector('#save-comment').addEventListener('click', function() {
        save_comment(postId, commentUrl);
    });
    document.querySelector('#cancel-comment').addEventListener('click', function() {
        popupContainer.removeChild(commentBox);
    });
}

function save_comment(postId, commentUrl) {
    let commentText = document.querySelector('#comment-text').value;
    if (commentText.trim() === '') {
        alert('Comment cannot be empty.');
        return;
    }

    // Create a form to submit the comment
    let form = document.createElement('form');
    form.method = 'POST';
    form.action = commentUrl;

    let postIdInput = document.createElement('input');
    postIdInput.type = 'hidden';
    postIdInput.name = 'post_id';
    postIdInput.value = postId;
    form.appendChild(postIdInput);

    let commentTextInput = document.createElement('input');
    commentTextInput.type = 'hidden';
    commentTextInput.name = 'comment_text';
    commentTextInput.value = commentText;
    form.appendChild(commentTextInput);

    let csrfTokenInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
    if (!csrfTokenInput) {
        console.error('CSRF token not found.');
        return;
    }
    let csrfToken = document.createElement('input');
    csrfToken.type = 'hidden';
    csrfToken.name = 'csrfmiddlewaretoken';
    csrfToken.value = csrfTokenInput.value;
    form.appendChild(csrfToken);

    document.body.appendChild(form);
    form.submit();
}