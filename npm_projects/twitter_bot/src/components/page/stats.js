import React, { useEffect, useState } from "react";
import { Segment, Statistic, Icon, Grid, Menu, Form, Button, Dropdown, Message, Modal, Table, Dimmer, Loader, Divider, Label } from "semantic-ui-react";
import { Line } from "react-chartjs-2";
import { Chart } from "chart.js/auto";
import 'chartjs-adapter-date-fns';
import { enUS } from 'date-fns/locale';
import "./stats.css"
import { set } from "date-fns";
import { Tweet } from 'react-tweet'




/**
 * A modal for viewing statistics detail
 * @param {object} props see prop
 * @prop {JSX} trigger The trigger of the modal
 * @prop {object} statsOptions The stats_options for fetch params
 * @prop {string} title The title of the modal
 * @prop {string} src The src url of the fetch
 * @returns JSX
 */
function StatsDetailModal(props) {
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);

    let display_tweets = [];

    useEffect(() => {
        setLoading(true);
        if (props.open && props.statsOptions && props.statsOptions.start_date && props.statsOptions.end_date && props.statsOptions.seiyuu) {
            fetch(props.src + "?" + new URLSearchParams(props.statsOptions).toString())
                .then(res => res.json())
                .then(data => {
                    if (!data.status) {
                        throw new Error("No data");
                    }
                    const data_arr = [];
                    for (let key in data) {
                        if (key !== "status") {
                            data_arr.push({
                                "name": key,
                                "value": data[key]
                            });
                        }
                    }
                    setData(data_arr);
                    setLoading(false);
                }
                ).catch(err => {
                    console.log(err);
                }
                );
        }
    }, [props.open, props.statsOptions]);

    const data_rows = data.map((item, index) => (
        <Table.Row key={index}>
            {(() => {
                switch (typeof item.value) {
                    case "number":
                        return (
                            <>
                                <Table.Cell width={6}>{item.name}</Table.Cell>
                                <Table.Cell width={10}>{item.value.toLocaleString('en-US', {
                                    maximumFractionDigits: 2,
                                    minimumFractionDigits: 0
                                })}</Table.Cell>
                            </>)
                    case "string":
                        return (
                            <>
                                <Table.Cell width={6}>{item.name}</Table.Cell>
                                <Table.Cell width={10}>{item.value}</Table.Cell>
                            </>)
                    case "boolean":
                        return (
                            <>
                                <Table.Cell width={6}>{item.name}</Table.Cell>
                                <Table.Cell width={10}>{item.value ? (<Icon name="check" color="green" />) : (<Icon name="x" color="green" />)}</Table.Cell>
                            </>)
                    case "object":
                        display_tweets = item.value;
                        return null;
                    default:
                        return <Table.Cell width={10}>Unknown</Table.Cell>
                }
            })()}
        </Table.Row>
    ))


    return (
        <Modal
            open={props.open}
        >
            <Modal.Header>{props.title}</Modal.Header>
            <Modal.Content scrolling>
                <h3>Detail</h3>
                <Table celled basic="very">
                    <Table.Body>
                        {data_rows}
                    </Table.Body>
                </Table>

                {display_tweets.length > 0 ? (
                    <>
                        <Divider></Divider>
                        <h3>Top 10 Tweets - {props.title}</h3>
                        {display_tweets.map((tweet_id, index) => (
                            <Segment style={{ "maxWidth": "550px", "margin": "1rem auto" }}>
                                <Label color='red' size="large" ribbon># {index + 1}</Label>
                                <Tweet key={index} id={tweet_id}></Tweet>
                            </Segment>
                        ))}
                    </>
                ) : null}

                {loading ? (
                    <Dimmer active>
                        <Loader></Loader>
                    </Dimmer>
                ) : null}
            </Modal.Content>
            <Modal.Actions>
                <Button onClick={props.handleClose}>Close</Button>
            </Modal.Actions>
        </Modal>
    )
}



