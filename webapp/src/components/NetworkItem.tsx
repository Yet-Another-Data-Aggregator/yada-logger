import React, { useState } from 'react';
import { Button, Input } from 'reactstrap';
import { Wifi, Lock, LockOpen } from '@material-ui/icons';
import { Link } from 'react-router-dom';

export default function NetworkItem(props: any) {
    const [securityKey, setSecurityKey]: [string, any] = useState('');

    const onSecurityKeyChange = (event: any) => {
        setSecurityKey(event.target.value);
    };

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
                to={`/device-information?ssid=${props.network.ssid}&passkey=${securityKey}`}
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
