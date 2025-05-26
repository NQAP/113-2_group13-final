document.addEventListener("DOMContentLoaded", function () {
    var link = window.location.href
    var getData = localStorage.getItem("visited")
    console.log(getData)
    if (getData){
        var Data = JSON.parse(getData);
        console.log(Data.includes(link));
        if (!Data.includes(link)) {
            if (Data.length == 3) {
                Data.shift();
            }
            Data.push(window.location.href);
            Data = JSON.stringify(Data);
            localStorage.setItem("visited", Data);
        }
    }
    else {
        var Data = [];
        Data.push(window.location.href);
        Data = JSON.stringify(Data);
        localStorage.setItem("visited", Data);
    }

    loadComments();
    createCommentForm();

    async function loadComments() {
        const csrftoken = $('[name="csrfmiddlewaretoken"]').val();
        // console.log(csrftoken)
        const commentsContainerId = 'comments-container';
        let commentsContainer = document.getElementById(commentsContainerId);
        commentsContainer.innerHTML = '<p>評論載入中...</p>';
        const url = window.location.href + 'comments/'
        const request = new Request(
            url,
            {
                method: 'POST',
                headers: {'X-CSRFToken': csrftoken},
                mode: 'same-origin' // Do not send CSRF token to another domain.
            }
        );
        const res = await fetch(request)
        if(res.ok){
            console.log(res);
            const data = await res.json();
            console.log(data);
            console.log(data.comments);
            comments = data.comments;

            displayCommentsData(comments, commentsContainer);
        }
        else{
            commentsContainer.innerHTML = '<p>載入評論失敗。</p>';
            console.error("載入評論錯誤:", error);
        }
            
            // .then(data => {
            //     const comments = JSON.parse(data.comments);
            //     displayCommentsData(comments, commentsContainer);
            // })
            // .catch(error => {
            //     commentsContainer.innerHTML = '<p>載入心情小語失敗。</p>';
            //     console.error("載入心情小語錯誤:", error);
            // });
    }

    function displayCommentsData(comments, container) {
        container.innerHTML = '';
        if(comments[0].user == -1){
            container.innerHTML += '<p class="nothing">還沒有任何評論</p>';
        }
        else if (comments.length > 0) {
            const ul = document.createElement('ul');
            comments.forEach(comment => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <p><strong>${comment.user} 評分：${comment.rating}</strong></p>
                    <p>評論：${comment.comment_text}</p>
                    <small>發布於 ${new Date(comment.created_at).toLocaleString()}</small>
                    `;
                ul.appendChild(li);
            });
            container.appendChild(ul);
        }
    }

    function createCommentForm() {
        const commentspart = document.getElementById('comments-section')
        let commentFormContainer = document.getElementById('comment-form-container');
        if (!commentFormContainer) {
            commentFormContainer = document.createElement('div');
            commentFormContainer.id = 'comment-form-container';
            commentspart.appendChild(commentFormContainer);
        }
        commentFormContainer.innerHTML = `
            <h3>留下你的評論</h3>
            <div class="rating-zone">
                <label for="rating">評分</label>
                <input type="number" id="rating" name="rating" min="1" max="5" value="{{ rating|default:'' }}">
                <small>請輸入 1 到 5 的評分</small>
            </div>
            <div class="text-zone">
                <textarea id="comment-text" rows="3" cols="50" placeholder="留下你的評論..."></textarea>
                <button id ="comment-sub" type="button" onclick="submitComment()">發布</button>
            </div>
            
        `;
        const token = localStorage.getItem('access');
        if (!token){
            document.getElementById('comment-text').setAttribute("disabled","disabled");
            document.getElementById('comment-text').setAttribute("placeholder", "登入來發表你的評論");
            document.getElementById('comment-sub').setAttribute("disabled","disabled");
        }
        else{
            document.getElementById('comment-text').removeAttribute("disabled");
            document.getElementById('comment-sub').removeAttribute("disabled");
        }
    }

    window.submitComment = function() {
        const commentText = document.getElementById('comment-text').value;
        const commentRating = document.getElementById('rating').value;
        var getData = localStorage.getItem('access');
        // var getDataArr = JSON.parse(getData);
        const token = String(localStorage.getItem('access'));
        console.log(token);
        const userdata = JSON.parse(atob(token.split('.')[1]));
        console.log(userdata);
        const url = window.location.href + 'add_comments/'
        const request = new Request(
            url,
            {
                method: 'POST',
                headers: {'X-CSRFToken': getCookie('csrftoken')},
                mode: 'same-origin', // Do not send CSRF token to another domain.
                body: JSON.stringify({ user: userdata.user_id, rating: commentRating, text: commentText })
            }
        );
        fetch(request)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                loadComments(); // 重新加載評論
                document.getElementById('comment-text').value = ''; // 清空輸入框
            } else {
                alert(data.message || '發布評論失敗');
            }
        })
        .catch(error => {
            alert('發布評論時發生錯誤。');
            console.error("發布評論錯誤:", error);
        });
    };

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                let cookie = cookies[i].trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = cookie.substring(name.length + 1);
                    break;
                }
            }
        }
        return cookieValue;
    }
})