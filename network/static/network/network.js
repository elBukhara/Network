document.addEventListener('DOMContentLoaded', function() {
    // When the button "EDIT" is clicked

    document.querySelectorAll('.btn.btn-outline-secondary.editing').forEach(button => {
        button.addEventListener('click', () => {
            // Getting the post's id 
            const id = button.dataset.id;
            console.log("The button edit was clicked for the post: " + id)

            // Selecting the buttons based on the id
            const buttonLike = document.getElementById('button-like-' + id);
            const buttonEdit = document.getElementById('button-edit-' + id);
            const editPost = document.getElementById('edit-post-' + id);

            let cardText = document.getElementById('card-text-' + id);
            let innerText = document.getElementById('innerText-' + id);

            buttonLike.style.display = 'none';
            buttonEdit.style.display = 'none';
            cardText.style.display = 'none';
            
            editPost.style.display = 'block';
            
            const text = cardText.innerHTML;
            innerText.value = text;

            const saveButton = document.getElementById('save-' + id);
            const cancelButton = document.getElementById('cancel-' + id);

            // When user SAVES the edited text
            saveButton.addEventListener('click', () => {
                const changedText = innerText.value;

                fetch(`/edit/${id}`, {
                    method: 'POST',
                    body: JSON.stringify ({
                    post: changedText
                    }),
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': "{{ csrftoken }}",  // Add this line if using CSRF protection
                    }
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Error updating post');
                    }
                    return response.json();
                })
                .then(result => {
                    console.log(`Edited text: ${result.new_text}`)
                        cardText.innerHTML = changedText;

                        buttonLike.style.display = 'inline-block';
                        buttonEdit.style.display = 'inline-block';
                        cardText.style.display = 'block';
                        
                        editPost.style.display = 'none';
                });
            });
            // When user CANCELS the edited  text
            cancelButton.addEventListener('click', () => {
                buttonLike.style.display = 'inline-block';
                buttonEdit.style.display = 'inline-block';
                cardText.style.display = 'block';
                editPost.style.display = 'none';
            });
        });
    });

    // Add event listener to all LIKE buttons
    document.querySelectorAll('.btn.btn-outline-danger').forEach(button => {
        button.addEventListener('click', () => {
            // Get post ID from data attribute
            const id = button.value;

            const likeIcon = document.getElementById(id);
            let likeCount = document.getElementById('like-count-' +  id).innerHTML;
            
            let isLiked = likeIcon.classList.contains("fa-solid");
            
            // Send POST request to like/unlike view
            fetch(`/like/${id}`, {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                console.log(data)
                // Update like button icon and count
                if (isLiked) {
                    likeIcon.className = "fa-regular fa-heart";
                    likeCount--
                    
                } else {
                    likeIcon.className = "fa-solid fa-heart";
                    likeCount++
                }
                document.getElementById('like-count-' +  id).innerHTML= likeCount;
                isLiked = !isLiked;
                // const likeButton = document.querySelector(`#${id}`);

            });
        });
    }); 
});  