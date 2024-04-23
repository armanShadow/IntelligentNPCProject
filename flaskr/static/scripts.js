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
            const snd = new Audio(data['TranslatedSpeechFile']);
            snd.play();
            creatBotMsgContainer(data['Response']);
            if (data["Question"]['isDetected']){
                loadQuestionContainer(data["Question"]);
            }
        }
    });
    event.preventDefault();
  });

});

document.addEventListener('DOMContentLoaded', function() {
    getChatHistory();
    getCurrentQuestion();
    }, false);

function loadQuestionContainer(question) {

    const questionSpan = document.getElementById("question");
    const questionText = document.createTextNode(question['Question']);
    questionSpan.innerHTML = '';
    questionSpan.appendChild(questionText);
    const categorySpan = document.getElementById("category");
    const categoryText = document.createTextNode(question['Category'] + " -- ");
    const difficultyText = document.createTextNode(question['Difficulty']);
    categorySpan.innerHTML = '';
    categorySpan.appendChild(categoryText);
    categorySpan.appendChild(difficultyText);
    const optionASpan = document.getElementById("optionA");
    const optionAText = document.createTextNode(question['Options']['A']);
    optionASpan.innerHTML = '';
    optionASpan.appendChild(optionAText);
    const optionBSpan = document.getElementById("optionB");
    const optionBText = document.createTextNode(question['Options']['B']);
    optionBSpan.innerHTML = '';
    optionBSpan.appendChild(optionBText);
    const optionCSpan = document.getElementById("optionC");
    const optionCText = document.createTextNode(question['Options']['C']);
    optionCSpan.innerHTML = '';
    optionCSpan.appendChild(optionCText);
    const optionDSpan = document.getElementById("optionD");
    const optionDText = document.createTextNode(question['Options']['D']);
    optionDSpan.innerHTML = '';
    optionDSpan.appendChild(optionDText);
}

function getCurrentQuestion() {
    $.ajax({
        type: "GET",
        url: "/getQuestion",
        success: function(data)
        {
            if (data["currQuestion"] != null){
                loadQuestionContainer(data["currQuestion"]);
            }
        }
    });
}

function getChatHistory() {
    $.ajax({
        type: "GET",
        url: "/chatHistory",
        success: function(data)
        {
            loadMessageContainer(data["ChatHistory"]);
        }
    });
}

function loadMessageContainer(chat_history) {
    for (let i = 0 ; i<chat_history.length; i++){
        if (chat_history[i].type == "HumanMessage"){
            creatPlayerMsgContainer(chat_history[i]['content']);
        }
        else {
            if (chat_history[i]['content']['Question']['isDetected']){
                loadQuestionContainer(chat_history[i]["content"]['Question']);
            }
            creatBotMsgContainer(chat_history[i]['content']['Response']);
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
    