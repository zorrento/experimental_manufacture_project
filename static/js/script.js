const map = L.map('map').setView([20, 0], 2); // Центр карты и начальный уровень масштабирования
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
}).addTo(map);

// Функция для загрузки данных о продажах
async function loadSalesData() {
    const response = await fetch('/api/sales');
    const salesData = await response.json();

    salesData.forEach(sale => {
        // Здесь вы можете добавить маркеры на карту в зависимости от региона или других параметров
        L.marker([20, 0]).addTo(map) // Замените координаты на реальные
            .bindPopup(Sale ID: ${sale.sale_id}<br>Value: ${sale.sales_value_usd} USD);
    });
}

// Загружаем данные при загрузке страницы
loadSalesData();