import React, { useState, useEffect } from "react";
import './layout.css';
import { Grid, Icon } from "semantic-ui-react";
import { LeftSideBar, RightSideBar, SideBarDimmer } from "./sidebar";
import { useLocation } from "react-router-dom";

import PropTypes from 'prop-types';

import store from "../store";
import { useSelector } from "react-redux";
import { setLeftActive, setRightActive } from "../store/layout_slice";

import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';


import About from './page/about';
import { Stats, StatsOptions } from "./page/stats";
import Login from './page/login';
import ConfigPage from './page/service_config';
import StatusPage from './page/service_status';
import { LibraryOptions, ImageLibrary } from './page/library';
import LogPage from "./page/logs";


function CompactContainer(props) {
    return (
        <div style={{ maxWidth: "32rem", margin: "auto", paddingTop: props.topPadded ? "20vh" : "0" }}>
            {props.children}
        </div>
    )
}
CompactContainer.propTypes = {
    children: PropTypes.oneOfType([
        PropTypes.arrayOf(PropTypes.node),
        PropTypes.node
    ]),
    topPadded: PropTypes.bool
}




function getTitle(pathname) {
    switch (pathname) {
        case "/bot/login/":
            return <h2>Login</h2>;
        case "/bot/stats/":
            return <h2>Statistics</h2>;
        case "/bot/status/":
            return <h2>Service Status</h2>;
        case "/bot/config/":
            return <h2>Service Configuration</h2>;
        case "/bot/library/":
            return <h2>Image Library</h2>;
        case "/bot/logs/":
            return <h2>Service Logs</h2>;
        default:
            return <h2>About</h2>;
    }
}

function TitleBar(props) {
    const path_name = useLocation().pathname;

    function handleSideActive(side, active) {
        if (side === "left") {
            store.dispatch(setLeftActive(active));
        }
        else if (side === "right") {
            store.dispatch(setRightActive(active));
        }
    }

    return (
        <div className={`bot stats title bar ${props.leftActive ? "left_active" : ""} ${props.rightActive ? "right_active" : ""}`}>
            <Grid verticalAlign="middle">
                <Grid.Column width={2} textAlign="left">
                    {props.hasLeftIcon ? <div className="bot stats left bar_icon">
                        <Icon name="bars" onClick={() => handleSideActive('left', !props.leftActive)} size="large"></Icon>
                    </div> : null}
                </Grid.Column>
                <Grid.Column width={12} textAlign="center">
                    {getTitle(path_name)}
                </Grid.Column>
                <Grid.Column width={2} textAlign="right">
                    {props.hasOptions ?
                        <div className="bot stats right bar_icon">
                            <Icon name="sliders horizontal" onClick={() => handleSideActive('right', !props.rightActive)} size="large"></Icon>
                        </div>
                        : null}
                </Grid.Column>
            </Grid>
        </div>
    )
}
TitleBar.propTypes = {
    leftActive: PropTypes.bool,
    rightActive: PropTypes.bool,
    hasLeftIcon: PropTypes.bool,
    hasOptions: PropTypes.bool
}



function BotLayout() {

    const layout_state = useSelector(state => state.LayoutSlice);

    const path_name = useLocation().pathname;

    console.log(path_name);


    return (
        <>
            <Route exact path="/bot/" component={About} />
            {
                path_name !== "/bot/"
                &&
                <>
                    <TitleBar
                        leftActive={layout_state.left_active && layout_state.view_width > layout_state.responsive_width}
                        rightActive={layout_state.right_active}
                        hasLeftIcon={layout_state.view_width <= layout_state.responsive_width}
                        hasOptions={["/bot/stats/", "/bot/library/"].includes(path_name)}
                    />
                    <LeftSideBar isActive={layout_state.left_active} />
                    <RightSideBar isActive={layout_state.right_active}>
                        <Route path="/bot/stats/" component={StatsOptions} />
                        <Route path="/bot/library/" component={LibraryOptions} />
                    </RightSideBar>
                    <SideBarDimmer />
                    <div className={`bot stats content ${layout_state.left_active && layout_state.view_width > layout_state.responsive_width ? "left_active" : ""} ${layout_state.right_active ? "right_active" : ""}`}>
                        <Route path="/bot/stats/" component={Stats} />
                        <Route path="/bot/login/" component={Login} />
                        <Route path="/bot/status/" component={StatusPage} />
                        <Route path="/bot/config/" component={ConfigPage} />
                        <Route path="/bot/library/" component={ImageLibrary} />
                        <Route path="/bot/logs/" component={LogPage} />
                    </div>
                </>
            }
        </>
    )
}
BotLayout.propTypes = {
    rightBarOptions: PropTypes.element
}

export default BotLayout;
export { CompactContainer };