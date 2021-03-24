import React, { useState } from 'react';
import { Button, Input } from 'reactstrap';
import { Wifi, Lock, LockOpen } from '@material-ui/icons';
import { Link } from 'react-router-dom';

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
        <Lock className="rightIcon" />
    ) : (
        <LockOpen className="rightIcon" />
    );

    const connectionPrompt = props.selected ? (
        <div className="inline">
            <Input
                variant="outlined"
                className="input"
                onChange={onSecurityKeyChange}
            />
            <Link
                className="button"
                to={
                    '/device-information/' +
                    props.network.ssid +
                    '/' +
                    securityKey
                }
            >
                Continue
            </Link>
        </div>
    ) : null;

    return (
        <div className="networkItem floatingCard" onClick={props.onClick}>
            <div className="inline">
                <Wifi className="leftIcon" />

                {props.network.ssid}

                {encIcon}
            </div>

            {connectionPrompt}
        </div>
    );
}
