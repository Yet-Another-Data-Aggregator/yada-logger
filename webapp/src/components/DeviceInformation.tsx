import React, { ChangeEvent, useState } from "react";
import {
    Grid,
    Select,
    Button,
    Container,
    TextField,
    Card,
    MenuItem,
  } from "@material-ui/core";
import { Info, PermDeviceInformation } from "@material-ui/icons";

export default function DeviceInformation() {

    const [deviceInfo, setDeviceInfo] = useState(null);
    const [equipmentType, setEquipmentType] = useState('');

    const handleEquipmentChange = (e: ChangeEvent<{value: unknown}>) => {
        setEquipmentType(e.target.value as string);
    }

    function getDeviceInfo(){    
        if(!deviceInfo) {
    fetch("/devinfo")
      .then(async (response) => {
        var responseJson = await response.json();

        console.log(responseJson);
        setDeviceInfo(responseJson);
      })
      .catch((reason) => {
        console.log("Something went wrong: " + reason);
      });
    }
    }

    getDeviceInfo();

    return (
        <Container className="w-11/12">
        <Grid container direction="column" alignItems='flex-start' spacing={2}>
            <Grid item>Logger Settings</Grid>
            <Grid item>IP: 0.0.0.0 
                <Info className="pl-1"/>
            </Grid>

            <Grid item>MAC: 00:00:00:00:00:00
                <PermDeviceInformation className="pl-1"/>
            </Grid>

            <Grid item>
            <TextField variant='outlined' label="Device Name"/>
            </Grid>

            <Grid item>
                <TextField variant='outlined' label="Site ID (optional)"/>
            </Grid>

            <Grid item>
            <Select onChange={handleEquipmentChange} value={equipmentType}>
                <MenuItem value={'A'}>Equipment A</MenuItem>
                <MenuItem value={'B'}>Equipment B</MenuItem>
                <MenuItem value={'C'}>Equipment C</MenuItem>
            </Select>
            </Grid>

        </Grid>
        </Container>
    );
}