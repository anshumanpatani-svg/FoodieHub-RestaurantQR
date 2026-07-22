
const menu=document.getElementById("menu-toggle");

const nav=document.getElementById("nav-menu");

const close=document.getElementById("close-menu");

const overlay=document.querySelector(".overlay");

menu.onclick=()=>{

nav.classList.add("active");

overlay.classList.add("show");

}

close.onclick=()=>{

nav.classList.remove("active");

overlay.classList.remove("show");

}

overlay.onclick=()=>{

nav.classList.remove("active");

overlay.classList.remove("show");

}

