import React, { useState, useEffect } from "react";
import './layout.css';
import { Grid, Icon } from "semantic-ui-react";
import { LeftSideBar, RightSideBar } from "./sidebar";
import { useLocation } from "react-router-dom";




function TitleBar(props) {
    const location = useLocation();


    return (
        <div className={`bot stats title bar ${props.leftActive ? "left_active" : ""} ${props.rightActive ? "right_active" : ""}`}>
            <Grid verticalAlign="middle">
                <Grid.Column width={2} textAlign="left">
                    {props.hasLeftIcon ? <div className="bot stats left bar_icon">
                        <Icon name="bars" onClick={() => props.setSideActive('left', !props.leftActive)} size="large"></Icon>
                    </div> : null}
                </Grid.Column>
                <Grid.Column width={12} textAlign="center">
                    {(() => {
                        switch (location.pathname) {
                            case "/bot/login":
                                return <h2>Login</h2>;
                            case "/bot/stats":
                                return <h2>Statistics</h2>;
                            case "/bot/config":
                                return <h2>Service Configuration</h2>;
                            case "/bot/library":
                                return <h2>Image Library</h2>;
                            case "/bot/logs":
                                return <h2>Service Logs</h2>;
                            default:
                                return <h2>About</h2>;
                        }
                    })()}
                </Grid.Column>
                <Grid.Column width={2} textAlign="right">
                    {props.hasOptions ?
                        <div className="bot stats right bar_icon">
                            <Icon name="sliders horizontal" onClick={() => props.setSideActive('right', !props.rightActive)} size="large"></Icon>
                        </div>
                        : null}
                </Grid.Column>
            </Grid>
        </div>
    )
}

const responsiveWidth = 1000;

function BotLayout(props) {
    const [left_active, setLeftActive] = useState(true);
    const [right_active, setRightActive] = useState(false);
    const [viewWidth, setViewWidth] = useState(window.innerWidth);

    function handleSideActive(side, setActive) {
        if (side === 'left') {
            setLeftActive(setActive);
            if (viewWidth <= responsiveWidth) {
                setRightActive(false);
            }
        }
        else if (side === 'right') {
            setRightActive(setActive);
            if (viewWidth <= responsiveWidth) {
                setLeftActive(false);
            }
        }
    }

    useEffect(() => {

        function updateViewWidth() {
            setViewWidth(window.innerWidth);
        }

        // Attach the event listener to update viewWidth when the window is resized
        window.addEventListener('resize', updateViewWidth);

        // Clean up the event listener when the component unmounts
        return () => {
            window.removeEventListener('resize', updateViewWidth);
        };
    }, []);

    useEffect(() => {
        if (viewWidth > responsiveWidth) {
            setLeftActive(true);
        }
        else {
            setLeftActive(false);
        }
    }, [viewWidth]);


    return (
        <>
            <TitleBar leftActive={left_active && viewWidth > responsiveWidth} rightActive={right_active} setSideActive={handleSideActive} hasLeftIcon={viewWidth <= responsiveWidth} hasOptions={props.rightBarOptions ? true : false} />
            <LeftSideBar setSideActive={handleSideActive} isActive={left_active}></LeftSideBar>
            <RightSideBar setSideActive={handleSideActive} isActive={right_active}>
                {React.cloneElement(props.rightBarOptions, { "handleSideActive": handleSideActive, ...props.rightBarOptions.props })}
            </RightSideBar>
            <div className={`bot stats sidebar_overlay ${(right_active || (viewWidth <= responsiveWidth && left_active)) ? "active" : ""}`} onClick={() => {
                setRightActive(false);
                if (viewWidth <= responsiveWidth) {
                    setLeftActive(false)
                }
            }}></div>
            <div className={`bot stats content ${left_active && viewWidth > responsiveWidth ? "left_active" : ""} ${right_active ? "right_active" : ""}`}>
                {props.children}
            </div>
        </>
    )
}

export default BotLayout;