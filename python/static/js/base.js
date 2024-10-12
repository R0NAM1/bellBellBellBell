function registerEventListeners() {
    var userElement = document.getElementById('userHover');
    console.log(userElement)

    userElement.addEventListener('mouseover', () => {
        var popup = document.getElementById('usernameDropdown');
        popup.style.display = 'block';
    });

    userElement.addEventListener('mouseout', () => {
        var popup = document.getElementById('usernameDropdown');
        popup.style.display = 'none';
    });
}

window.onload = registerEventListeners();