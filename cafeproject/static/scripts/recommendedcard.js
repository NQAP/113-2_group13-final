// Loading recommended website
document.addEventListener("DOMContentLoaded", function () {
    var recommendedpart = document.getElementById('recommendedcardcontainer');
    cafes.sort(function(a,b) {
        return b.rating - a.rating
    });
    for (let index = 0; index < 6; index++) {
        const cafe = cafes[index];
        const name = cafe.name;
        const imgSrc = cafe.image_url;
        const address = cafe.address;
        const rating = cafe.rating;
        const taglist = cafe.tags_list;
        const link = cafe.detail_url;
        const card = document.createElement("div");
        card.className = "recommendedcard";
        card.innerHTML = `
        <div class="recommendedimagecontainer">
            <img src="${imgSrc}" alt=${name} class="recommendedimage"/>
        </div>
        <div class="recommendedcardtext">
            <h3>${name}</h3>
            <p>當前評分：${rating}</p>
            <p>地址：${address}</p>
        </div>`
        recommendedpart.appendChild(card);
        // 滑鼠進入，翻轉卡片
        card.addEventListener('mouseenter', () => {
            card.style.cursor = 'pointer';
            card.style.boxShadow = '0 0 10px #999999';
        });

        // 滑鼠離開，恢復正面
        card.addEventListener('mouseleave', () => {
            card.style.cursor = '';
            card.style.boxShadow = '';
        });

        // 點擊跳轉到對應品種的 Dogpedia 頁面
        card.addEventListener('click', () => {
            // 附上網址參數 ?breed=品種名稱
            window.location.href = link;
        });
    }
});
