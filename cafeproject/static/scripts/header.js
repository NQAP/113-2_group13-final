document.addEventListener('DOMContentLoaded', function() {
  // 檢查是否登入，並切換選單顯示
  if (localStorage.getItem('access')) {
    const loginLink = document.querySelector('.login-link');
    const registerLink = document.querySelector('.register-link');
    const userMenu = document.querySelector('.user-menu');
    
    // 先確認元素存在再操作
    if (loginLink) loginLink.style.display = 'none';
    if (registerLink) registerLink.style.display = 'none';
    if (userMenu) userMenu.style.display = '';
  }

  // 登出按鈕事件
  const logoutBtn = document.getElementById('logout-btn');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', async function(e) {
      e.preventDefault();
      const access = localStorage.getItem('access');
      const refresh = localStorage.getItem('refresh');
      try {
        await fetch('/cafe/api/logout/', {
          method: 'POST',
          headers: {
            'Authorization': 'Bearer ' + access,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ refresh: refresh })
        });
      } catch (err) {
        console.error('登出失敗:', err); // 建議加入錯誤處理
      }
      // 清除 token 並跳轉
      localStorage.removeItem('access');
      localStorage.removeItem('refresh');
      window.location.href = '/cafe/login/';
    });
  }
});
