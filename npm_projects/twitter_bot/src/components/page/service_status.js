import React, { useState, useEffect } from "react";
import { Grid, Icon, Button, Label, Form, Segment, Table } from "semantic-ui-react";

import PropTypes from 'prop-types';

/**
 * 
 * @param {object} props see prop
 * @prop {string} title title of status block
 * @prop {boolean} active is service online
 * @prop {string} lastPostTime last post time
 * @prop {number} interval interval between posts
 * @returns 
 */
function StatusBlock(props) {

    const seiyuu_name = {
        "kaorin": "前田佳織里 kaorin__bot",
        "akarin": "鬼頭明里 akarin__bot",
        "chemi": "田中ちえ美 Chiemi__bot",
        "konachi": "月音こな konachi__bot"
    }

    return (
        <Segment>
            <h3>{seiyuu_name[props.title]}</h3>
            <Table celled basic="very">
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
                        <Table.Cell>{props.interval ? `${props.interval} hours` : "-"} </Table.Cell>
                    </Table.Row>
                </Table.Body>
            </Table>
        </Segment>
    )
}
StatusBlock.propTypes = {
    title: PropTypes.string.isRequired,
    active: PropTypes.bool.isRequired,
    lastPostTime: PropTypes.string,
    interval: PropTypes.number,
}

function StatusPage() {
    const [config, setConfig] = useState([]);

    useEffect(() => {
        fetch("/bot/api/config/get/").then(res => {
            if (res.status === 200 && res.status) {
                res.json().then(data => {
                    setConfig(data.data);
                });
            }
        })
    }, []);

    return (
        <>
            {config.map((service, index) => {
                return <StatusBlock key={index} title={service.seiyuu_id_name} active={service.is_active} lastPostTime={service.last_post_time} interval={service.interval}></StatusBlock>
            }
            )}
        </>
    )
}

export default StatusPage;
