window.addEventListener('resize', function (){
    let desc = document.getElementsByClassName('desc')[0]
    desc.style.fontSize = 'x-large'
    desc.innerHTML = 'You are viewing about ' + (window.innerWidth / 311 * window.innerHeight / 371).toString() + ' Big Yoshis';
})