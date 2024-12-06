// Заглушка для функции добавления записи
function addRecordForm() {
    fetch('/get_url_root')
        .then(response => response.json())  // Парсим ответ как JSON
        .then(data => {
            const baseUrl = data.base_url;  // Получаем базовый URL
            const fullUrl = `${baseUrl}add_record`;
            window.open(fullUrl, '_blank');  // Открываем полную ссылку в новой вкладке
        })
        .catch(error => console.error('Error:', error));  // Обрабатываем ошибки
}

// Заглушка для функции удаления записи
function deleteRecordForm() {
    fetch('/get_url_root')
        .then(response => response.json())  // Парсим ответ как JSON
        .then(data => {
            const baseUrl = data.base_url;  // Получаем базовый URL
            const fullUrl = `${baseUrl}delete_record`;
            window.open(fullUrl, '_blank');  // Открываем полную ссылку в новой вкладке
        })
        .catch(error => console.error('Error:', error));  // Обрабатываем ошибки
}
