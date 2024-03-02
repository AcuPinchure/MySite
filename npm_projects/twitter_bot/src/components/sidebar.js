import React from "react";
import './layout.css';
import { Icon, Menu, Divider, Form, Dropdown, Button } from "semantic-ui-react";
import BotLogo from "../assets/bot_logo.svg";
import { useLocation, useHistory } from "react-router-dom";
import { useSelector } from "react-redux";

import store from "../store";
import { setLeftActive, setRightActive } from "../store/layout_slice";

import PropTypes from 'prop-types';


function LeftSideBar(props) {
    return (
        <div className={`bot stats left sidebar ${props.isActive ? "active" : ""}`}>
            <SideBarTitle></SideBarTitle>
            <NaviMenu></NaviMenu>
        </div>
    )
}
LeftSideBar.propTypes = {
    isActive: PropTypes.bool.isRequired
}

function SideBarTitle() {
    return (
        <img src={BotLogo} alt="Bot Logo" className="bot stats site_title" onClick={() => { window.location = "/bot/" }}></img>
    )
}


function NaviMenu() {
    const path_name = useLocation().pathname;
    const history = useHistory();

    const show_admin_menu = useSelector(state => state.LayoutSlice.show_admin_menu);

    function handleItemClick(path) {
        history.push(path);
        store.dispatch(setLeftActive(false));
        store.dispatch(setRightActive(false));
    }

    return (
        <Menu secondary vertical inverted fluid size="large">
            <Menu.Item data-name="about" onClick={() => { window.location = "/bot/" }}>
                <Icon name="home"></Icon>
                About
            </Menu.Item>
            <Menu.Item active={path_name.startsWith("/bot/stats/")} onClick={() => handleItemClick("/bot/stats/")}>
                <Icon name="chart bar"></Icon>
                Statistics
            </Menu.Item>
            <Menu.Item active={path_name.startsWith("/bot/status/")} onClick={() => handleItemClick("/bot/status/")}>
                <Icon name="signal"></Icon>
                Service Status
            </Menu.Item>
            {show_admin_menu ?
                <>
                    <Menu.Item active={path_name.startsWith("/bot/config/")} onClick={() => handleItemClick("/bot/config/")}>
                        <Icon name="cogs"></Icon>
                        Service Config
                    </Menu.Item>
                    <Menu.Item active={path_name.startsWith("/bot/library/")} onClick={() => handleItemClick("/bot/library/")}>
                        <Icon name="images outline"></Icon>
                        Image Library
                    </Menu.Item>
                    <Menu.Item active={path_name.startsWith("/bot/logs/")} onClick={() => handleItemClick("/bot/logs/")}>
                        <Icon name="clock outline"></Icon>
                        Logs
                    </Menu.Item>
                    <Menu.Item onClick={() => { window.location = "/bot/logout/" }}>
                        <Icon name="log out"></Icon>
                        Logout
                    </Menu.Item>
                </>
                :
                null
            }

        </Menu>
    )
}


function RightSideBar(props) {

    return (
        <div className={`bot stats right sidebar ${props.isActive ? "active" : ""}`}>
            {props.children}
        </div>
    )
}
RightSideBar.propTypes = {
    isActive: PropTypes.bool.isRequired
}


function SideBarDimmer() {

    const layout_state = useSelector(state => state.LayoutSlice);

    function handleDimmerClick() {
        store.dispatch(setLeftActive(false));
        store.dispatch(setRightActive(false));
    }

    return (
        <>
            <div
                className={`bot stats left sidebar_overlay ${(layout_state.left_active && layout_state.view_width <= layout_state.responsive_width) ? "active" : ""}`}
                onClick={handleDimmerClick}
            ></div>
            <div
                className={`bot stats right sidebar_overlay ${layout_state.right_active ? "active" : ""}`}
                onClick={handleDimmerClick}
            ></div>
        </>
    )
}



export { LeftSideBar, RightSideBar, SideBarDimmer };