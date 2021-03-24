import React, { useState } from 'react';
import { Button, Input } from 'reactstrap';
import { Info, PermDeviceInformation } from '@material-ui/icons';
import { useParams } from 'react-router-dom';

export default function DeviceInformation() {
    const [deviceInfo, setDeviceInfo]: [any, any] = useState(null);
    const [deviceName, setDeviceName] = useState('');
    const [siteId, setSiteId] = useState('');
    const { ssid, passkey }: any = useParams();

    const onDeviceNameChange = (event: any) => {
        setDeviceName(event.target.value);
    };

    const onSiteIdChange = (event: any) => {
        setSiteId(event.target.value);
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
            body: JSON.stringify({ name: devname, siteid: siteid }),
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

    const handleSaveButton = () => {
        console.log('Saving device name: ' + deviceName);
        console.log('Saving site id: ' + siteId);
        saveDeviceInfo(deviceName, siteId);
    };

    //Get the device info once when the component is loaded.
    getDeviceInfo();

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

                <Button
                    className="button"
                    variant="outlined"
                    onClick={handleSaveButton}
                >
                    Save
                </Button>
            </div>
        </div>
    );
}
