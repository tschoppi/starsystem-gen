function regenerate(){
    current_path = window.location.href;
    current_path = current_path.split("&seed")[0]
    window.location.href = current_path
}