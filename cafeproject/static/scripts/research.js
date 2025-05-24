let map;
let markers = [];

window.initMap = function () {
	const center = { lat: 25.0173, lng: 121.5398 }; // 台大位置

	map = new google.maps.Map(document.getElementById("map"), {
		center: center,
		zoom: 15,
	});

	loadFilteredCafes(cafes); // 初始載入全部資料
};

function loadFilteredCafes(cafeList) {
	clearMarkers();

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
	});
}

function clearMarkers() {
	markers.forEach((marker) => marker.setMap(null));
	markers = [];
}

document.addEventListener("DOMContentLoaded", () => {
	const form = document.getElementById("filter-form");

	form.addEventListener("submit", (e) => {
		e.preventDefault();

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
			console.log("✅ 評分條件：", minRating);
		}

		const filteredCafes = cafes.filter((cafe) => {
			// 篩選 tag
			if (filters.length > 0 && !filters.every(tag => cafe.tags.includes(tag))) {
				return false;
			}

			// ✅ 篩選低消（範圍交集邏輯）
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

			return true;
		});

		console.log("結果：", filteredCafes.length, "家店符合條件");
		loadFilteredCafes(filteredCafes);
	});
});
