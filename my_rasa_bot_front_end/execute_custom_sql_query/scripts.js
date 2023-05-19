const audio_click = new Audio("../audios/click.mp3");

function openNav() {
    document.getElementById("mySidenav").style.width = "350px";
    audio_click.play();
  }
  
  function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    audio_click.play();
  }


  // for cmd prompt like execute_custom_sql_query.html

  // The fetch() function is a built-in JavaScript function for making HTTP requests to a server. In the code snippet you provided, it is used to send a user's message to the Rasa server for processing.
  // then is  used to handle response

const consoleOutput = document.getElementById("console");
const input = document.getElementById("input");
let conversationHistory = "";
let originalHeight = input.style.height;

input.addEventListener("keydown", function (event) {
  if (event.keyCode === 13 && !event.shiftKey) {
    event.preventDefault();
    submitCommand();
    input.style.height = originalHeight; // reset the height to its original value
  } else if (event.keyCode === 13 && event.shiftKey) {
    input.value += "\n";
    input.style.height = input.scrollHeight + "px"; // expand the textarea height
  }
});


function addTableFromString(dataString) {
  
   data = dataString.split("]");

  // Create a table element
  const table = document.createElement('table'); 

  // Create the table header rows
 
    const colData = data[0].split("$");
    const row = document.createElement('tr');
      colData.forEach((cellData) => {
        if(cellData!="") {
        const th = document.createElement('th');
        cellData= cellData.trim().replace("[","");
        th.textContent = cellData
        row.appendChild(th);
        }
    });
    table.appendChild(row);
  

 
  // Create the table body rows
  for (let i = 1; i < data.length; i++) {
    const colData = data[i].split("$");
    
      const row = document.createElement('tr');
      colData.forEach((cellData) => {
        if(cellData!=""){
        const td = document.createElement('td');
        td.textContent = cellData.trim().replace("[","");
        row.appendChild(td);
        }
    });
    table.appendChild(row);
    
    
  }

  consoleOutput.innerHTML += '<span style="color: #7289DA;">JUICERO@MYSQL:$</span>\n';
  consoleOutput.appendChild(table);
  consoleOutput.scrollTop = consoleOutput.scrollHeight;
}






function submitCommand() {
  const command = input.value.trim();
  if (command.length > 0) {
    addToConsole(`<span style="color: #7289DA;">JUICERO@MYSQL:$</span>${command}\n`);
    //conversationHistory += `JUICERO@MYSQL:$ ${command}\n`;
    input.value = "";
    // Replace the URL with your Rasa server endpoint
    const rasaURL = "http://localhost:5005/webhooks/rest/webhook";
    const initial_msg="execute custom mysql command";
    fetch(rasaURL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        sender: "user",
        message: initial_msg,
      }),
    }).then((response) => response.json())
      .then((data) => {
        if (data.length > 0) {
          let rasaResponse = data[0].text;
          console.log(rasaResponse)
          if(rasaResponse=="enter mysql command"){
            console.log("mysql command = ",{command});
            fetch(rasaURL, {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                sender: "user",
                message: command,
              }),
            }).then((response) => response.json())
              .then((data) => {
                if (data.length > 0) {
                  let rasaResponse = data[0].text;
                  console.log(data[0])
                  if (rasaResponse.includes("Here is the result of your query:\n")) {
                    console.log("table found!");
                    rasaResponse=rasaResponse.replace("Here is the result of your query:\n","")
                    console.log("after removing Here is the result of your query:\n")
                    console.log(rasaResponse)
                    addTableFromString(rasaResponse)
                  } else {
                    console.log("table not found!");
                    addToConsole(`<span style="color: #7289DA;">JUICERO@MYSQL:$</span> ${rasaResponse}\n`);
                  }
                  
                 //console.log(data[0])
                  

                 
                  //conversationHistory += `${rasaResponse}\n`;
                }
              })
              .catch((error) => {
                console.log("Error:", error);
                addToConsole(`<span style="color: #7289DA;">JUICERO@MYSQL:$</span>  Failed to connect to Rasa server.\n`);
              });
          }
          
          
          
        }
      })
      .catch((error) => {
        console.log("Error:", error);
        addToConsole(`<span style="color: #7289DA;">JUICERO@MYSQL:$</span>  Failed to connect to Rasa server.\n`);
      });
    
    
  }
}

function addToConsole(text) {
  consoleOutput.innerHTML += text;
  consoleOutput.scrollTop = consoleOutput.scrollHeight;
}


  
 