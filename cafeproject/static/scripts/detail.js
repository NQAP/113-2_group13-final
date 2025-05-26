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
