import React, { useState, useEffect } from "react";
import { Grid, Icon, Button, Label, Form, Segment, Table } from "semantic-ui-react";

import PropTypes from 'prop-types';

import store from "../../store";
import { useSelector } from "react-redux";
import { CompactContainer } from "../layout";

/**
 * 
 * @param {object} props see prop
 * @prop {string} name service name
 * @prop {string} screenName twitter screen name
 * @prop {boolean} active is service online
 * @prop {string} lastPostTime last post time
 * @prop {number} interval interval between posts
 * @returns 
 */
function StatusBlock(props) {

    return (
        <Segment>
            <h3>
                {`${props.name} ${props.screenName}`}
                {
                    props.active &&
                    <a href={`https://twitter.com/${props.screenName}`} target="__blank" style={{ color: "grey", marginLeft: "1rem" }}>
                        <Icon name="external alternate"></Icon>
                    </a>
                }

            </h3>
            <Table basic="very">
                <Table.Body>
                    <Table.Row>
                        <Table.Cell collapsing>Service Status</Table.Cell>
                        <Table.Cell>{props.active ? <Label color="green"><Icon name="check"></Icon>Online</Label> : <Label color="red"><Icon name="x"></Icon>Offline</Label>}</Table.Cell>
                    </Table.Row>
                    <Table.Row>
                        <Table.Cell collapsing>Last Post</Table.Cell>
                        <Table.Cell>{props.lastPostTime ? props.lastPostTime : "-"}</Table.Cell>
                    </Table.Row>
                    <Table.Row>
                        <Table.Cell collapsing>Interval</Table.Cell>
                        <Table.Cell>{props.interval && props.active ? `${props.interval} hours` : "-"} </Table.Cell>
                    </Table.Row>
                </Table.Body>
            </Table>
        </Segment>
    )
}
StatusBlock.propTypes = {
    name: PropTypes.string.isRequired,
    screenName: PropTypes.string.isRequired,
    active: PropTypes.bool.isRequired,
    lastPostTime: PropTypes.string,
    interval: PropTypes.number,
}

function StatusPage() {

    const config = useSelector(state => state.StatsSlice.stats_options.seiyuu_list);

    return (
        <>
            {config.map((service) => {
                return <StatusBlock key={service.id} name={service.name} screenName={service.screen_name} active={service.activated} lastPostTime={service.last_post_time} interval={service.interval}></StatusBlock>
            }
            )}
        </>
    )
}

export default StatusPage;
