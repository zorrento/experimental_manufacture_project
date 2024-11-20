// filter.js

// Функция для фильтрации маркеров на карте
function filterMarkers() {
    // Получаем состояния чекбоксов
    const competitorsChecked = document.getElementById('competitors-checkbox').checked;
    const depositsChecked = document.getElementById('deposits-checkbox').checked;
    const salesChecked = document.getElementById('sales-checkbox').checked;

    // Заглушка для применения фильтров (реализуйте логику отображения маркеров)
    console.log('Фильтры активны: ');
    console.log('Конкуренты: ' + competitorsChecked);
    console.log('Депозиты: ' + depositsChecked);
    console.log('Продажи: ' + salesChecked);
    
    // Здесь можно будет добавить логику фильтрации маркеров на карте в зависимости от состояния чекбоксов
}
