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

    const handleEquipmentChange = (e: ChangeEvent<{ value: unknown }>) => {
        setEquipmentType(e.target.value as string);
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
                    <TextField variant="outlined" label="Device Name" />
                </Grid>

                <Grid item>
                    <TextField variant="outlined" label="Site ID (optional)" />
                </Grid>

                <Grid item>
                    <Button variant="outlined">Save</Button>
                </Grid>
            </Grid>
        </Container>
    );
}
