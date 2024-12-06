// menu.js

// Функция для сворачивания/раскрывания меню
function toggleMenu() {
    const menu = document.getElementById('menu');
    const menuIcon = document.getElementById('menu-icon');
    const menuCollapseIcon = document.getElementById('menu-collapse-icon');

    let menuState;

    if (menu.classList.contains('menu-collapsed')) {
        menu.classList.remove('menu-collapsed');
        menu.classList.add('menu-expanded');
        menuIcon.style.display = 'block';
        menuCollapseIcon.classList.add('hidden');
        menuState = 'expanded'; // Меню раскрыто
    } else {
        menu.classList.remove('menu-expanded');
        menu.classList.add('menu-collapsed');
        menuIcon.style.display = 'none';
        menuCollapseIcon.classList.remove('hidden');
        menuState = 'collapsed'; // Меню свернуто
    }
}

// поиск продаж определенной машины
// function searchMachineSaleInfo() {
//     const machineId = document.getElementById("search-machine-id").value;

//     if (machineId.trim()) {
//         fetch(`/search_by_machine?machine_id=${machineId}`)
//             .then(response => {
//                 if (!response.ok) {
//                     throw new Error(`HTTP error! status: ${response.status}`);
//                 }
//                 return response.text(); // Получаем HTML
//             })
//             .then(html => {
//                 window.location.href = `/search_by_machine?machine_id=${machineId}`; 
//             })
//             .catch(error => {
//                 console.error('Error:', error);
//                 // Обработка ошибки
//             });
//     }
// }

// Функция для скрытия всех групп меток
function hideMarkerGroups(map) {
    map.eachLayer(function (layer) {
        if (layer instanceof L.FeatureGroup) {
            map.removeLayer(layer);
        }
    });
}

// // Функция для показа маркеров поиска
// function showSearchMarkers(searchMarkers, map) {
//     hideMarkerGroups(map); // Убираем существующие метки
//     searchMarkers.addTo(map); // Добавляем метки поиска
// }

// // Функция для возврата групп "Продажи" и "Конкуренты"
// function resetDefaultMarkers(map, salesGroup, competitorsGroup) {
//     hideMarkerGroups(map); // Убираем существующие метки
//     salesGroup.addTo(map); // Добавляем маркеры продаж
//     competitorsGroup.addTo(map); // Добавляем маркеры конкурентов
// }

function searchMachineSaleInfo() {
    const machineId = document.getElementById('search-machine-id').value; // Получаем номер машины из поля ввода

    if (machineId) {
        // Отправляем запрос на сервер
        fetch(`/search_by_machine?machine_id=${machineId}`, {
            method: 'GET',
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);  // Выводим ошибку, если она есть
            } else {
                // Если данные получены, обновляем карту
                document.getElementById('map').innerHTML = data.map;  // Обновляем контейнер карты
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Продажи не найдены.');
        });
    } else {
        alert('Пожалуйста, введите номер машины');
    }
}

function searchCitySaleInfo() {
    const cityName = document.getElementById('search-city-name').value; 

    if (cityName) {
        // Отправляем запрос на сервер
        fetch(`/search_by_city?city_name=${cityName}`, {
            method: 'GET',
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);  // Выводим ошибку, если она есть
            } else {
                // Если данные получены, обновляем карту
                document.getElementById('map').innerHTML = data.map;  // Обновляем контейнер карты
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Продажи не найдены.');
        });
    } else {
        alert('Пожалуйста, введите название города');
    }
}

// function resetDefaultMarkers() {
//     // Отправляем запрос на сервер для получения исходной карты
//     fetch('/')
//         .then(response => response.text())
//         .then(data => {
//             // Обновляем контейнер карты на странице
//             document.getElementById('map').innerHTML = data;
//         })
//         .catch(error => {
//             console.error('Error:', error);
//             alert('Произошла ошибка при сбросе карты.');
//         });
// }

function resetDefaultMarkers() {
    document.getElementById('search-machine-id').value = '';
    document.getElementById('search-city-name').value = '';

    fetch('/reset_map')
        .then(response => response.json())
        .then(data => {
            // Обновляем только карту
            document.getElementById('map').innerHTML = data.map;
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Произошла ошибка при сбросе карты.');
        });
}


