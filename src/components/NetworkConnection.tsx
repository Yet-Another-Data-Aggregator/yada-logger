import React from "react";
import {List, ListItem, ListItemText, Icon, ListItemIcon} from "@material-ui/core";
import {Wifi} from "@material-ui/icons";

export default function NetworkConnection() {

    return (
        <List className="w-1/2 border">
            <ListItem className="border">
                <ListItemIcon>
                    <Wifi/>
                </ListItemIcon>
                <ListItemText className="flex justify-center" primary="This is where"/>
            </ListItem>
            <ListItemText primary="my wifi networks"/>
            <ListItemText primary="would be displayed"/>
            <ListItemText primary="if I could find any!"/>
        </List>
    );
}