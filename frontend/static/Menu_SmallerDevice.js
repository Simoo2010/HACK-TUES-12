function toggleMenu() {
  const menu = document.getElementById("nav-links");
  menu.classList.toggle("show");
}

document.getElementById("menu-btn").addEventListener("click", toggleMenu);