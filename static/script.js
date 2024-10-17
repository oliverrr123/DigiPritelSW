function toggleMenu() {
    if (menu.style.display == 'none') {
        menu.style.display = 'flex';
        toggle.style.background = 'radial-gradient(ellipse at center, rgba(0,0,0,0.33) 0%, rgba(0,0,0,0.9))'
    } else {
        menu.style.display = 'none';
        toggle.style.background = 'transparent';
    }
}

function changeColor(event) {
    document.getElementsByClassName('eye')[0].style.backgroundColor = event.target.style.backgroundColor;
    document.getElementsByClassName('eye')[1].style.backgroundColor = event.target.style.backgroundColor;
    document.getElementsByClassName('mouth')[0].style.backgroundColor = event.target.style.backgroundColor;
    // toggleMenu();
}
