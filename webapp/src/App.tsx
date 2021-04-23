import React from 'react';
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Redirect,
} from 'react-router-dom';
import { Animated } from 'react-animated-css';
import './App.scss';
import NetworkConnection from './components/NetworkConnection';
import DeviceInformation from './components/DeviceInformation';
import StaticNavbar, { StaticNavItem } from './components/StaticNavbar';
import { Info, Wifi } from '@material-ui/icons';
import 'typeface-lato';

function App() {
    return (
        <Router>
            {/* A <Switch> looks through its children <Route>s and
            renders the first one that matches the current URL. */}
            <Switch>
                <Route path="/">
                    <Redirect to="/network-connection/" />
                    <Animated
                        animationIn="fadeIn"
                        animationOut="fadeOut"
                        isVisible={true}
                    >
                        <div className="app">
                            <StaticNavbar
                                autoCollapse={true}
                                roundRightCorners={true}
                            >
                                <StaticNavItem
                                    label={'Network Connection'}
                                    route={'/network-connection'}
                                    icon={<Wifi />}
                                >
                                    <NetworkConnection />
                                </StaticNavItem>
                                <StaticNavItem
                                    label={'Device Information'}
                                    route={'/device-information/'}
                                    icon={<Info />}
                                >
                                    <DeviceInformation />
                                </StaticNavItem>
                            </StaticNavbar>
                        </div>
                    </Animated>
                </Route>
            </Switch>
        </Router>
    );
}

export default App;
