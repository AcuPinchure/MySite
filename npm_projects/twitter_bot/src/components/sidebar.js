import React, { useEffect, useState } from "react";
import './layout.css';
import { Icon, Menu, Divider, Form, Dropdown, Button } from "semantic-ui-react";
import BotLogo from "../assets/bot_logo.svg";
import { useLocation, useHistory } from "react-router-dom";


function LeftSideBar(props) {
    const history = useHistory();
    return (
        <div className={`bot stats left sidebar ${props.isActive ? "active" : ""}`}>
            <SideBarTitle onClick={() => history.push("/bot/")}></SideBarTitle>
            <NaviMenu></NaviMenu>
        </div>
    )
}

function SideBarTitle(props) {
    const history = useHistory();
    return (
        <img src={BotLogo} alt="Bot Logo" className="bot stats site_title" onClick={() => history.push("/")}></img>
    )
}


function NaviMenu(props) {
    const location = useLocation();
    const history = useHistory();

    return (
        <Menu secondary vertical inverted fluid size="large">
            <Menu.Item data-name="about" onClick={() => history.push("/bot/")}>
                <Icon name="home"></Icon>
                About
            </Menu.Item>
            <Menu.Item active={location.pathname.startsWith("/bot/stats")} onClick={() => history.push("/bot/stats")}>
                <Icon name="chart bar"></Icon>
                Statistics
            </Menu.Item>
            <Menu.Item active={location.pathname.startsWith("/bot/config")} onClick={() => history.push("/bot/config")}>
                <Icon name="cogs"></Icon>
                Service Config
            </Menu.Item>
            <Menu.Item active={location.pathname.startsWith("/bot/library")} onClick={() => history.push("/bot/library")}>
                <Icon name="images outline"></Icon>
                Image Library
            </Menu.Item>
            <Menu.Item active={location.pathname.startsWith("/bot/logs")} onClick={() => history.push("/bot/logs")}>
                <Icon name="clock outline"></Icon>
                Logs
            </Menu.Item>
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