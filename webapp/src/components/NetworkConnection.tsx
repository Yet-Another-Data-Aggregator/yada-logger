import React, { useState } from 'react';
import { List, ListItem, ListItemText, Button } from '@material-ui/core';
import NetworkItem from './NetworkItem';

export default function NetworkConnection() {
    const [availableNetworks, setNetworks]: [Array<any>, any] = useState([]);
    const [selectedNetworkIndex, setSelectedNetworkIndex]: [
        number,
        any
    ] = useState(-1);

    const refreshNetworks = () => {
        getWifiNetworks();
    };

    function getWifiNetworks() {
        fetch('/rescan_wifi')
            .then(async (response) => {
                var responseJson = await response.json();

                setNetworks(responseJson.scan_results);

                console.log('Success Getting Wifi Networks');
                console.log(responseJson);
            })
            .catch((reason) => {
                console.log('ERROR:' + reason);
            });
    }

    return (
        <div className="networkConnection">
            <List className="networkList">
                {availableNetworks && availableNetworks.length > 0 ? (
                    <div>
                        {availableNetworks.map((network, index) => {
                            return (
                                <NetworkItem
                                    key={index}
                                    network={network}
                                    selected={index === selectedNetworkIndex}
                                    onClick={() => {
                                        setSelectedNetworkIndex(index);
                                    }}
                                />
                            );
                        })}
                    </div>
                ) : (
                    <div className="floatingCard">
                        <ListItem className="border">
                            <ListItemText
                                className="floatingCard"
                                primary="Didn't find any networks."
                            />
                        </ListItem>
                    </div>
                )}
            </List>

            <Button onClick={refreshNetworks}>Refresh</Button>
        </div>
    );
}
