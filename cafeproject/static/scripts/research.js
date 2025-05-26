console.log("✅ research.js 載入成功");
let map;
let markers = [];

window.initMap = function () {
	console.log("🗺️ initMap 被呼叫");
	const center = { lat: 25.0173, lng: 121.5398 }; // 台大位置

	map = new google.maps.Map(document.getElementById("map"), {
		center: center,
		zoom: 15,
	});

	loadFilteredCafes(cafes); // 初始載入全部資料
};

function loadFilteredCafes(cafeList) {
	clearMarkers();

	// 建立 bounds
	const bounds = new google.maps.LatLngBounds();

	cafeList.forEach((cafe) => {
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

		marker.addListener("mouseover", () => infowindow.open(map, marker));
		marker.addListener("mouseout", () => infowindow.close());
		marker.addListener("click", () => window.open(cafe.detail_url, "_blank"));

		markers.push(marker);

		// 每新增一個 marker，就把位置加到 bounds 中
		bounds.extend(cafe.location);
	});

	// 若 cafeList 不為空，才套用自動視野調整
	if (cafeList.length > 0) {
		map.fitBounds(bounds);
	}
}

function clearMarkers() {
	markers.forEach((marker) => marker.setMap(null));
	markers = [];
}

document.addEventListener("DOMContentLoaded", () => {
	console.log("✅ DOM 載入完成");
	const form = document.getElementById("filter-form");

	form.addEventListener("submit", (e) => {
		e.preventDefault();
		console.log("✅ 成功觸發 submit");

		// // 行政區對應中心座標
		// const districtCenters = {
		// 	"中山區": { lat: 25.0685, lng: 121.5250 },
		// 	"中正區": { lat: 25.0352, lng: 121.5198 },
		// 	"信義區": { lat: 25.0330, lng: 121.5623 },
		// 	"內湖區": { lat: 25.0832, lng: 121.5756 },
		// 	"大同區": { lat: 25.0631, lng: 121.5158 },
		// 	"大安區": { lat: 25.0266, lng: 121.5434 },
		// 	"松山區": { lat: 25.0505, lng: 121.5571 },
		// 	"永和區": { lat: 25.0152, lng: 121.5169 },
		// 	"中和區": { lat: 24.9961, lng: 121.5076 },
		// 	"萬華區": { lat: 25.0332, lng: 121.4972 }
		// };

		const filters = [];

		if (document.getElementById("unlimited_time").checked) filters.push("unlimited_time");
		if (document.getElementById("has_socket").checked) filters.push("has_socket");
		if (document.getElementById("has_meal").checked) filters.push("has_meal");
		if (document.getElementById("quiet").checked) filters.push("quiet");
		if (document.getElementById("pet_friendly").checked) filters.push("pet_friendly");

		// 低消範圍條件（支援 min/max 下拉選單）
		const minVal = document.getElementById("min_spending_min").value;
		const maxVal = document.getElementById("min_spending_max").value;

		let minLimit = minVal ? parseInt(minVal) : null;
		let maxLimit = maxVal ? parseInt(maxVal) : null;

		const minSpendingFilterFn = (min, max) => {
			if (minLimit !== null && (min === null || min < minLimit)) return false;
			if (maxLimit !== null && (max === null || max > maxLimit)) return false;
			return true;
		};

		// 評分條件
		const ratingSelect = document.getElementById("rating").value;
		let minRating = null;
		if (ratingSelect && ratingSelect !== "不限") {
			minRating = parseFloat(ratingSelect);
		}

		// 行政區條件
		const selectedDistrict = document.getElementById("district").value;

		const filteredCafes = cafes.filter((cafe) => {
			// 篩選 tag
			if (filters.length > 0 && !filters.every(tag => cafe.tags.includes(tag))) {
				return false;
			}

			// 篩選低消（範圍交集邏輯）
			if (minSpendingFilterFn) {
				const min = cafe.min_spending_min;
				const max = cafe.min_spending_max;
				if (!minSpendingFilterFn(min, max)) return false;
			}

			// 篩選評分
			if (minRating !== null) {
				const rating = Number(cafe.rating);
				if (isNaN(rating) || rating < minRating) return false;
			}

			// 篩選行政區
			if (selectedDistrict && cafe.district !== selectedDistrict) {
				return false;
			}

			return true;
		});

		loadFilteredCafes(filteredCafes);

		// // 根據選擇區域切換地圖中心
		// if (selectedDistrict && selectedDistrict !== "不限") {
		// 	const center = districtCenters[selectedDistrict];
		// 	if (center) {
		// 		map.panTo(center); // 滑動
		// 		setTimeout(() => {
		// 			map.setZoom(15);
		// 		}, 300);
		// 	}
		// } else {
		// 	map.panTo({ lat: 25.0173, lng: 121.5398 });
		// 	setTimeout(() => {
		// 		map.setZoom(15);
		// 	}, 300);
		// }		
	});
});
