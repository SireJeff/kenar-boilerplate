// script.js
document.addEventListener('DOMContentLoaded', () => {
    const popupContainer = document.getElementById('popup-container');
    const backButton = document.getElementById('back-button');
    const confirmButton = document.getElementById('confirm-button');
    const selectedName = document.getElementById('selected-name');
    const selectedDescription = document.getElementById('selected-description');
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    const modeIcon = document.getElementById('mode-icon');
    const userPostsContainer = document.getElementById('user-posts');
    
    const nameOptions = [
        'نام آگهی ۱',
        'نام آگهی ۲',
        'نام آگهی ۳',
    ];

    const descriptionOptions = [
        'توضیحات ۱',
        'توضیحات 2',
        'توضیحات 3',
    ];

    const userPosts = [
        { id: 1, name: 'آگهی ۱', description: 'توضیحات آگهی ۱' },
        { id: 2, name: 'آگهی ۲', description: 'توضیحات آگهی ۲' },
        { id: 3, name: 'آگهی ۳', description: 'توضیحات آگهی ۳' },
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

    function populateUserPosts(posts) {
        posts.forEach(post => {
            const listItem = document.createElement('li');
            listItem.textContent = `${post.name} - ${post.description}`;
            listItem.addEventListener('click', () => selectUserPost(post));
            userPostsContainer.appendChild(listItem);
        });
    }

    function selectUserPost(post) {
        // ارسال درخواست به دیتابیس برای انتخاب این آگهی
        fetch('/api/select_post', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ postId: post.id }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('آگهی انتخاب شد!');
            } else {
                alert('خطایی رخ داده است. لطفاً دوباره تلاش کنید.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('خطایی رخ داده است. لطفاً دوباره تلاش کنید.');
        });
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

    // Populate user posts
    populateUserPosts(userPosts);

    // For demonstration, show the pop-up after 1 second
    setTimeout(showPopup, 1000);
});
