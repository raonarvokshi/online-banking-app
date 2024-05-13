"use strict";

// ALERT MESSAGES TIMEOUT
const alertMsg = document.getElementById("alert-msg");

$(document).ready(function () {
    const alertMsg = $("#alert-msg");
    if (alertMsg.length) {
        setTimeout(function () {
            alertMsg.fadeOut(700, function () {
                alertMsg.remove();
            });
        }, 4000);
    }
});
