import React, { useState } from 'react';
import { List, ListItem, ListItemText, Icon, ListItemIcon, Button, Container } from '@material-ui/core';
import { Wifi, Lock, LockOpen } from '@material-ui/icons';

export default function NetworkConnection() {
    const [availableNetworks, setNetworks]: [Array<any>, any] = useState([]);

    const sendTestGet = () => {
        fetch("/ping").then(async (response) => {
            var responseJson = await response.json();

            alert(responseJson.data);
            console.log(responseJson.data);
        }).catch((reason) => {
            console.log("Something went wrong: " + reason);
        })
    };

    const refreshNetworks = () => {
        getWifiNetworks();
    };

    const connectToTestNetwork = () => {
        attemptConnection("DATA_ERROR_24G", "SmileyApple205");
    };

    function getWifiNetworks() {
        fetch("/rescan_wifi").then(async (response) => {
            var responseJson = await response.json();

            setNetworks(responseJson.scan_results);

            console.log("Success Getting Wifi Networks");
            console.log(responseJson);
        }).catch((reason) => {
            console.log("ERROR:" + reason);
        });
    }

    function attemptConnection(ssid: string, passkey: string) {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ wifi_ssid: ssid, wifi_passcode: passkey})
        };

        fetch("/enable_wifi", requestOptions).then(async (response) => {
            var responseJson = await response.json();

            console.log(responseJson);
        }).catch((reason) => {
            console.log("Something went wrong: " + reason);
        })
    }

    function sendTestPost(message: string) {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ data: message })
        };

        fetch("/testpost", requestOptions).then(async (response) => {
            var responseJson = await response.json();

            alert(responseJson.data);
            console.log(responseJson.data);
        }).catch((reason) => {
            console.log("Something went wrong: " + reason);
        })
    }

    const NetworkList = (availableNetworks: Array<any>) => {
        console.log(availableNetworks);

        if (availableNetworks && availableNetworks.length > 0) {
            return (
                <div>
                    {availableNetworks.map((network, index) => {
                        const encIcon = (network.encrypted) ? (<Lock/>) : (<LockOpen/>);

                        return (<ListItem key={index} className="border">
                            <ListItemIcon>
                                <Wifi />
                            </ListItemIcon>
                            <ListItemText className="flex justify-center" primary={network.ssid} />
                            <ListItemIcon>
                                {encIcon}
                            </ListItemIcon>
                        </ListItem>)
                    })}
                </div>
            )
        }
        else {
            return (
                <div>
                    <ListItem className="border">
                        <ListItemText className="flex justify-center" primary="Didn't find any networks." />
                    </ListItem>
                </div>
            )
        }
    }

    return (
        <Container>
            <List className="w-1/2 border">
                {NetworkList(availableNetworks)}
            </List>

            <Button onClick={sendTestGet}>Ping</Button>
            <Button onClick={refreshNetworks}>Refresh</Button>
            <Button onClick={connectToTestNetwork}>Try To Connect To Data Error</Button>
        </Container>
    );
}