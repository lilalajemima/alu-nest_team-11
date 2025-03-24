document.addEventListener('DOMContentLoaded', () => {
    const loginNav = document.getElementById('login-nav');
    const signupNav = document.getElementById('signup-nav');
    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');

    // Switch to Sign Up form
    signupNav.addEventListener('click', () => {
        loginNav.classList.remove('active');
        signupNav.classList.add('active');
        loginForm.classList.add('hidden');
        signupForm.classList.remove('hidden');
    });

    // Switch to Login form
    loginNav.addEventListener('click', () => {
        signupNav.classList.remove('active');
        loginNav.classList.add('active');
        signupForm.classList.add('hidden');
        loginForm.classList.remove('hidden');
    });
}); 