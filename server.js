const express = require('express');
const path = require('path');
const ip = require('ip');
var bodyParser = require('body-parser'); //needed to get data from body of POST requests
const app = express();

app.use(bodyParser.json()); // support json encoded bodies

//Set and use the path to serve the production build of the webapp
const webappBuildPath = path.join(__dirname, "webapp/build");
console.log("Using build path of:" + webappBuildPath);
app.use(express.static(webappBuildPath));

//Serve the webapp on the default route
app.get('/', (req, res) => {
    res.sendFile(path.join(webappBuildPath, 'index.html'));
  });
  

//if they request ping, pong back
app.get('/ping', (req, res) => {
  res.send({data : "pong"});
});

app.post('/testpost', (req, res) => {
    var msg = req.body.data;
    console.log("Client sent me: " + msg);
});

// console.log that your server is up and running
var server = app.listen(5000, function () {
    var host = ip.address();
    var port = server.address().port;
    console.log('running at http://' + host + ':' + port);
});