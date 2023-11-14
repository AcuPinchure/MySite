import React from "react";
import { Grid, Icon, Button, Label, Form, Segment, Table } from "semantic-ui-react";

import PropTypes from 'prop-types';

/**
 * 
 * @param {object} props see prop
 * @prop {string} title title of status block
 * @prop {boolean} isOnline is service online
 * @prop {string} lastPost last post time
 * @prop {number} interval interval between posts
 * @returns 
 */
function StatusBlock(props) {
    return (
        <Segment>
            <h3>{props.title}</h3>
            <Table celled basic="very">
                <Table.Body>
                    <Table.Row>
                        <Table.Cell collapsing>Service Status</Table.Cell>
                        <Table.Cell>{props.isOnline ? <Label color="green"><Icon name="check"></Icon>Online</Label> : <Label color="red"><Icon name="x"></Icon>Offline</Label>}</Table.Cell>
                    </Table.Row>
                    <Table.Row>
                        <Table.Cell collapsing>Last Post</Table.Cell>
                        <Table.Cell>{props.lastPost ? props.lastPost : "-"}</Table.Cell>
                    </Table.Row>
                    <Table.Row>
                        <Table.Cell collapsing>Interval</Table.Cell>
                        <Table.Cell>{props.interval ? `${props.interval} hours` : "-"} </Table.Cell>
                    </Table.Row>
                </Table.Body>
            </Table>
        </Segment>
    )
}
StatusBlock.propTypes = {
    title: PropTypes.string.isRequired,
    isOnline: PropTypes.bool.isRequired,
    lastPost: PropTypes.string,
    interval: PropTypes.number,
}

function StatusPage(props) {
    return (
        <>
            <StatusBlock title="Kaorin" isOnline={true} lastPost="2021-08-10 12:00:00" interval={1}></StatusBlock>
            <StatusBlock title="Akarin" isOnline={true} lastPost="2021-08-10 12:00:00" interval={1}></StatusBlock>
            <StatusBlock title="Chemi" isOnline={true} lastPost="2021-08-10 12:00:00" interval={1}></StatusBlock>
            <StatusBlock title="Konachi" isOnline={false}></StatusBlock>
        </>
    )
}

export default StatusPage;
