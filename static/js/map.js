// Пример: добавление маркеров на карту

function addMarker(lat, lon, data) {
    var marker = L.marker([lat, lon]).addTo(map);
    marker.bindPopup(`Sale ID: ${data.sale_id}<br/>Value: ${data.sales_value_usd}`).openPopup();
}

fetch('/sales').then(response => response.json()).then(data => {
    data.forEach(sale => {
        // Здесь вы можете добавить логику для получения координат
        // Например, через ваш объект region или другие данные
        addMarker(20, 0, sale); // Используем примерные координаты
    });
});
