let map;
let markers = [];

window.initMap = function () {
	const center = { lat: 25.0173, lng: 121.5398 }; // 台大位置
  
	map = new google.maps.Map(document.getElementById("map"), {
	  center: center,
	  zoom: 15,
	});
  
	loadCafes();
}

// // 假資料（後續可改成從後端抓資料）
// const cafes = [
//   	{
// 		name: "DDD Cafe",
// 		location: { lat: 25.0176, lng: 121.5378 },
// 		address: "台北市大安區某路1號",
// 		image_url:
// 		"https://hips.hearstapps.com/hmg-prod/images/vergerg-1676879198.jpg",
// 		detail_url: "/cafe/ddd-cafe", // → 導向 Django 內容頁
// 		tags: ["unlimited_time", "has_socket", "has_meal"],
// 	},
// 	{
// 		name: "ABC Coffee",
// 		location: { lat: 25.019, lng: 121.5405 },
// 		address: "台北市大安區某路2號",
// 		image_url:
// 		"https://doqvf81n9htmm.cloudfront.net/data/Luke1226_165/2020-02/%E5%92%96%E5%95%A1%E5%BB%B3/%E5%8F%B0%E5%8C%97%E7%99%AE%E5%92%96%E5%95%A1_40a.jpg",
// 		detail_url: "/cafe/abc-coffee",
// 		tags: ["quiet", "pet_friendly"],
//   	},
// ];

function loadCafes(filters = []) {
	clearMarkers();

	cafes.forEach((cafe) => {
		// 若有篩選條件，且 cafe 不符合，則略過
		if (
			filters.length > 0 &&
			!filters.every((tag) => cafe.tags.includes(tag))
		) {
			return;
		}

		const marker = new google.maps.Marker({
			position: cafe.location,
			map,
			title: cafe.name,
		});

		const infowindow = new google.maps.InfoWindow({
			content: `
				<div style="max-width: 220px;">
					<a href="${cafe.detail_url}" target="_blank" style="text-decoration: none; color: inherit;">
						<img src="${cafe.image_url}" alt="${cafe.name}" style="width: 100%; height: auto; border-radius: 8px; margin-bottom: 5px;">
						<strong>${cafe.name}</strong><br>
						<span style="font-size: 0.9rem;">${cafe.address}</span>
					</a>
				</div>
			`,
		});

		marker.addListener("mouseover", () => {
			infowindow.open(map, marker);
		});

		marker.addListener("mouseout", () => {
			infowindow.close();
		});

		marker.addListener("click", () => {
			window.open(cafe.detail_url, "_blank");
		});

		markers.push(marker);
	});
}

function clearMarkers() {
	markers.forEach((marker) => marker.setMap(null));
	markers = [];
}

// 當頁面載入完成後加上監聽器
document.addEventListener("DOMContentLoaded", () => {
	const form = document.getElementById("filter-form");

	form.addEventListener("submit", (e) => {
		e.preventDefault();

		const filters = [];

		if (document.getElementById("unlimited_time").checked)
			filters.push("unlimited_time");
		if (document.getElementById("has_socket").checked)
			filters.push("has_socket");
		if (document.getElementById("has_meal").checked)
			filters.push("has_meal");
		if (document.getElementById("quiet").checked)
			filters.push("quiet");
		if (document.getElementById("pet_friendly").checked)
			filters.push("pet_friendly");

		console.log("篩選條件：", filters);

		loadCafes(filters); // 根據篩選重新載入
	});
});
