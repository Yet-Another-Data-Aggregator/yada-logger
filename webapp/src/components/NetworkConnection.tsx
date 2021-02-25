import React, { useState } from 'react';
import { Button } from 'reactstrap';
import NetworkItem from './NetworkItem';

export default function NetworkConnection() {
    const [availableNetworks, setNetworks]: [Array<any>, any] = useState([]);
    const [selectedNetworkIndex, setSelectedNetworkIndex]: [
        number,
        any
    ] = useState(-1);

    const refreshNetworks = () => {
        setSelectedNetworkIndex(-1);
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
            <h1>Available Networks</h1>

            {availableNetworks && availableNetworks.length > 0 ? (
                <ul className="networkList">
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
                </ul>
            ) : (
                <div className="networkItem">Didn't find any networks.</div>
            )}

            <Button className="button" onClick={refreshNetworks}>
                Refresh
            </Button>
        </div>
    );
}
