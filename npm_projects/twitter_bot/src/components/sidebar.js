import React from "react";
import './layout.css';
import { Icon, Menu, Divider, Form, Dropdown, Button } from "semantic-ui-react";
import BotLogo from "../assets/bot_logo.svg";
import { useLocation, useHistory } from "react-router-dom";
import { useSelector } from "react-redux";

import store from "../store";
import { setLeftActive } from "../store/layout_slice";


function LeftSideBar(props) {
    return (
        <div className={`bot stats left sidebar ${props.isActive ? "active" : ""}`}>
            <SideBarTitle></SideBarTitle>
            <NaviMenu></NaviMenu>
        </div>
    )
}

function SideBarTitle() {
    return (
        <img src={BotLogo} alt="Bot Logo" className="bot stats site_title" onClick={() => { window.location = "/bot/" }}></img>
    )
}


function NaviMenu() {
    const location = useLocation();
    const history = useHistory();

    const showAdminMenu = useSelector(state => state.LayoutSlice.showAdminMenu);

    function handleItemClick(path) {
        history.push(path);
        store.dispatch(setLeftActive(false));
    }

    return (
        <Menu secondary vertical inverted fluid size="large">
            <Menu.Item data-name="about" onClick={() => { window.location = "/bot/" }}>
                <Icon name="home"></Icon>
                About
            </Menu.Item>
            <Menu.Item active={location.pathname.startsWith("/bot/stats/")} onClick={() => handleItemClick("/bot/stats/")}>
                <Icon name="chart bar"></Icon>
                Statistics
            </Menu.Item>
            <Menu.Item active={location.pathname.startsWith("/bot/status/")} onClick={() => handleItemClick("/bot/status/")}>
                <Icon name="signal"></Icon>
                Service Status
            </Menu.Item>
            {showAdminMenu ?
                <>
                    <Menu.Item active={location.pathname.startsWith("/bot/config/")} onClick={() => handleItemClick("/bot/config/")}>
                        <Icon name="cogs"></Icon>
                        Service Config
                    </Menu.Item>
                    <Menu.Item active={location.pathname.startsWith("/bot/library/")} onClick={() => handleItemClick("/bot/library/")}>
                        <Icon name="images outline"></Icon>
                        Image Library
                    </Menu.Item>
                    <Menu.Item active={location.pathname.startsWith("/bot/logs/")} onClick={() => handleItemClick("/bot/logs/")}>
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
            <div className="bot stats right sidebar_close" onClick={() => props.setSideActive('right', false)}>
                <Icon name="angle right" size="large"></Icon>
            </div>
            <Divider className="bot stats sidebar_close"></Divider>
            {props.children}
        </div>
    )
}



export { LeftSideBar, RightSideBar };