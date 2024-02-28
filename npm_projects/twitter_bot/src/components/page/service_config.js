import React, { useState, useEffect, useRef } from "react";
import { Accordion, Form, Icon, Divider, Segment, Table } from "semantic-ui-react";

import PropTypes from 'prop-types';
import Cookies from "js-cookie";

import store from "../../store";
import { useSelector } from "react-redux";
import { setSeiyuuList } from "../../store/stats_slice";

import { seiyuu_name } from "../App";
import { set } from "date-fns";
import { CompactContainer } from "../layout";

/**
 * A row of service config
 * @param {object} props - see prop
 * @prop {string} name - seiyuu name
 * @prop {string} screenName - twitter screen name
 * @prop {string} idName - seiyuu id name
 * @prop {boolean} active - is service active
 * @prop {number} interval - interval between posts
 * @returns 
 */
function ServiceConfig(props) {
    const [config, setConfig] = useState({
        "posts_interval": 0,
        "active": false
    });

    const [loading, setLoading] = useState(false);

    useEffect(() => {
        setConfig({
            "posts_interval": props.interval,
            "active": props.active
        });
    }, [props.active, props.posts_interval]);

    const interval_input_ref = useRef(null);

    function handleFocusInput() {
        if (interval_input_ref.current) {
            interval_input_ref.current.focus();
        }
    }

    function handleIntervalChange(e) {
        setConfig(prev => ({ ...prev, "posts_interval": parseInt(e.target.value) }));
    }

    function handleActiveChange() {
        setConfig(prev => ({ ...prev, "active": !prev.active }));
    }

    function handleApply() {
        setLoading(true);
        fetch(`/bot/api/config/update/${props.idName}/`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": Cookies.get("csrftoken")
            },
            body: JSON.stringify({
                "interval": config.posts_interval,
                "activated": config.active
            })
        }).then(res => {
            if (res.status === 200) {
                fetch("/bot/api/config/get/").then(res => {
                    if (res.status === 200) {
                        res.json().then(data => {
                            store.dispatch(setSeiyuuList(data.data));
                        });
                    }
                });
            }
            console.log(res.json());
            throw new Error("Failed to update config");
        }).catch(err => {
            console.error(err);
        }).finally(() => {
            setLoading(false);
        });
    }

    function handleReset() {
        setConfig({
            "posts_interval": props.interval,
            "active": props.active
        });
    }

    return (
        <Segment>
            <Form>
                <h3>{`${props.name} ${props.screenName}`}</h3>
                <Table basic="very">
                    <Table.Body>
                        <Table.Row style={{ cursor: "pointer" }} onClick={handleFocusInput}>
                            <Table.Cell collapsing>Posts Interval</Table.Cell>
                            <Table.Cell>
                                <Form.Field>
                                    <input ref={interval_input_ref} type="number" required value={config.posts_interval} min={1} max={24} onChange={handleIntervalChange} />
                                </Form.Field>
                            </Table.Cell>
                        </Table.Row>
                        <Table.Row onClick={handleActiveChange} style={{ cursor: "pointer" }}>
                            <Table.Cell collapsing>Activate</Table.Cell>
                            <Table.Cell>
                                <Form.Checkbox checked={config.active} name="active" toggle />
                            </Table.Cell>
                        </Table.Row>
                        <Table.Row >
                            <Table.Cell colSpan={2}>
                                <Form.Group>
                                    <Form.Button
                                        width={8}
                                        fluid
                                        color="teal"
                                        loading={loading}
                                        disabled={
                                            loading ||
                                            (config.posts_interval === props.interval && config.active === props.active)
                                        }
                                        onClick={handleApply}
                                    >Apply</Form.Button>
                                    <Form.Button
                                        width={8}
                                        fluid
                                        loading={loading}
                                        disabled={
                                            loading ||
                                            (config.posts_interval === props.interval && config.active === props.active)
                                        }
                                        onClick={handleReset}
                                    >Reset</Form.Button>
                                </Form.Group>
                            </Table.Cell>
                        </Table.Row>
                    </Table.Body>
                </Table>
            </Form>
        </Segment>
    )
}
ServiceConfig.propTypes = {
    name: PropTypes.string.isRequired,
    screenName: PropTypes.string.isRequired,
    idName: PropTypes.string.isRequired,
    active: PropTypes.bool.isRequired,
    interval: PropTypes.number.isRequired,
}

function ConfigPage() {

    const config = useSelector(state => state.StatsSlice.stats_options.seiyuu_list);

    return (
        <CompactContainer>
            {config.map((service, index) => {
                return (
                    <ServiceConfig key={service.id} idName={service.id_name} name={service.name} screenName={service.screen_name} active={service.activated} interval={service.interval} ></ServiceConfig>
                )
            })}
        </CompactContainer>
    )
}

export default ConfigPage;

