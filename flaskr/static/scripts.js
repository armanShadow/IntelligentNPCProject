$(document).ready(function() {

    $("form").submit(function (event) {
    var formData = {
      user_input: $("#user_input").val(),
    };

    creatPlayerMsgContainer(formData['user_input']);

    $("#user_input").val('');

    $.ajax({
        type: "POST",
        url: "/chat",
        data: formData,
        dataType: "json",
        encode: true,
        success: function(data)
        {
            creatBotMsgContainer(data['Response']);
        }
    });
    event.preventDefault();
  });

});

document.addEventListener('DOMContentLoaded', function() {
    getChatHistory();
    }, false);

function getChatHistory() {
    let chat_history = null;
    $.ajax({
        type: "GET",
        url: "/chatHistory",
        success: function(data)
        {
            chat_history = data["ChatHistory"];
            loadMessageContainer(chat_history);
        }
    });
}

function loadMessageContainer(chat_history) {
    for (let i = 0 ; i<chat_history.length; i++){
        if (chat_history[i].type == "HumanMessage"){
            creatPlayerMsgContainer(chat_history[i].content);
        }
        else {
            creatBotMsgContainer(chat_history[i].content)
        }
    }
}

function creatBotMsgContainer(data) {
    const currentDiv = document.getElementById("card-body");
    const newDivBot = document.createElement('div');
    newDivBot.classList.add("d-flex", "justify-content-start", "mb-4");
    const innerDivBot = document.createElement('div');
    innerDivBot.classList.add("msg_cotainer");
    const botResponse = document.createTextNode(data);
    innerDivBot.appendChild(botResponse);
    newDivBot.appendChild(innerDivBot);
    currentDiv.appendChild(newDivBot);
}

function creatPlayerMsgContainer(data) {
    const currentDiv = document.getElementById("card-body");
    const newDivPlayer = document.createElement('div');
    newDivPlayer.classList.add("d-flex", "justify-content-end", "mb-4");
    const innerDivPlayer = document.createElement('div');
    innerDivPlayer.classList.add("msg_cotainer_send");
    const playerResponse = document.createTextNode(data);
    innerDivPlayer.appendChild(playerResponse);
    newDivPlayer.appendChild(innerDivPlayer);
    currentDiv.appendChild(newDivPlayer);
}
    