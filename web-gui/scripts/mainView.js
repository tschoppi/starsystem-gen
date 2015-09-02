$(document).ready(function() {

    $("#generate").click(function (e) {
        $.post("/generate", {"mustHaveGarden": document.getElementById("garden").checked})
            .done(function (starSystem) {
                document.getElementById("overview").innerHTML = starSystem.message;
            });
        e.preventDefault();
    });
});