function make_active(caller) {
    let current = document.getElementsByClassName("active")[0];
    current.classList.remove("active");
    caller.classList.add("active");
    return;
}