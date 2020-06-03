document.addEventListener('DOMContentLoaded', () => {

    // clear on login page
    localStorage.clear()

    document.querySelector('#form').onsubmit = () => {
        let username = document.querySelector('#username').value;
        // Store username in local storage
        localStorage.setItem('username', username);
    }

});