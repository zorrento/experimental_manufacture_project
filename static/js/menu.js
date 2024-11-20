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





// Заглушка для функции поиска по названию машины
function searchMachine() {
    const machineName = document.getElementById('search-machine-name').value;
    if (machineName) {
        alert(`Следующие данные найдены для: ${machineName}`);
    } else {
        alert('Введите название машины для поиска');
    }
}
