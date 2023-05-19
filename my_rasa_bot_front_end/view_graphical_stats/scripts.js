
const audio_click = new Audio("../audios/click.mp3");

function openNav() {
    document.getElementById("mySidenav").style.width = "350px";
    audio_click.play();
  }

  function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    audio_click.play();
  }


  host = 'http://localhost:5005/webhooks/rest/webhook'

  function send(message) {
    console.log("User Message:", message)
    $.ajax({
        url: host,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            "message": message,
            "sender": "User"
        }),
        success: function(data, textStatus) {
            if (data != null) {
                setBotResponse(data);
            }
            console.log("Rasa Response: ", data, "\n Status:", textStatus)
        },
        error: function(errorMessage) {
            console.log('Error' + errorMessage);

        }
    });
    
}

function refresh(){
   msg="update all graphs"
   rasaURL='http://localhost:5005/webhooks/rest/webhook'
   fetch(rasaURL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        sender: "user",
        message: msg,
      }),
    }).then((response) => response.json())
      .then((data) => {
        if (data.length > 0) {
          let rasaResponse = data[0]["text"];
          console.log(rasaResponse)
          if (rasaResponse== "graphs have been updated. kindly refresh the page."){
            console.log("images updated refreshing page now.")
            location.reload();
          }
          
          
         // conversationHistory += `${rasaResponse}\n`;
        }
      })
      .catch((error) => {
        console.log("Error:", error);
        
      });
  // location.reload();   //to automatically refresh page. like browser refresh button , but also removes the prev console.logs
  audio_click.play();
  console.log("please refresh the page if still not updated")
   
}

