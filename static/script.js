const map = L.map('map').setView([35.693124, 139.728893], 13);

// Tile Layerを追加
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// 円を描画する関数
function drawCircle(lon, lat, radius) {
    fetch(`/api/circle/${lon}/${lat}/${radius}`)
        .then(response => response.json())
        .then(data => {
            // 円を描画
            const circle = L.geoJSON(data.circle, {
                style: { color: 'red', weight: 2 }
            }).addTo(map);

            // ポリゴンを描画
            data.data.forEach(item => {
                L.geoJSON(item.geometry, {
                    style: { color: 'orange', weight: 1, fillOpacity: 0.5 }
                }).addTo(map);

                // ポリゴン情報をポップアップで表示
                L.geoJSON(item.geometry).bindPopup(
                    `Population: ${item.population}<br>File: ${item.file}`
                ).addTo(map);
            });
        })
        .catch(err => console.error(err));
}

// 初期値: 東京・防衛省を中心に半径9180mの円
drawCircle(139.728893, 35.693124, 9180);
