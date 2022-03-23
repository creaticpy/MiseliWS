$(document).ready(function () {
    $(document).keydown(function (e) {
        e = e || Event
        if (e.altKey && String.fromCharCode(e.keyCode) == 'W') {
            cerrar_tab()
        }

        if (e.ctrlKey && String.fromCharCode(e.keyCode) == 'W') {
            alert("ctr+w pressed!");
        }
    })

    window.onbeforeunload = confirmExit;

    function confirmExit() {
        return "You have attempted to leave this page. Are you sure?";
    }
})


