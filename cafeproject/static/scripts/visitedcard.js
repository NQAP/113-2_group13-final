// Loading visited website
document.addEventListener("DOMContentLoaded", function () {
    var getData = localStorage.getItem("visited")
    console.log(getData)
    if (getData){
        var Data = JSON.parse(getData)
        for (let index = 0; index < Data.length; index++) {
            loadvisitedcard(Data[index]);
        }
    }
});

async function loadvisitedcard(data) {
    var visitedpart = document.getElementById('visitedcardcontainer');
    const csrftoken = $('[name="csrfmiddlewaretoken"]').val();
    const request = new Request(
        data,
        {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            mode: 'same-origin' // Do not send CSRF token to another domain.
        }
    );
    const res = await fetch(request)
    if(res.ok){
        console.log(res);
        const details = await res.json();
        datalist = details.cafe
        console.log(datalist);
        const name = datalist.name;
        const imgSrc = datalist.image_url;
        const address = datalist.address;
        const rating = datalist.rating;
        const taglist = datalist.tags_list;
        const card = document.createElement("div");
        card.className = "visitedcard";
        card.innerHTML = `
        <div class="visitedimagecontainer">
            <img src="${imgSrc}" alt=${name} class="visitedimage"/>
        </div>
        <div class="visitedcardtext">
            <h3>${name}</h3>
            <p>當前評分：${rating}</p>
            <p>地址：${address}</p>
        </div>`
        tag = document.createElement("p");
        for (let index = 0; index < taglist.length; index++) {
            tag.innerHTML.text += taglist[index]
        }
        card.appendChild(tag);
        visitedpart.appendChild(card);
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
            window.location.href = data;
        });
    } 
    
}
