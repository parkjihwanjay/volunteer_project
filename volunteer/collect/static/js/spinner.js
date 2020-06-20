const button = document.querySelector('.volunteer_button');
const spinner = document.querySelector('.loader')

button.addEventListener('click', SpinnerOn)

function SpinnerOn(event){
    spinner.style.display = "flex";
    // spinner.style.removeProperty('display');
    // console.log('스피너 동작');
}