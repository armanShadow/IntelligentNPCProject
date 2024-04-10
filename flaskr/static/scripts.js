var chat_history = [];
$(document).ready(function() {

    $("form").submit(function (event) {

    var formData = {
      user_input: $("#user_input").val(),
    };

    $("#user_input").val('');


    const currentDiv = document.getElementById("card-body");

    const newDivPlayer = document.createElement('div');
    newDivPlayer.classList.add("d-flex", "justify-content-end", "mb-4");
    const innerDivPlayer = document.createElement('div');
    innerDivPlayer.classList.add("msg_cotainer_send");
    const playerResponse = document.createTextNode(formData['user_input']);
    innerDivPlayer.appendChild(playerResponse);
    newDivPlayer.appendChild(innerDivPlayer);
    currentDiv.appendChild(newDivPlayer);

    $.ajax({
        type: "POST",
        url: "/chat",
        data: formData,
        dataType: "json",
        encode: true,
        success: function(data)
        {
            chat_history.push({role: "Player", response: formData['user_input']});
            chat_history.push({role: "QuizMaster", response: data['Response']});

            const newDivBot = document.createElement('div');
            newDivBot.classList.add("d-flex", "justify-content-start", "mb-4");
            const innerDivBot = document.createElement('div');
            innerDivBot.classList.add("msg_cotainer");
            const botResponse = document.createTextNode(data['Response']);
            innerDivBot.appendChild(botResponse);
            newDivBot.appendChild(innerDivBot);
            currentDiv.appendChild(newDivBot);

        }
    });
    event.preventDefault();
  });

});
