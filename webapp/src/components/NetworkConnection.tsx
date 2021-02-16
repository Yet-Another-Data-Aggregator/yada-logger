import React, { useState } from 'react';
import { List, ListItem, ListItemText, Icon, ListItemIcon, Button, Container } from '@material-ui/core';
import { Wifi } from '@material-ui/icons';

export default function NetworkConnection() {
    const [availableNetworks, setNetworks]: [Array<{ ssid: string }>, any] = useState([]);

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

    function getWifiNetworks() {
        fetch("/rescan_wifi").then(async (response) => {
            var responseJson = await response.json();

            setNetworks(responseJson.scanResults);

            console.log("Success Getting Wifi Networks");
            console.log(responseJson);
            console.log(availableNetworks);
        }).catch((reason) => {
            console.log("ERROR:" + reason);
        });
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

    const NetworkList = (availableNetworks: Array<{ ssid: string }>) => {
        console.log(availableNetworks);

        if (availableNetworks && availableNetworks.length > 0) {
            return (
                <div>
                    {availableNetworks.map((network) => {
                        <ListItem className="border">
                            <ListItemIcon>
                                <Wifi />
                            </ListItemIcon>
                            <ListItemText className="flex justify-center" primary={network.ssid} />
                        </ListItem>
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
        </Container>
    );
}