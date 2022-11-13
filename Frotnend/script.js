var SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
const synth = window.speechSynthesis;
const recognition = new SpeechRecognition();
const icon = document.querySelector('i.fa.fa-microphone');

function searchFromVoice() {
  recognition.start();
  recognition.onresult = (event) => {
    const speechToText = event.results[0][0].transcript;
    console.log(speechToText);
    document.getElementById("searchbar").value = speechToText;
    search();
  }
}

function search() {
    var term = document.getElementById("searchbar").value;
    var apigClient = apigClientFactory.newClient({ apiKey: "e8AQzs26uc6jZVmMHCiTn6RAKe5EtQ84483xGWcC" });
    var body = { };
    var params = {q : term};
    var additionalParams = {headers: {
    'Content-Type':"application/json"
    }};

    apigClient.searchGet(params, body , additionalParams).then(function(res){
        console.log("success");
        console.log(res);
        console.log(res.data);
        console.log(res.data.text.length);
        console.log(res.data.text);
        show(res)
      })
      }

function show(res) {
    var feat = document.getElementById("images");

    if(typeof(feat) != 'undefined' && feat != null){
      while (feat.firstChild) {
        feat.removeChild(feat.firstChild);
      }}
    
    if (res.data.text.length == 0) {
        var cont = document.createTextNode("No image to display");
        feat.appendChild(cont);
      }
      else {
        results=res.data.text
        for (var i = 0; i < results.length; i++) {
          var news = new Image();
          news.src = results[i]
          feat.appendChild(news);
        }
      }
    }

const file = document.getElementById("file");

function upload() {
    file.click();
}

function prev(input){
    var read = new FileReader();
    nam = input.files[0].name;
    ext = nam.split(".").pop();
    nam = nam.replace(/\.[^/.]+$/, "");
    nam = nam + "." + ext;
    console.log(nam);

    var myHeaders = new Headers();
  myHeaders.append("x-api-key", "e8AQzs26uc6jZVmMHCiTn6RAKe5EtQ84483xGWcC");
  myHeaders.append("Content-Type", "image/jpeg");

var file = input.files[0];

var requestOptions = {
  method: 'PUT',
  headers: myHeaders,
  body: file,
  redirect: 'follow'
};

fetch("https://5hq5axcu1i.execute-api.us-east-1.amazonaws.com/dev/b2a2/"+nam, requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));
}
