const express = require('express');
const path = require('path');
const ip = require('ip');
const os = require('os');
const fs = require('fs');
const ini = require('ini');
const wifi_manager = require('./wifi_manager')();
const iwlist = require('./iwlist');
var bodyParser = require('body-parser'); //needed to get data from body of POST requests
const app = express();

const ap_ssid = 'RASPI-AP';
const configPath = './src/config.ini';

app.use(bodyParser.json()); // support json encoded bodies

//Set and use the path to serve the production build of the webapp
const webappBuildPath = path.join(__dirname, 'webapp/build');
console.log('Using build path of:' + webappBuildPath);
app.use(express.static(webappBuildPath));

// Helper function to log errors and send a generic status "SUCCESS"
// message to the caller
function log_error_send_success_with(success_obj, error, response) {
    if (error) {
        console.log('ERROR: ' + error);
        response.send({ status: 'ERROR', error: error });
    } else {
        success_obj = success_obj || {};
        success_obj['status'] = 'SUCCESS';
        response.send(success_obj);
    }
    response.end();
}

function checkWifiEnabledFallbackToAP() {
    //Check if we are currently connected to a wifi network
    wifi_manager.is_wifi_enabled(function (error, result_ip) {
        if (result_ip) {
            console.log('\nWifi is enabled. IP:' + result_ip);
            
        } else {
            console.log(
                '\nWifi is not enabled, Enabling AP for self-configure'
            );

            //enable AP so we can configure wifi
            wifi_manager.enable_ap_mode(ap_ssid, function (error) {
                if (error) {
                    console.log('... AP Enable ERROR: ' + error);
                } else {
                    console.log('... AP Enable Success!');
                }
            });
        }
    });

    //update ip and mac in config
    const wifiInfo = os.networkInterfaces()['wlan0'];

            console.log('Saving new IP (' + wifiInfo.address  + ') and MAC (' + wifiInfo.mac + ') to config');

            var config = ini.parse(fs.readFileSync(configPath, 'utf-8'));

            config.config.ip = wifiInfo.address;
            config.config.mac = wifiInfo.mac;

            fs.writeFileSync(configPath, ini.stringify(config));

            console.log('wrote changes to config.ini');
}

/*******ROUTE HANDLERS****************/

//Serve the webapp on the default route
app.get('/', (req, res) => {
    res.sendFile(path.join(webappBuildPath, 'index.html'));
});

//route handler to rescan wifi
app.get('/rescan_wifi', function (request, response) {
    console.log('Server got /rescan_wifi');
    iwlist(function (error, result) {
        log_error_send_success_with(result[0], error, response);
    });
});

//route handler for GET device info
app.get('/devinfo', function (request, response) {
    const wifiInfo = os.networkInterfaces()['wlan0'];

    console.log('Client GET /devinfo');

    if (wifiInfo) {
        response.send(wifiInfo);
    } else {
        console.error(
            "Can't retrieve device info, network interface for wlan0 not present."
        );
    }
});

//POST route for device information, writes changes to src/config.ini
app.post('/devinfo', function (request, response) {
    console.log('Client POST /devinfo');

    var dev_info = {
        name: request.body.name,
        siteid: request.body.siteid,
        notes: request.body.notes,
        ip: request.body.ip,
        mac: request.body.mac
    };

    var config = ini.parse(fs.readFileSync(configPath, 'utf-8'));

    config.config.devname = dev_info.name;
    config.config.siteid = dev_info.siteid;
    config.config.notes = dev_info.notes;
    config.config.ip = dev_info.ip;
    config.config.mac = dev_info.mac;

    fs.writeFileSync(configPath, ini.stringify(config));

    console.log('wrote changes to config.ini');
});

/************************************************/
checkWifiEnabledFallbackToAP();

// console.log that your server is up and running
var server = app.listen(80, function () {
    var host = ip.address();
    var port = server.address().port;
    console.log('running at http://' + host + ':' + port);
});

//route handler for connecting to wifi
app.post('/enable_wifi', function (request, response) {
    var conn_info = {
        wifi_ssid: request.body.wifi_ssid,
        wifi_passcode: request.body.wifi_passcode,
    };

    // TODO: If wifi did not come up correctly, it should fail
    // currently we ignore ifup failures.
    wifi_manager.enable_wifi_mode(conn_info, function (error) {
        if (error) {
            console.log('Enable Wifi ERROR: ' + error);
            console.log('Attempt to re-enable AP mode');
            wifi_manager.enable_ap_mode(ap_ssid, function (error) {
                console.log('... AP mode reset');
            });
        }

        //restart the web server to give the pi a chance to connect to wifi
        console.log('Wifi Enabled! - Restarting server');
        server.close();

        //This causes the wifi to not connect for some reason
        console.log(
            'waiting 10 seconds then checking if we successfully connected'
        );
        setTimeout(() => {
            checkWifiEnabledFallbackToAP();
        }, 10000);

        server = app.listen(80, function () {
            var host = ip.address();
            var port = server.address().port;
            console.log('restarted server at http://' + host + ':' + port);
        });
    });
});
