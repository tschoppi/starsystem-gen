function regenerate(){
    current_path = window.location.href
    current_path = current_path.split("&seed")[0]
    window.location.href = current_path
}

function go_back(){
    current_path = window.location.href.split("/")
    current_path.pop()
    current_path = current_path.join("/")
    window.location.href = current_path
}