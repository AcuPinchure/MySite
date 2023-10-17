import React, {useState} from "react";
import './layout.css';
import { Grid, Icon } from "semantic-ui-react";
import {LeftSideBar, RightSideBar, StatsOptions} from "./sidebar";
import { HashRouter, Route } from "react-router-dom";

import Stats from "./page/stats";



function TitleBar(props) {
    return (
        <div className="bot stats title bar">
            <Grid verticalAlign="middle">
                <Grid.Column width={2} textAlign="left">
                    <div className="bot stats left bar_icon">
                        <Icon name="bars" onClick={() => props.setSideActive('left', true)} size="large"></Icon>
                    </div>
                </Grid.Column>
                <Grid.Column width={12} textAlign="center">
                    <h2>{props.title}</h2>
                </Grid.Column>
                <Grid.Column width={2} textAlign="right">
                    <div className="bot stats right bar_icon">
                        <Icon name="cog" onClick={() => props.setSideActive('right', true)} size="large"></Icon>
                    </div>
                </Grid.Column>
            </Grid>
        </div>
    )
}



function BotLayout() {
    const [left_active, setLeftActive] = useState(false);
    const [right_active, setRightActive] = useState(false);
    const [title, setTitle] = useState("Statistics");

    function handleSideActive(side, setActive) {
        if (side==='left') {
            setLeftActive(setActive);
        }
        else if (side==='right') {
            setRightActive(setActive);
        }
    }
    return (
        <>
            <TitleBar title={title} setSideActive={handleSideActive}></TitleBar>
            <LeftSideBar setSideActive={handleSideActive} isActive={left_active}></LeftSideBar>
            <RightSideBar setSideActive={handleSideActive} isActive={right_active}>
                <StatsOptions defaultStartDate="2023-06-30" defaultEndDate="2023-07-31" defaultSeiyuu="kaorin"></StatsOptions>
            </RightSideBar>
            <div className="bot stats content">
                <HashRouter>
                    <Route path="/stats" component={Stats} />
                </HashRouter>
            </div>
        </>
    )
}

export default BotLayout;