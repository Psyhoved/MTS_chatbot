let history = ''

function getBotResponse(input) {

    request = "Клиент: " + input + "\n"

    // Simple responses
    if (input === "testFront") {
        return "Проверка фронтенда";
    } else {
        return postRequest("chat/getBotNextMessage", history, request);
        // return postRequest("chat/getBotNextMessage", input);
    }
}

function postRequest(url, history, request) {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", url);
    xhr.responseType = "json"
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(history + request);
    xhr.onload = function () {
        if (xhr.status === 200) {
            const response = xhr.response['MTS_chatbot'];
            history = "Помощник (Ты): " + response + "\n" + request
            handleBotResponse(response)
        } else {
            alert("Error: " + xhr.status);
        }
    };
}

function appendHistory(str) {
    history = substringTail(history, 4000)
    history += str
}

function substringTail(str, num) {
    if (num <= 0 || num > str.length) {
        return str;
    }
    return str.substring(str.length - num, str.length);
}