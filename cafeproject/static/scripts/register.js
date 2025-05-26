document.getElementById('register-form').addEventListener('submit', async function (e) {
	e.preventDefault();
	const username = document.getElementById('username').value;
	const password = document.getElementById('password').value;

	const res = await fetch('/cafe/api/register/', {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ username, password })
	});

	const data = await res.json();
	const msgEl = document.getElementById('msg');

	if (res.ok) {
		msgEl.className = 'success';
		msgEl.innerText = '註冊成功，前往登入頁...';
		setTimeout(() => {
			window.location.href = '/cafe/login/';
		}, 1500);
	} else {
		msgEl.className = 'error';
		msgEl.innerText = '註冊失敗：' + (data.error || '帳號可能已存在');
	}
});