import React from "react";
import { List, ListItem, ListItemText, Icon, ListItemIcon, Button, Container } from "@material-ui/core";
import { Wifi } from "@material-ui/icons";

export default function NetworkConnection() {

    const sendTestGet = () => {
        fetch("/ping").then(async (response) => {
            var responseJson = await response.json();

            alert(responseJson.data);
            console.log(responseJson.data);
        }).catch((reason) => {
            console.log("Something went wrong: " + reason);
        })
    };

    const sayHiToServer = () => {
        sendTestPost("Hey server!");
    };

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

    return (
        <Container>
            <List className="w-1/2 border">
                <ListItem className="border">
                    <ListItemIcon>
                        <Wifi />
                    </ListItemIcon>
                    <ListItemText className="flex justify-center" primary="This is where" />
                </ListItem>
                <ListItemText primary="my wifi networks" />
                <ListItemText primary="would be displayed" />
                <ListItemText primary="if I could find any!" />
            </List>

            <Button onClick={sendTestGet}>Ping</Button>
            <Button onClick={sayHiToServer}>Say Hello To The Server</Button>
        </Container>
    );
}