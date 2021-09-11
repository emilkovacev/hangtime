window.addEventListener('resize', function (){
    let header = document.getElementById('header')
    header.style.fontSize = 'x-large'
    header.innerHTML = 'You are viewing about ' + (window.innerWidth / 311 * window.innerHeight / 371).toString() + ' Big Yoshis';
})