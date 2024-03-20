import React, { useEffect, useState } from "react";
import { Segment, Statistic, Icon, Grid, Menu, Form, Button, Dropdown, Message, Modal, Table, Dimmer, Loader, Divider, Label } from "semantic-ui-react";
import "./stats.css"
import { set } from "date-fns";
import { Tweet } from 'react-tweet'

import store from "../../store";
import { useSelector } from "react-redux";
import { setStatsOption, setSummary, setFollowers, setLikesDetail, setPostsDetail, setRtsDetail } from "../../store/stats_slice";
import { setRightActive } from "../../store/layout_slice";

import Chart from "react-apexcharts";

import PropTypes from 'prop-types';
import { setActiveTab, setFilterOptions, setLibraryLoading } from "../../store/library_slice";
import { useHistory } from "react-router-dom/cjs/react-router-dom.min";




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

    const show_admin_menu = useSelector(state => state.LayoutSlice.show_admin_menu);

    const history = useHistory();

    let display_tweets = [];

    useEffect(() => {
        setLoading(true);
        if (props.open && props.statsOptions && props.statsOptions.start_date && props.statsOptions.end_date && props.statsOptions.seiyuu_id_name) {
            fetch(props.src + "?" + new URLSearchParams({
                "seiyuu": props.statsOptions.seiyuu_id_name,
                "start_date": props.statsOptions.start_date,
                "end_date": props.statsOptions.end_date
            }).toString())
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
    }, [props.statsOptions, props.open, props.src]);

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

    function handleToLibrary(tweet_id) {
        if (!show_admin_menu) {
            window.location.href = "/bot/login/";
        };
        store.dispatch(setFilterOptions({
            "tweet_id": tweet_id
        }));
        store.dispatch(setActiveTab("tweet_id"));
        store.dispatch(setLibraryLoading(true));
        history.push("/bot/library/");
    }


    return (
        <Modal
            open={props.open}
            onClose={props.handleClose}
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
                            <Segment key={index} style={{ "maxWidth": "550px", "margin": "1rem auto" }}>
                                <Label color='red' size="large" ribbon># {index + 1}</Label>
                                <Tweet id={tweet_id}></Tweet>
                                {
                                    show_admin_menu
                                    &&
                                    <Button fluid onClick={() => handleToLibrary(tweet_id)}>
                                        View This Image In Library
                                    </Button>}
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
StatsDetailModal.propTypes = {
    open: PropTypes.bool.isRequired,
    handleClose: PropTypes.func.isRequired,
    title: PropTypes.string.isRequired,
    src: PropTypes.string.isRequired,
    statsOptions: PropTypes.object.isRequired
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
StatsBlock.propTypes = {
    size: PropTypes.number,
    title: PropTypes.string.isRequired,
    iconName: PropTypes.string.isRequired,
    value: PropTypes.string.isRequired,
    subinfo: PropTypes.string.isRequired,
    loading: PropTypes.bool.isRequired,
    handleClick: PropTypes.func
}

/**
 * 
 * @returns JSX
 */
function Stats() {
    const stats_options = useSelector(state => state.StatsSlice.stats_options);
    const stats_summary = useSelector(state => state.StatsSlice.summary);
    const followers = useSelector(state => state.StatsSlice.followers);

    const curr_seiyuu = stats_options.seiyuu_list.find(item => item.id_name === stats_options.seiyuu_id_name);

    const [loading, setLoading] = useState(true);

    const [modalOpen, setModalOpen] = useState({
        "posts": false,
        "likes": false,
        "rts": false
    });

    useEffect(() => {
        if (!(stats_options.start_date && stats_options.end_date && stats_options.seiyuu_id_name)) return;
        console.log("fetching stats");
        setLoading(true);
        const url_params = new URLSearchParams();
        url_params.append("seiyuu", stats_options.seiyuu_id_name);
        url_params.append("start_date", stats_options.start_date);
        url_params.append("end_date", stats_options.end_date);
        const summary_fetch = fetch("/bot/api/getStats/?" + url_params.toString())
            .then(res => res.json())
            .then(data => {
                if (!data.status) {
                    throw new Error("No data");
                }
                store.dispatch(setSummary({
                    "seiyuu_name": data.seiyuu_name,
                    "seiyuu_id": data.seiyuu_id,
                    "start_date": data.start_date,
                    "end_date": data.end_date,
                    "interval": data.interval,
                    "posts": data.posts,
                    "likes": data.likes,
                    "rts": data.rts
                }));
            }
            ).catch(err => {
                store.dispatch(setSummary({
                    "seiyuu_name": "",
                    "seiyuu_id": "",
                    "start_date": "",
                    "end_date": "",
                    "interval": 0,
                    "posts": 0,
                    "likes": 0,
                    "rts": 0
                }));
                console.error(err);
            }
            );
        const followers_fetch = fetch("/bot/api/followers/get/?" + url_params.toString())
            .then(res => res.json())
            .then(data => {
                if (!data.status) {
                    throw new Error("No data");
                }
                store.dispatch(setFollowers(data.data));
            }
            ).catch(err => {
                store.dispatch(setFollowers([]));
                console.error(err);
            }
            );

        Promise.all([summary_fetch, followers_fetch]).then(() => {
            setLoading(false);
        }).catch(err => {
            alert("Failed to fetch data");
            console.error(err);
            setLoading(false);
        });
    }, [stats_options.seiyuu_id_name, stats_options.start_date, stats_options.end_date]);

    // calculate current followers
    let curr_followers;
    if (followers.length > 0) {
        curr_followers = followers[followers.length - 1].followers;
    }
    else {
        curr_followers = 0;
    }

    // calculate average followers growth
    let avg_followers_growth;
    if (followers.length > 0) {
        const followers_diff = followers[followers.length - 1].followers - followers[0].followers;
        const day_diff = (new Date(followers[followers.length - 1].data_time) - new Date(followers[0].data_time)) / (1000 * 60 * 60 * 24);
        avg_followers_growth = followers_diff / day_diff;
    }
    else {
        avg_followers_growth = 0;
    }


    return (
        <>
            <h1>{curr_seiyuu && `${curr_seiyuu.name} @${curr_seiyuu.screen_name}`}</h1>
            {(stats_summary.start_date && stats_summary.end_date && stats_options.seiyuu_id_name) ? (
                <Grid columns={3} stackable>
                    <StatsDetailModal open={modalOpen.posts} handleClose={() => setModalOpen(prev => ({ ...prev, posts: false }))} title="Posts" statsOptions={stats_options} src="/bot/api/detailStats/posts/" />
                    <StatsBlock title="Posts" iconName="twitter" value={stats_summary.posts.toLocaleString()} subinfo={`${(stats_summary.posts / stats_summary.interval).toFixed(2)} posts per hour`} loading={loading} handleClick={() => setModalOpen(prev => ({ ...prev, posts: true }))} />

                    <StatsDetailModal open={modalOpen.likes} handleClose={() => setModalOpen(prev => ({ ...prev, likes: false }))} title="Likes" statsOptions={stats_options} src="/bot/api/detailStats/likes/" />
                    <StatsBlock title="Likes" iconName="heart" value={stats_summary.likes.toLocaleString()} subinfo={`${(stats_summary.likes / stats_summary.posts).toFixed(2)} likes per post`} loading={loading} handleClick={() => setModalOpen(prev => ({ ...prev, likes: true }))} />

                    <StatsDetailModal open={modalOpen.rts} handleClose={() => setModalOpen(prev => ({ ...prev, rts: false }))} title="Retweets" statsOptions={stats_options} src="/bot/api/detailStats/rts/" />
                    <StatsBlock title="Retweets" iconName="retweet" value={stats_summary.rts.toLocaleString()} subinfo={`${(stats_summary.rts / stats_summary.posts).toFixed(2)} retweets per post`} loading={loading} handleClick={() => setModalOpen(prev => ({ ...prev, rts: true }))} />
                </Grid>
            ) : (
                <Message negative>
                    <Message.Header>Failed to load statistics: {stats_options.start_date} ~ {stats_options.end_date}</Message.Header>
                    <p>There is no post data in the selected date interval.</p>
                </Message>
            )}
            {followers.length > 0 ? (
                <Grid columns={3} stackable>
                    <StatsBlock size={16} title="Followers" iconName="users" value={curr_followers.toLocaleString()} subinfo={`${avg_followers_growth.toFixed(2)} new followers per day`} loading={loading}>
                        <div className="bot stats linechart_container">
                            <div className="bot stats linechart_wrapper">
                                <Chart
                                    options={{
                                        chart: {
                                            id: "followers-chart",
                                            type: "line",
                                            zoom: {
                                                type: 'x',
                                                enabled: true,
                                                autoScaleYaxis: false
                                            }
                                        },
                                        dataLabels: {
                                            enabled: false
                                        },
                                        markers: {
                                            size: 0,
                                        },
                                        title: {
                                            text: 'Followers Trends',
                                            align: 'left'
                                        },
                                        xaxis: {
                                            type: "datetime",
                                        },
                                    }}
                                    series={[
                                        {
                                            name: "followers",
                                            data: followers.map(item => [new Date(item.data_time), item.followers])
                                        }
                                    ]}
                                    type="line"
                                    width="100%"
                                ></Chart>
                            </div>
                        </div>

                    </StatsBlock>
                </Grid>

            ) : (
                <Message negative>
                    <Message.Header>Failed to load followers data: {stats_options.start_date} ~ {stats_options.end_date}</Message.Header>
                    <p>There is no followers data in the selected date interval.</p>
                </Message>
            )}

        </>
    )
}


function StatsOptions() {
    const curr_date = new Date();
    const curr_date_str = curr_date.toISOString().split("T")[0];
    const prev_date = new Date(curr_date.getTime() - 7 * 24 * 60 * 60 * 1000);
    const prev_date_str = prev_date.toISOString().split("T")[0];

    const stats_options = useSelector(state => state.StatsSlice.stats_options);

    const [statsOptionLocal, setStatsOptionLocal] = useState({
        "seiyuu_id_name": "",
        "start_date": "",
        "end_date": ""
    });

    useEffect(() => {
        if (stats_options.seiyuu_list.length === 0) return;
        if (stats_options.seiyuu_id_name && stats_options.start_date && stats_options.end_date) return;
        store.dispatch(setStatsOption({
            "seiyuu_id_name": stats_options.seiyuu_list[0].id_name,
            "start_date": prev_date_str,
            "end_date": curr_date_str
        }));
    }, [stats_options.seiyuu_list]);

    useEffect(() => {
        if (stats_options.seiyuu_id_name && stats_options.start_date && stats_options.end_date) {
            setStatsOptionLocal({
                "seiyuu_id_name": stats_options.seiyuu_id_name,
                "start_date": stats_options.start_date,
                "end_date": stats_options.end_date
            });
        }
    }, [stats_options.seiyuu_id_name, stats_options.start_date, stats_options.end_date]);

    function handleSelectSeiyuu(e) {
        store.dispatch(setStatsOption({
            ...stats_options,
            seiyuu_id_name: e.target.getAttribute("data-seiyuu")
        })
        );
        store.dispatch(setRightActive(false));
    }

    function handleSelectPreset(start_date, end_date) {
        store.dispatch(setStatsOption({
            ...stats_options,
            "start_date": start_date,
            "end_date": end_date
        }));
        store.dispatch(setRightActive(false));
    }

    function handleApply() {
        store.dispatch(setStatsOption({
            ...stats_options,
            ...statsOptionLocal
        }));
        store.dispatch(setRightActive(false));
    }

    return (
        <>
            <h3>Account</h3>
            <Menu text vertical>
                {stats_options.seiyuu_list.map((item, index) => (
                    <Menu.Item key={item.id_name} data-seiyuu={item.id_name} active={statsOptionLocal.seiyuu_id_name === item.id_name} onClick={handleSelectSeiyuu}>{item.name}</Menu.Item>
                ))}
            </Menu>
            <Form>
                <h3>Data Interval</h3>
                <Form.Input
                    label="Start Date"
                    control="input"
                    type="date"
                    max={stats_options.end_date || undefined}
                    value={statsOptionLocal.start_date}
                    onChange={(e) => setStatsOptionLocal(prev => ({ ...prev, "start_date": e.target.value }))}
                />
                <Form.Input
                    label="End Date"
                    control="input"
                    type="date"
                    min={stats_options.start_date || prev_date_str}
                    value={statsOptionLocal.end_date}
                    onChange={(e) => setStatsOptionLocal(prev => ({ ...prev, "end_date": e.target.value }))}
                />
                <Button primary fluid onClick={handleApply}>Apply</Button>
                <h3>Interval Preset</h3>
                <Form.Field>
                    <Dropdown fluid className="icon" text="Select Preset" button labeled icon="wait">
                        <Dropdown.Menu>
                            {
                                stats_options.preset_dates.map((item, index) => (
                                    <Dropdown.Item key={index} onClick={() => handleSelectPreset(item.start_date, item.end_date)}>{item.name}</Dropdown.Item>
                                ))
                            }
                        </Dropdown.Menu>
                    </Dropdown>
                </Form.Field>
            </Form>
        </>
    )
}
StatsOptions.propTypes = {
    handleSideActive: PropTypes.func,
}

export { Stats, StatsOptions };