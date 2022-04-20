window.onload = () => {
    title = document.getElementsByTagName('title')[0].innerHTML.toLowerCase()
    navbarItem = document.getElementById(title)
    if(navbarItem){
        navbarItem.classList.add('active')
    }    
}    