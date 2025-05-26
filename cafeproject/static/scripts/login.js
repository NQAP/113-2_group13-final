document.getElementById('login-form').addEventListener('submit', async function (e) {
e.preventDefault();
const username = document.getElementById('username').value;
const password = document.getElementById('password').value;
const msgEl = document.getElementById('msg');
try {
	const res = await fetch('/cafe/api/token/', {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ username, password })
	});
	const data = await res.json();
	if (res.ok) {
		console.log('登入成功，令牌:', data);
		localStorage.setItem('access', data.access);
        const userdata = JSON.parse(atob(data.access.split('.')[1]));
        console.log(userdata)
		localStorage.setItem('refresh', data.refresh);
		if (msgEl) {
			msgEl.className = 'success';
			msgEl.innerText = '登入成功，跳轉中...';
		}
		// setTimeout(() => {
		// 	console.log('準備跳轉...');
		// 	window.location.href = '/';
		// }, 1000);
	} else {
		if (msgEl) {
			msgEl.className = 'error';
			msgEl.innerText = '登入失敗：' + (data.detail || '請確認帳號密碼');
		}
	}
} catch (err) {
	console.error('Login error:', err);
	if (msgEl) {
		msgEl.className = 'error';
		msgEl.innerText = '發生錯誤，請稍後再試';
	}
}
});
