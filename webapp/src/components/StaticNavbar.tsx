/**
 * Side navbar component
 *
 * creates navbar component that can be developed further to implement both levels of the dynamic side navbar
 */

//import { fireAuthSignOut } from "FireConfig";
import React, { ReactElement } from 'react';
import { Link, Route, useLocation } from 'react-router-dom';

/**
 * autoCollapse: if true, the navbar compresses itself and expands when hovered. Ideal if icons are used
 * roundRightCornser: if true, all 4 corners of the navbar are rounded. if false on the left two are. This will need to be expanded upon later if this component is used to create multiple levels of navbars
 * currentPrivilege: privilege of the current user
 * active route: the active route
 */
interface navbarProps {
    autoCollapse: Boolean;
    roundRightCorners: Boolean;
    //currentPrivilege: string;
    children: ReactElement | ReactElement[];
}

/**
 * name: text to display on the nav item
 * route: the route switched to upon clicking the nav item
 * currentRoute: the current route the user is on (used to highlight the current route)
 * requiredPermissions: permissions required to navigate to this route
 * currentPermission: permission level of the current user
 */
interface StaticNavItemProp {
    label: string;
    route: string;
    icon: any;
    children: ReactElement;
}

/**
 * Navigation item
 * @param props
 */
export function StaticNavItem(props: StaticNavItemProp) {
    let currentRoute = useLocation();

    /**
     * returns empty div if the permissions are not met
     */
    return (
        <Link to={props.route}>
            <div
                className={`navItem ${
                    currentRoute.pathname.startsWith(props.route)
                        ? 'active'
                        : 'inactive'
                }`}
            >
                <div className="navIcon">{props.icon}</div>
                <div className="navTitle">{props.label}</div>
            </div>
        </Link>
    );
}

/**
 * Side navbar
 * @param props
 */
export default function StaticNavbar(props: navbarProps) {
    function createRoute(child: ReactElement) {
        return <Route path={child.props.route}>{child.props.children}</Route>;
    }

    return (
        <>
            <div className="staticNavbar">
                <div className={`navLinks`}>{props.children}</div>
            </div>
            <div className="routes">
                {React.Children.map(props.children, createRoute)}
            </div>
        </>
    );
}
