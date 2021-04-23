import React, { useState } from 'react';
import { Button, Input } from 'reactstrap';
import { Wifi } from '@material-ui/icons';
import { Link, useHistory } from 'react-router-dom';

export default function HiddenNetworkItem() {
    const [securityKey, setSecurityKey]: [string, any] = useState('');
    const [ssid, setSSID]: [string, any] = useState('');
    const history = useHistory();

    const [expanded, setExpanded]: [boolean, any] = useState(false);

    //Helper function to check if string is null or whitespace
    function isBlank(str: string) {
        return !str || /^\s*$/.test(str);
    }

    const onSecurityKeyChange = (event: any) => {
        setSecurityKey(event.target.value);
    };

    const onSSIDChange = (event: any) => {
        setSSID(event.target.value);
    };

    const expandButton = (
        <Button
            className="expandButton"
            onClick={() => {
                setExpanded(!expanded);
            }}
        >
            Hidden SSID
        </Button>
    );

    const connectionPrompt = expanded ? (
        <div className="hiddenNetworkItem">
            {expandButton}

            <div className="inline">
                <Input
                    variant="outlined"
                    className="input"
                    placeholder="Hidden Network SSID"
                    onChange={onSSIDChange}
                />
            </div>

            <div className="inline">
                <Input
                    variant="outlined"
                    className="input"
                    placeholder="Hidden Network Password"
                    onChange={onSecurityKeyChange}
                />
                <Button
                    className="button"
                    onClick={() => {
                        if (!isBlank(ssid)) {
                            history.push(
                                `/device-information?ssid=${ssid}&passkey=${securityKey}`
                            );
                        } else {
                            alert('SSID required before proceeding.');
                        }
                    }}
                >
                    Continue
                </Button>
            </div>

            <div className="inline"></div>
        </div>
    ) : (
        <div className="hiddenNetworkItem">{expandButton}</div>
    );

    return <div>{connectionPrompt}</div>;
}
