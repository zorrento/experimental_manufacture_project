// Заглушка для функции добавления записи
function addRecordForm() {
    const nameInput = document.getElementById('marker-name');
    const latInput = document.getElementById('marker-lat');
    const lngInput = document.getElementById('marker-lng');
    
    const name = nameInput.value;
    const lat = latInput.value;
    const lng = lngInput.value;

    if (name && lat && lng) {
        alert(`Запись добавлена: ${name}`);
        // Очистка полей ввода
        nameInput.value = '';
        latInput.value = '';
        lngInput.value = '';
    } else {
        alert("Заполните все поля");
    }
}

// Заглушка для функции удаления записи
function deleteRecordForm() {
    const idInput = document.getElementById('marker-id');
    
    const id = idInput.value;
    if (id) {
        alert(`Запись с ID ${id} удалена`);
        // Очистка поля ввода
        idInput.value = '';
    } else {
        alert("Введите ID записи для удаления");
    }
}
