import React, { ChangeEvent, useState } from 'react';
import {
    Grid,
    Select,
    Button,
    Container,
    TextField,
    Card,
    MenuItem,
} from '@material-ui/core';
import { Info, PermDeviceInformation } from '@material-ui/icons';

export default function DeviceInformation() {
    const [deviceInfo, setDeviceInfo]: [any, any] = useState(null);
    const [equipmentTypeList, setEquipmentTypeList]: [any, any] = useState(
        null
    );
    const [equipmentType, setEquipmentType] = useState('');
    const [deviceName, setDeviceName] = useState('');
    const [siteId, setSiteId] = useState('');

    const onDeviceNameChange = (event: any) => {
        setDeviceName(event.target.value);
    };

    const onSiteIdChange = (event: any) => {
        setSiteId(event.target.value);
    };

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

    getDeviceInfo();

    //TODO: Get equipment types from firestore.

    return (
        <Container className="w-11/12">
            <Grid
                container
                direction="column"
                alignItems="flex-start"
                spacing={2}
            >
                <Grid item className="text-2xl font-bold">
                    Logger Settings
                </Grid>
                <Grid item>
                    IP: {deviceInfo?.address ?? '<unknown>'}
                    <Info className="pl-1" />
                </Grid>

                <Grid item>
                    MAC: {deviceInfo?.mac ?? '<unknown>'}
                    <PermDeviceInformation className="pl-1" />
                </Grid>

                <Grid item>
                    <TextField
                        variant="outlined"
                        label="Device Name"
                        onChange={onDeviceNameChange}
                        value={deviceName}
                    />
                </Grid>

                <Grid item>
                    <TextField
                        variant="outlined"
                        label="Site ID (optional)"
                        onChange={onSiteIdChange}
                        value={siteId}
                    />
                </Grid>

                <Grid item>
                    <Button variant="outlined" onClick={handleSaveButton}>
                        Save
                    </Button>
                </Grid>
            </Grid>
        </Container>
    );
}
