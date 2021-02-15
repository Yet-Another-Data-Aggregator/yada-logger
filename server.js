const express = require('express');
const path = require('path');
const ip = require('ip');
const wifi_manager = require('./wifi_manager')();
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

//route handler for connecting to wifi
app.post("/api/enable_wifi", function(request, response) {
  var conn_info = {
      wifi_ssid:      request.body.wifi_ssid,
      wifi_passcode:  request.body.wifi_passcode,
  };

  // TODO: If wifi did not come up correctly, it should fail
  // currently we ignore ifup failures.
  wifi_manager.enable_wifi_mode(conn_info, function(error) {
      if (error) {
          console.log("Enable Wifi ERROR: " + error);
          console.log("Attempt to re-enable AP mode");
          wifi_manager.enable_ap_mode(config.access_point.ssid, function(error) {
              console.log("... AP mode reset");
          });
          response.redirect("/");
      }
      // Success! - exit
      console.log("Wifi Enabled! - Exiting");
      process.exit(0);
  });
});



//Check if we are currently connected to a wifi network
wifi_manager.is_wifi_enabled(function(error, result_ip) {		
  if (result_ip) {
    console.log("\nWifi is enabled.");
} else {
    console.log("\nWifi is not enabled, Enabling AP for self-configure");

    //enable AP so we can configure wifi
    wifi_manager.enable_ap_mode(config.access_point.ssid, function(error) {
      if(error) {
          console.log("... AP Enable ERROR: " + error);
      } else {
          console.log("... AP Enable Success!");
      }
  });
}
});

// console.log that your server is up and running
var server = app.listen(5000, function () {
    var host = ip.address();
    var port = server.address().port;
    console.log('running at http://' + host + ':' + port);
});
