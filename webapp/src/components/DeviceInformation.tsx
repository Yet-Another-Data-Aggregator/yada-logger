import React, { useState } from 'react';
import { Button, Input } from 'reactstrap';
import { Info, PermDeviceInformation } from '@material-ui/icons';
import { useLocation, useParams } from 'react-router-dom';

export default function DeviceInformation() {
    const [deviceInfo, setDeviceInfo]: [any, any] = useState(null);
    const [deviceName, setDeviceName] = useState('');
    const [notes, setNotes] = useState('');
    const [siteId, setSiteId] = useState('');
    const location = useLocation();
    const searchParams = new URLSearchParams(location.search);

    const onDeviceNameChange = (event: any) => {
        setDeviceName(event.target.value);
    };

    const onNotesChange = (event: any) => {
        setNotes(event.target.value);
    };

    const onSiteIdChange = (event: any) => {
        setSiteId(event.target.value);
    };

    //Helper function to check if string is null or whitespace
    function isBlank(str: string) {
        return !str || /^\s*$/.test(str);
    }

    function getDeviceInfo() {
        if (!deviceInfo) {
            fetch('/devinfo')
                .then(async (response) => {
                    var responseJson = await response.json();
                    const ipv4info = responseJson[0];

                    console.log(ipv4info);
                    setDeviceInfo(ipv4info);
                })
                .catch((reason) => {
                    console.log('Something went wrong: ' + reason);
                });
        }
    }

    function saveDeviceInfo(devname: string, siteid: string) {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: devname,
                siteid: siteid,
                notes: notes,
            }),
        };

        console.log(
            'Sending device info message with ' + devname + ':' + siteid
        );

        fetch('/devinfo', requestOptions)
            .then(async (response) => {
                var responseJson = await response.json();

                console.log(responseJson);
            })
            .catch((reason) => {
                console.log('Something went wrong: ' + reason);
            });
    }

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

    const handleSaveButton = () => {
        if (!isBlank(deviceName)) {
            console.log('Saving device name: ' + deviceName);
            console.log('Saving site id: ' + siteId);
            saveDeviceInfo(deviceName, siteId);

            const ssid = searchParams.get('ssid');
            const passkey = searchParams.get('passkey');

            if (ssid != null && passkey != null && !isBlank(ssid)) {
                attemptConnection(ssid, passkey);
            } else {
                alert(
                    'SSID or network passkey not specified.  Return to network selection and try again.'
                );
            }
        } else {
            alert('Device name cannot be empty.');
        }
    };

    //Get the device info once when the component is loaded.
    getDeviceInfo();

    console.log(searchParams.get('ssid'));
    console.log(searchParams.get('passkey'));

    return (
        <div className="deviceInformation">
            <h1>Logger Settings</h1>

            <div className="infoBox">
                <div className="infoLine">
                    IP: {deviceInfo?.address ?? '<unknown>'}
                    <Info className="icon" />
                </div>

                <div className="infoLine">
                    MAC: {deviceInfo?.mac ?? '<unknown>'}
                    <PermDeviceInformation className="icon" />
                </div>
            </div>

            <div>
                <div className="label">Device Name:</div>
                <Input
                    className="input"
                    onChange={onDeviceNameChange}
                    value={deviceName}
                />

                <div className="label">Site ID:</div>
                <Input
                    className="input"
                    onChange={onSiteIdChange}
                    value={siteId}
                />

                <div className="label">Notes:</div>
                <Input
                    type="textarea"
                    className="largeInput"
                    onChange={onNotesChange}
                    value={notes}
                />

                <Button
                    className="button"
                    variant="outlined"
                    onClick={handleSaveButton}
                >
                    Save &amp; Attempt Connect
                </Button>
            </div>
        </div>
    );
}