/**
 * A block of a statistic data
 * @param {object} props see prop
 * @prop {integer} size The width of the block, 1-16, nullable
 * @prop {string} title The title (statistics meaning) of the block
 * @prop {string} iconName The font awesome icon name
 * @prop {string} value The value of the statistic
 * @prop {string} subinfo The subinfo of the statistic
 * @prop {boolean} loading Whether the block is loading
 * @prop {function} handleClick The function to handle the click event
 * @returns JSX
 */
function StatsBlock(props) {
    return (
        <Grid.Column width={props.size}>
            <Segment loading={props.loading} onClick={props.handleClick} style={props.handleClick ? { "cursor": "pointer" } : null}>
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

/**
 * 
 * @param {object} props see prop
 * @prop {object} crossData The cross data
 * @prop {function} updateCrossData The function to update the cross data
 * @returns JSX
 */
function Stats(props) {
    // props: seiyuu<str:"kaorin","akarin","chemi">, startDate<str:"YYYY-MM-DD">, endDate<str:"YYYY-MM-DD">
    const [stats, setStats] = useState({
        "status": true,
        "seiyuu_name": "",
        "seiyuu_id": "",
        "start_date": "",
        "end_date": "",
        "interval": 0,
        "posts": 0,
        "likes": 0,
        "rts": 0
    });
    const [followers, setFollowers] = useState({
        "status": true,
        "data": []
    });

    const [loading, setLoading] = useState(true);

    const [modalOpen, setModalOpen] = useState({
        "posts": false,
        "likes": false,
        "rts": false
    });

    const statsOptions = props.crossData;

    useEffect(() => {
        if (statsOptions && statsOptions.start_date && statsOptions.end_date && statsOptions.seiyuu) {
            console.log("fetching stats");
            setLoading(true);
            const url_params = new URLSearchParams();
            url_params.append("seiyuu", statsOptions.seiyuu);
            url_params.append("start_date", statsOptions.start_date);
            url_params.append("end_date", statsOptions.end_date);
            fetch("/bot/api/getStats/?" + url_params.toString())
                .then(res => res.json())
                .then(data => {
                    if (!data.status) {
                        throw new Error("No data");
                    }
                    setStats(data);
                    localStorage.setItem("stats_data", JSON.stringify(data));
                    setLoading(false);
                }
                ).catch(err => {
                    setStats({
                        "status": false,
                        "seiyuu_name": "",
                        "seiyuu_id": "",
                        "start_date": "",
                        "end_date": "",
                        "interval": 0,
                        "posts": 0,
                        "likes": 0,
                        "rts": 0
                    });
                    console.log(err);
                    setLoading(false);
                }
                );
            fetch("/bot/api/followers/get/?" + url_params.toString())
                .then(res => res.json())
                .then(data => {
                    if (!data.status) {
                        throw new Error("No data");
                    }
                    setFollowers(data);
                    setLoading(false);
                }
                ).catch(err => {
                    setFollowers({
                        "status": false,
                        "data": []
                    });
                    console.log(err);
                    setLoading(false);
                }
                );
        }
    }, [props.crossData]);

    // calculate current followers
    let curr_followers;
    if (followers.status && followers.data.length > 0) {
        curr_followers = followers.data[followers.data.length - 1].followers;
    }
    else {
        curr_followers = 0;
    }

    // calculate average followers growth
    let avg_followers_growth;
    if (followers.status && followers.data.length > 0) {
        const followers_diff = followers.data[followers.data.length - 1].followers - followers.data[0].followers;
        const day_diff = (new Date(followers.data[followers.data.length - 1].data_time) - new Date(followers.data[0].data_time)) / (1000 * 60 * 60 * 24);
        avg_followers_growth = followers_diff / day_diff;
    }
    else {
        avg_followers_growth = 0;
    }


    return (
        <>
            <h1>{stats.status ? (stats.seiyuu_name + " " + stats.seiyuu_id) : statsOptions.seiyuu}</h1>
            {stats.status ? (
                <Grid columns={3} stackable>
                    <StatsDetailModal open={modalOpen.posts} handleClose={() => setModalOpen(prev => ({ ...prev, posts: false }))} title="Posts" statsOptions={statsOptions} src="/bot/api/detailStats/posts/" />
                    <StatsBlock title="Posts" iconName="twitter" value={stats.posts.toLocaleString()} subinfo={`${(stats.posts / stats.interval).toFixed(2)} posts per hour`} loading={loading} handleClick={() => setModalOpen(prev => ({ ...prev, posts: true }))} />

                    <StatsDetailModal open={modalOpen.likes} handleClose={() => setModalOpen(prev => ({ ...prev, likes: false }))} title="Likes" statsOptions={statsOptions} src="/bot/api/detailStats/likes/" />
                    <StatsBlock title="Likes" iconName="heart" value={stats.likes.toLocaleString()} subinfo={`${(stats.likes / stats.posts).toFixed(2)} likes per post`} loading={loading} handleClick={() => setModalOpen(prev => ({ ...prev, likes: true }))} />

                    <StatsDetailModal open={modalOpen.rts} handleClose={() => setModalOpen(prev => ({ ...prev, rts: false }))} title="Retweets" statsOptions={statsOptions} src="/bot/api/detailStats/rts/" />
                    <StatsBlock title="Retweets" iconName="retweet" value={stats.rts.toLocaleString()} subinfo={`${(stats.rts / stats.posts).toFixed(2)} retweets per post`} loading={loading} handleClick={() => setModalOpen(prev => ({ ...prev, rts: true }))} />
                </Grid>
            ) : (
                <Message negative>
                    <Message.Header>Failed to load statistics: {statsOptions.start_date} ~ {statsOptions.end_date}</Message.Header>
                    <p>There is no post data for the selected time interval.</p>
                </Message>
            )}
            {followers.status ? (
                <Grid columns={3} stackable>
                    <StatsBlock size={16} title="Followers" iconName="users" value={curr_followers.toLocaleString()} subinfo={`${avg_followers_growth.toFixed(2)} new followers per day`} loading={loading}>
                        <div className="bot stats linechart_container">
                            <div className="bot stats linechart_wrapper">
                                <Line data={{
                                    labels: followers.data.map((item) => (item.data_time)),
                                    datasets: [
                                        {
                                            label: "Followers",
                                            data: followers.data.map((item) => (item.followers)),
                                            fill: false,
                                            borderColor: "#2185d0",
                                            backgroundColor: "#2185d0",
                                            tension: 0.1,
                                        }
                                    ]
                                }} options={{
                                    plugins: {
                                        legend: {
                                            display: false
                                        }
                                    },
                                    scales: {
                                        x: {
                                            type: "time",
                                            adapters: {
                                                date: {
                                                    locale: enUS, // Add this line to set the locale
                                                }, // Specify the adapter name without locale configuration
                                            },
                                        },
                                        y: {
                                            beginAtZero: false,
                                        },
                                    },
                                }} />
                            </div>
                        </div>

                    </StatsBlock>
                </Grid>

            ) : (
                <Message negative>
                    <Message.Header>Failed to load followers data: {statsOptions.start_date} ~ {statsOptions.end_date}</Message.Header>
                    <p>There is no followers data for the selected time interval.</p>
                </Message>
            )}

        </>
    )
}


/**
 * 
 * @param {object} props see prop
 * @prop {function} updateCrossData - The function to update the cross data
 * @prop {function} handleSideActive - The function to handle the side bar active 
 * @prop {object} crossData - The cross data
 * @returns JSX
 */
function StatsOptions(props) {
    const [statsOptions, setStatsOptions] = useState({
        "start_date": "",
        "end_date": "",
        "seiyuu": ""
    });


    const localStorage = window.localStorage;


    function handleSelectSeiyuu(e) {
        setStatsOptions(prev => (
            {
                ...prev,
                "seiyuu": e.target.getAttribute("data-seiyuu")
            }
        ));
        handleApply();
    }

    useEffect(() => {
        // if (localStorage.getItem("stats_options")) {
        //     const stats_options = JSON.parse(localStorage.getItem("stats_options"));
        //     setStartDate(stats_options.start_date);
        //     setEndDate(stats_options.end_date);
        //     setSeiyuu(stats_options.seiyuu);
        // }
        const curr_time = new Date();
        const curr_date = curr_time.toISOString().split("T")[0];
        const prev_time = new Date(curr_time.getTime() - 7 * 24 * 60 * 60 * 1000);
        const prev_date = prev_time.toISOString().split("T")[0];
        setStatsOptions({
            "start_date": prev_date,
            "end_date": curr_date,
            "seiyuu": "kaorin"
        });
    }, []);

    useEffect(() => {
        props.updateCrossData(statsOptions);
    }, [statsOptions]);

    function handleApply() {
        localStorage.setItem("stats_options", JSON.stringify(statsOptions));
        props.handleSideActive("right", false);
    }

    function handlePresets(preset_value) {
        const curr_time = new Date();
        const curr_date = curr_time.toISOString().split("T")[0];
        if (preset_value === "week") {
            const prev_time = new Date(curr_time.getTime() - 7 * 24 * 60 * 60 * 1000);
            const prev_date = prev_time.toISOString().split("T")[0];
            setStatsOptions(prev => (
                {
                    ...prev,
                    "start_date": prev_date,
                    "end_date": curr_date
                }
            ));
        }
        else if (preset_value === "month") {
            const prev_time = new Date(curr_time.getTime() - 30 * 24 * 60 * 60 * 1000);
            const prev_date = prev_time.toISOString().split("T")[0];
            setStatsOptions(prev => (
                {
                    ...prev,
                    "start_date": prev_date,
                    "end_date": curr_date
                }
            ));
        }
        else if (preset_value === "year") {
            const prev_time = new Date(curr_time.getTime() - 365 * 24 * 60 * 60 * 1000);
            const prev_date = prev_time.toISOString().split("T")[0];
            setStatsOptions(prev => (
                {
                    ...prev,
                    "start_date": prev_date,
                    "end_date": curr_date
                }
            ));
        }
        else if (preset_value === "all") {
            setStatsOptions(prev => (
                {
                    ...prev,
                    "start_date": "2000-01-01",
                    "end_date": curr_date
                }
            ));
        }

        handleApply();
    }


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
                <Menu.Item data-seiyuu="kaorin" active={statsOptions.seiyuu === "kaorin"} onClick={handleSelectSeiyuu}>前田佳織里</Menu.Item>
                <Menu.Item data-seiyuu="chemi" active={statsOptions.seiyuu === "chemi"} onClick={handleSelectSeiyuu}>田中ちえ美</Menu.Item>
                <Menu.Item data-seiyuu="akarin" active={statsOptions.seiyuu === "akarin"} onClick={handleSelectSeiyuu}>鬼頭明里</Menu.Item>
                <Menu.Item data-seiyuu="konachi" active={statsOptions.seiyuu === "konachi"} onClick={handleSelectSeiyuu}>月音こな</Menu.Item>
            </Menu>
            <h3>Data Interval</h3>
            <Form>
                <Form.Input label="Start Date" control="input" type="date" value={statsOptions.start_date} onChange={(e) => setStartDate(prev => ({ ...prev, "start_date": e.target.value }))}></Form.Input>
                <Form.Input label="End Date" control="input" type="date" value={statsOptions.end_date} onChange={(e) => setEndDate(prev => ({ ...prev, "end_date": e.target.value }))}></Form.Input>
                <Form.Field>
                    <label>Preset</label>
                    <Dropdown fluid className="icon" text="Select Preset" button labeled icon="wait" options={presetOptions} onChange={(e, { value }) => {
                        handlePresets(value);
                    }}></Dropdown>
                </Form.Field>
                <Form.Field>
                    <Button fluid onClick={handleApply}>Apply</Button>
                </Form.Field>

            </Form>
        </>
    )
}

export { Stats, StatsOptions };