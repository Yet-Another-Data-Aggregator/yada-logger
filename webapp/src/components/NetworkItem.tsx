import React, { useState } from 'react';
import { Button, ListItemText, TextField, Card } from '@material-ui/core';
import { Wifi, Lock, LockOpen } from '@material-ui/icons';

export default function NetworkItem(props: any) {
    const [securityKey, setSecurityKey]: [string, any] = useState('');
    const onSecurityKeyChange = (event: any) => {
        console.log(event.target.value);
        setSecurityKey(event.target.value);
    };

    function attemptConnection(ssid: string, passkey: string) {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ wifi_ssid: ssid, wifi_passcode: passkey }),
        };

        console.log('sending connection message with ' + ssid + ':' + passkey);

        fetch('/enable_wifi', requestOptions)
            .then(async (response) => {
                var responseJson = await response.json();

                console.log(responseJson);
            })
            .catch((reason) => {
                console.log('Something went wrong: ' + reason);
            });
    }

    const encIcon = props.network.encrypted ? (
        <Lock className="mr-5" />
    ) : (
        <LockOpen className="mr-5" />
    );

    const connectionPrompt = props.selected ? (
        <div className="my-5 flex space-x-4 justify-center">
            <TextField
                variant="outlined"
                size="small"
                label="Security Key"
                onChange={onSecurityKeyChange}
            />
            <Button
                variant="outlined"
                className="ml-5"
                onClick={() => {
                    attemptConnection(props.network.ssid, securityKey);
                }}
            >
                Connect
            </Button>
        </div>
    ) : null;

    return (
        <Card className="border" onClick={props.onClick}>
            <div className="flex">
                <Wifi className="ml-5" />

                <ListItemText
                    className="flex justify-center"
                    primary={props.network.ssid}
                />

                {encIcon}
            </div>

            {connectionPrompt}
        </Card>
    );
}
