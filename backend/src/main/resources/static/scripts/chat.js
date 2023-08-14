// Collapsible
var coll = document.getElementsByClassName("collapsible");

for (let i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function () {
        this.classList.toggle("active");

        var content = this.nextElementSibling;

        if (content.style.maxHeight) {
            content.style.maxHeight = null;
        } else {
            content.style.maxHeight = content.scrollHeight + "px";
        }

    });
}

function getTime() {
    let today = new Date();
    hours = today.getHours();
    minutes = today.getMinutes();

    if (hours < 10) {
        hours = "0" + hours;
    }

    if (minutes < 10) {
        minutes = "0" + minutes;
    }

    return hours + ":" + minutes;
}

function wrapChatText(message, type) {
    return '<p class="' + type + '"><span>' + message + '</span></p>'
}

function wrapUserMessage(message) {
    return wrapChatText(message, 'userText')
}

function wrapBotMessage(message) {
    return wrapChatText(message, 'botText')
}

// Gets the first message
function firstBotMessage() {
    let firstMessage = "Я Света - нейросетевой ассистент по услугам МТС. Вы можете задавать мне вопросы об услугах МТС"
    document.getElementById("botStarterMessage").innerHTML = wrapBotMessage(firstMessage);

    let time = getTime();

    $("#chat-timestamp").append(time);
    document.getElementById("userInput").scrollIntoView(false);
}

firstBotMessage();

// Retrieves the response
function handleBotResponse(botResponse) {
    $("#chatbox").append(wrapBotMessage(botResponse));
    document.getElementById("chat-bar-bottom").scrollIntoView(true);
}

//Gets the text from the input box and processes it
function proceedUserMessage() {
    let userText = $("#textInput").val();

    if (userText === "") {
        return
    }

    let userHtml = wrapUserMessage(userText);

    $("#textInput").val("");
    $("#chatbox").append(userHtml);
    document.getElementById("chat-bar-bottom").scrollIntoView(true);

    setTimeout(() => {
        getBotResponse(userText);
    }, 1000)

}

function sendButton() {
    proceedUserMessage();
}

// Press enter to send a message
$("#textInput").keypress(function (e) {
    if (e.which == 13) {
        proceedUserMessage();
    }
});