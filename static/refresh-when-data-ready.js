var polling_url = document.currentScript.getAttribute('polling_url');

function indicateError() {
    alert('Error');
}

function handleStatusDuringPolling(computing) {
    if (!computing){
        clearInterval(pollInterval);
        location.reload();
    }
}

function refreshPageAfterComputeSucceeds() {
    var poll = function() {
        $.ajax({
            type: "GET",
            url: polling_url,
            success: function(result) {
                const computing = result.computing;
                handleStatusDuringPolling(computing);
            },
            error: function(result) {
                clearInterval(pollInterval);
                indicateError();
            }
        })
    }

    pollInterval = setInterval(poll, 500);

    poll();
}

$(document).ready(function(){
    refreshPageAfterComputeSucceeds();
});
