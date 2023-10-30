import React, { useEffect, useState } from "react";
import { Segment, Statistic, Icon, Grid, Menu, Form, Button, Dropdown } from "semantic-ui-react";

/**
 * A block of a statistic data
 * @prop {integer} size The width of the block, 1-16, nullable
 * @prop {string} title The title (statistics meaning) of the block
 * @prop {string} iconName The font awesome icon name
 * @prop {string} value The value of the statistic
 * @prop {string} subinfo The subinfo of the statistic
 * @prop {boolean} loading Whether the block is loading
 * @returns JSX
 */
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
                {props.children}
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
            },
            {
                "date": "2023-07-01 23:00:05",
                "followers": 2400
            }
        ]
    });

    const [loading, setLoading] = useState(true);

    const avg_followers_growth = (stats.followers[stats.followers.length - 1].followers - stats.followers[0].followers) / stats.interval * 24;

    return (
        <>
            <h1>{stats.seiyuu_name + " " + stats.seiyuu_id}</h1>
            <Grid columns={3} stackable>
                <StatsBlock title="Posts" iconName="twitter" value={stats.posts} subinfo={`${(stats.posts / stats.interval).toFixed(2)} posts per hour`} loading={false} />
                <StatsBlock title="Likes" iconName="heart" value={stats.likes} subinfo={`${(stats.likes / stats.posts).toFixed(2)} likes per post`} loading={false} />
                <StatsBlock title="Retweets" iconName="retweet" value={stats.rts} subinfo={`${(stats.rts / stats.posts).toFixed(2)} retweets per post`} loading={false} />
                <StatsBlock size={16} title="Followers" iconName="users" value={stats.followers[stats.followers.length - 1].followers} subinfo={`${avg_followers_growth.toFixed(2)} new followers per day`} loading={false}>
                    Line chart here
                </StatsBlock>
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
        { key: "stats_preset_week", text: "Last 7 days", value: "week" },
        { key: "stats_preset_month", text: "Last 30 days", value: "month" },
        { key: "stats_preset_year", text: "Last 365 days", value: "year" },
        { key: "stats_preset_all", text: "All Time", value: "all" }
    ]
    return (
        <>
            <h3>Account</h3>
            <Menu text vertical>
                <Menu.Item data-seiyuu="kaorin" active={select_seiyuu === "kaorin"} onClick={handleSelectSeiyuu}>前田佳織里</Menu.Item>
                <Menu.Item data-seiyuu="chemi" active={select_seiyuu === "chemi"} onClick={handleSelectSeiyuu}>田中ちえ美</Menu.Item>
                <Menu.Item data-seiyuu="akarin" active={select_seiyuu === "akarin"} onClick={handleSelectSeiyuu}>鬼頭明里</Menu.Item>
                <Menu.Item data-seiyuu="konachi" active={select_seiyuu === "konachi"} onClick={handleSelectSeiyuu}>月音こな</Menu.Item>
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

export { Stats, StatsOptions };