// 選取所有 .card 元素
const visitedcards = document.querySelectorAll('.visitedcard');

visitedcards.forEach(card => {
  const link = card.getAttribute('data-link');     // 例如 ./Dogpedia.html
  const breed = card.getAttribute('data-breed');   // 例如 Poodle、Shiba_Inu 等

  // 滑鼠進入，翻轉卡片
  card.addEventListener('mouseenter', () => {
    card.style.height = '30.5vh';
    card.style.cursor = 'pointer';
    card.style.boxShadow = '0 0 10px #999999';
  });

  // 滑鼠離開，恢復正面
  card.addEventListener('mouseleave', () => {
    card.style.height = '30vh';
    card.style.cursor = '';
    card.style.boxShadow = '';
  });

  // 點擊跳轉到對應品種的 Dogpedia 頁面
  card.addEventListener('click', () => {
    // 附上網址參數 ?breed=品種名稱
    window.location.href = link;
  });
});