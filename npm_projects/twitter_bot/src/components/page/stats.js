import React, { useEffect, useState } from "react";
import { Segment, Statistic, Icon, Grid, Menu, Form, Button, Dropdown } from "semantic-ui-react";


function StatsBlock(props) {
    // props: size<int:1-3>, title<str>, iconName<str>, value<str>, subinfo<str>, loading<bool>
    return (
        <Grid.Column width={props.size}>
            <Segment loading={props.loading}>
                <h3>
                    <Icon name={props.iconName} />
                    {props.title}
                </h3>
                <Statistic>
                    <Statistic.Value>{props.value}</Statistic.Value>
                </Statistic>
                <div className="bot stats subinfo">
                    {props.subinfo}
                </div>
            </Segment>
        </Grid.Column>
    )
}


function Stats(props) {
    // props: seiyuu<str:"kaorin","akarin","chemi">, startDate<str:"YYYY-MM-DD">, endDate<str:"YYYY-MM-DD">
    const [stats, setStats] = useState({
        "seiyuu_name": "前田佳織里",
        "seiyuu_id": "@kaorin__bot",
        "start_date": "2023-06-01 00:00",
        "end_date": "2023-07-01 23:59",
        "interval": 223, // hours
        "posts": 223,
        "likes": 3425,
        "rts": 302,
        "top_likes": [
            {

            }
        ],
        "top_rts": [],
        "followers": [
            {
                "date": "2023-06-01 00:00:05",
                "followers": 2350
            }
        ]
    });

    const [loading, setLoading] = useState(true);

    return (
        <>  
            <h1>{stats.seiyuu_name + " " + stats.seiyuu_id}</h1>
            <Grid columns={3} stackable>
                
            </Grid>
        </>
    )
}

function StatsOptions(props) {
    const [start_date, setStartDate] = useState(null);
    const [end_date, setEndDate] = useState(null);
    const [select_seiyuu, setSeiyuu] = useState(null);
    function handleSelectSeiyuu(e) {
        setSeiyuu(e.target.getAttribute("data-seiyuu"));
    }

    useEffect(() => {
        setStartDate(props.defaultStartDate);
        setEndDate(props.defaultEndDate);
        setSeiyuu(props.defaultSeiyuu);
    }, [props.defaultStartDate, props.defaultEndDate, props.defaultSeiyuu]);

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

export {Stats, StatsOptions};