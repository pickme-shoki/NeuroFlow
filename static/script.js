function toggleTheme() {
    document.body.classList.toggle('dark');
    const isDark = document.body.classList.contains('dark');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
}

window.onload = () => {
    if(localStorage.getItem('theme') === 'dark') document.body.classList.add('dark');
    const quotes = [
        "Health is a state of complete harmony of the body, mind and spirit.",
        "The human body is the best picture of the human soul.",
        "Your brain is the most complex organ; nourish it with care."
    ];
    document.getElementById('health-quote').innerText = quotes[Math.floor(Math.random()*quotes.length)];
};