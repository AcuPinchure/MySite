import React, {useEffect, useState} from "react";
import './layout.css';
import { Icon, Menu, Divider, Form, Dropdown, Button } from "semantic-ui-react";
import BotLogo from "../assets/bot_logo.svg";


function LeftSideBar(props) {

    // useEffect(() => {
    //     if (props.isActive) {
    //         window.addEventListener("click", handleClickOutside);
    //     }
    //     return () => {
    //         window.removeEventListener("click", handleClickOutside);
    //     }
    // }, [props.isActive]);

    // function handleClickOutside(e) {
    //     if (!e.target.classList.contains("bot", "stats", "left", "sidebar")) {
    //         props.setSideActive('left', false);
    //     }
    // }

    return (
        <div className={`bot stats left sidebar ${props.isActive ? "active" : ""}`}>
            <div className="bot stats left sidebar_close" onClick={() => props.setSideActive('left', false)}>
                <Icon name="angle left" inverted={true} size="large"></Icon>
            </div>
            <SideBarTitle></SideBarTitle>
            <Divider></Divider>
            <NaviMenu></NaviMenu>
        </div>
    )
}

function SideBarTitle(props) {
    return (
        <img src={BotLogo} alt="Bot Logo" className="bot stats site_title"></img>
    )
}


function NaviMenu(props) {
    const [active_item, setActive] = useState("");
    function handleClick(e) {
        setActive(e.target.getAttribute("data-name"));
    }
    return (
        <Menu text vertical inverted>
            <Menu.Item data-name="about" active={active_item === "about"} onClick={handleClick}>
                <Icon name="home"></Icon>
                About
            </Menu.Item>
            <Menu.Item data-name="stats" active={active_item === "stats"} onClick={handleClick}>
                <Icon name="chart bar"></Icon>
                Statistics
            </Menu.Item>
            <Menu.Item data-name="status" active={active_item === "status"} onClick={handleClick}>
                <Icon name="tachometer alternate"></Icon>
                Server Status
            </Menu.Item>
        </Menu>
    )
}


function RightSideBar(props) {

    // useEffect(() => {
    //     if (props.isActive) {
    //         window.addEventListener("click", handleClickOutside);
    //     }
    //     return () => {
    //         window.removeEventListener("click", handleClickOutside);
    //     }
    // }, [props.isActive]);

    // function handleClickOutside(e) {
    //     if (!e.target.classList.contains("bot", "stats", "right", "sidebar")) {
    //         props.setSideActive('right', false);
    //     }
    // }

    return (
        <div className={`bot stats right sidebar ${props.isActive ? "active" : ""}`}>
            <div className="bot stats right sidebar_close" onClick={() => props.setSideActive('right', false)}>
                <Icon name="angle right" size="large"></Icon>
            </div>
            <Divider className="bot stats sidebar_close"></Divider>
            { props.children }
        </div>
    )
}

function StatsOptions(props) {
    const [start_date, setStartDate] = useState(props.defaultStartDate);
    const [end_date, setEndDate] = useState(props.defaultEndDate);
    const [select_seiyuu, setSeiyuu] = useState(props.defaultSeiyuu);
    function handleSelectSeiyuu(e) {
        setSeiyuu(e.target.getAttribute("data-seiyuu"));
    }

    const presetOptions = [
        {key:"stats_preset_week", text:"Last 7 days", value:"week"},
        {key:"stats_preset_month", text:"Last 30 days", value:"month"},
        {key:"stats_preset_year", text:"Last 365 days", value:"year"},
        {key:"stats_preset_all", text:"All Time", value:"all"}
    ]
    return (
        <>
            <h3>Account</h3>
            <Menu text vertical>
                <Menu.Item data-seiyuu="kaorin" active={select_seiyuu === "kaorin"} onClick={handleSelectSeiyuu}>前田佳織里</Menu.Item>
                <Menu.Item data-seiyuu="chemi" active={select_seiyuu === "chemi"} onClick={handleSelectSeiyuu}>田中ちえ美</Menu.Item>
                <Menu.Item data-seiyuu="akarin" active={select_seiyuu === "akarin"} onClick={handleSelectSeiyuu}>鬼頭明里</Menu.Item>
            </Menu>
            <h3>Data Interval</h3>
            <Form>
                <Form.Input label="Start Date" type="date" value={props.defaultStartDate}></Form.Input>
                <Form.Input label="End Date" type="date" value={props.defaultEndDate}></Form.Input>
                <Form.Field>
                    <label>Preset</label>
                    <Dropdown fluid className="icon" text="Select Preset" button labeled icon="wait" options={presetOptions}></Dropdown>
                </Form.Field>
                <Form.Field>
                    <Button fluid>Apply</Button>
                </Form.Field>
                
            </Form>
        </>
    )
}

export {LeftSideBar, RightSideBar, StatsOptions};