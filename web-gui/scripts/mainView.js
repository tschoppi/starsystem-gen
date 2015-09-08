$(document).ready(function() {

    $("#generate").click(function (e) {
        $.post("/generate", {"mustHaveGarden": document.getElementById("garden").checked})
            .done(function (starSystem) {
                console.log(starSystem);
            });
        e.preventDefault();
    });
});