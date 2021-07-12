async function getData() {
    setConversations()
    setSystems()
}

async function setSystems() {
    let response = await fetch('/systems_list/', {
        method: 'GET'
    });
    let answer = await response.json();
    let select = document.getElementById('system');
    for (const system of answer)
        $(select).append('<option value=' + system.id + ' class="System">' + system.system_name + '</option>')
}

async function setConversations() {
    let response = await fetch('/conversations_list/', {
        method: 'GET'
    });
    let answer = await response.json();
    let select = document.getElementById('system');
    for (const conversation of answer)
        $(select).append('<option value=' + conversation.id + ' class="Conversation">' + conversation.conversation_name + '(' + conversation.messenger_name + ')' + '</option>')
}

async function sendData() {
    const csrftoken = getCookie('csrftoken')
    let selected = $("#sys option:selected")
    data = {
        id: selected.val(),
        type: selected.attr('class')
    }
    $.ajax({
        type: 'POST',
        url: "/send_request_for_access/",
        headers: {
            "X-CSRFToken": csrftoken,
            'Content-Type': 'application/json'
        },
        data: JSON.stringify(data),
        datatype: "json",
        success: function () {
            let snackbar = document.getElementById("snackbar");
            snackbar.className = "show";
            setTimeout(function () {
                snackbar.className = snackbar.className.replace("show", "");
            }, 3000);
        }
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}