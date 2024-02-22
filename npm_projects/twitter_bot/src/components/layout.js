import React, { useState, useEffect } from "react";
import './layout.css';
import { Grid, Icon } from "semantic-ui-react";
import { LeftSideBar, RightSideBar } from "./sidebar";
import { useLocation } from "react-router-dom";

import PropTypes from 'prop-types';

import store from "../store";
import { useSelector } from "react-redux";
import { setLeftActive, setRightActive, setViewWidth } from "../store/layout_slice";



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
    const location = useLocation();

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
                    {getTitle(location.pathname)}
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

function BotLayout(props) {

    const layout_state = useSelector(state => state.LayoutSlice);

    // const layout_state = {
    //     view_width: useSelector(state => state.LayoutSlice.view_width),
    //     responsive_width: useSelector(state => state.LayoutSlice.responsive_width)
    // };
    // const left_active = useSelector(state => state.LayoutSlice.left_active);
    // const right_active = useSelector(state => state.LayoutSlice.right_active);


    useEffect(() => {

        function updateViewWidth() {
            store.dispatch(setViewWidth(window.innerWidth));
        }

        // Attach the event listener to update viewWidth when the window is resized
        window.addEventListener('resize', updateViewWidth);

        // Clean up the event listener when the component unmounts
        return () => {
            window.removeEventListener('resize', updateViewWidth);
        };
    }, []);


    return (
        <>
            <TitleBar leftActive={layout_state.left_active && layout_state.view_width > layout_state.responsive_width} rightActive={layout_state.right_active} hasLeftIcon={layout_state.view_width <= layout_state.responsive_width} hasOptions={props.rightBarOptions ? true : false} />
            <LeftSideBar isActive={layout_state.left_active}></LeftSideBar>
            <RightSideBar isActive={layout_state.right_active}>
                {props.rightBarOptions}
            </RightSideBar>
            <div
                className={`bot stats sidebar_overlay ${(layout_state.right_active || (layout_state.left_active && layout_state.view_width <= layout_state.responsive_width)) ? "active" : ""}`}
                style={layout_state.left_active && layout_state.view_width <= layout_state.responsive_width ? { zIndex: 200 } : null}
                onClick={() => {
                    store.dispatch(setLeftActive(false));
                    store.dispatch(setRightActive(false));
                }}
            ></div>
            <div className={`bot stats content ${layout_state.left_active && layout_state.view_width > layout_state.responsive_width ? "left_active" : ""} ${layout_state.right_active ? "right_active" : ""}`}>
                {props.children}
            </div>
        </>
    )
}
BotLayout.propTypes = {
    rightBarOptions: PropTypes.element
}

export default BotLayout;

export { CompactContainer };