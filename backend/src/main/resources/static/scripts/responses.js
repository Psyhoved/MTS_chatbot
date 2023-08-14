let allMessages = ''

function getBotResponse(input) {

    allMessages += ' '
    allMessages += input

    // Simple responses
    if (input === "testFront") {
        return "Проверка фронтенда";
    } else {
        return postRequest("chat/getBotNextMessage", allMessages);
    }
}

function postRequest(url, data) {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", url);
    xhr.responseType = "json"
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify(data));
    xhr.onload = function () {
        if (xhr.status === 200) {
            const response = xhr.response['MTS_chatbot'];
            allMessages += ' '
            allMessages += response
            handleBotResponse(response)
        } else {
            // Return an error message if the status code is not 200
            alert("Error: " + xhr.status);
        }
    };
}