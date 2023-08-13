function getBotResponse(input) {
    //rock paper scissors
    if (input == "rock") {
        return "paper";
    } else if (input == "paper") {
        return "scissors";
    } else if (input == "scissors") {
        return "rock";
    }

    // Simple responses
    if (input.lower === "привет") {
        return "Привет! Расскажите о вашей компании, и я смогу предложить вам несколько наших услуг";
    } else if (input.includes("жопа")) {
        return "Я не хочу разговаривать об этом";
    } else {
        return "В данный момент я не подключена к нейролингивстической модели";
    }
}

function postRequest(url, data) {
    // Create a new XMLHttpRequest object
    const xhr = new XMLHttpRequest();
    // Open the connection with the POST method and the URL
    xhr.open("POST", url);
    // Set the request header to indicate JSON content type
    xhr.setRequestHeader("Content-Type", "application/json");
    // Define what to do when the response is ready
    xhr.onload = function () {
        // Check if the status code is 200 (OK)
        if (xhr.status === 200) {
            // Parse the response text as a JSON object
            var response = JSON.parse(xhr.responseText);
            // Return a string representation of the response object
            return JSON.stringify(response);
        } else {
            // Return an error message if the status code is not 200
            return "Error: " + xhr.status;
        }
    };
    // Send the request with the data object as a JSON string
    xhr.send(JSON.stringify(data));
}