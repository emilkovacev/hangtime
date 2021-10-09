window.addEventListener('resize', function (){
    let header = document.getElementById('header')
    let desc = document.getElementsByClassName('desc')[0]
    desc.innerHTML = ''
    header.style.fontSize = 'x-large'
    header.innerHTML = 'You are viewing about ' + (window.innerWidth / 311 * window.innerHeight / 371).toString() + ' Big Yoshis';
})