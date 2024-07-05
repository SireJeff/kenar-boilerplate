// script.js
document.addEventListener('DOMContentLoaded', () => {
    const popupContainer = document.getElementById('popup-container');
    const backButton = document.getElementById('back-button');
    const confirmButton = document.getElementById('confirm-button');
    const selectedName = document.getElementById('selected-name');
    const selectedDescription = document.getElementById('selected-description');
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    const modeIcon = document.getElementById('mode-icon');
    
    const nameOptions = [
        'نام آگهی ۱',
        'نام آگهی ۲',
        'نام آگهی ۳',
    ];

    const descriptionOptions = [
        'توضیحات ۱',
        'توضیحات ۲',
        'توضیحات ۳',
    ];

    function populateOptions(containerId, options, type) {
        const container = document.getElementById(containerId);
        options.forEach(option => {
            const button = document.createElement('button');
            button.className = 'option-button';
            button.textContent = option;
            button.addEventListener('click', () => selectOption(type, option, button));
            container.appendChild(button);
        });
    }

    function selectOption(type, option, button) {
        const selectedContainer = type === 'name' ? selectedName : selectedDescription;
        const buttons = document.querySelectorAll(`#${type}-options .option-button`);
        buttons.forEach(btn => btn.classList.remove('selected'));
        button.classList.add('selected');
        selectedContainer.textContent = option;
    }

    function showPopup() {
        popupContainer.classList.remove('hidden');
    }

    function closePopup() {
        popupContainer.classList.add('hidden');
        // پاک کردن انتخاب‌ها
        selectedName.textContent = '';
        selectedDescription.textContent = '';
        const buttons = document.querySelectorAll('.option-button');
        buttons.forEach(btn => btn.classList.remove('selected'));
    }

    function toggleDarkMode() {
        document.body.classList.toggle('dark-mode');
        if (document.body.classList.contains('dark-mode')) {
            modeIcon.src = "/static/sun.png";
            modeIcon.alt = 'Light Mode';
        } else {
            modeIcon.src = "/static/moon.png";
            modeIcon.alt = 'Dark Mode';
        }
    }

    backButton.addEventListener('click', closePopup);
    confirmButton.addEventListener('click', () => {
        // Handle final selection confirmation
        alert('انتخاب قطعی انجام شد!');
        closePopup();
    });

    darkModeToggle.addEventListener('click', toggleDarkMode);

    // Populate options
    populateOptions('name-options', nameOptions, 'name');
    populateOptions('description-options', descriptionOptions, 'description');

    // For demonstration, show the pop-up after 1 second
    setTimeout(showPopup, 1000);
});
