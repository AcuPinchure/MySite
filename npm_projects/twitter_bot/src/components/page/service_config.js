import React, { useState, useEffect } from "react";
import { Accordion, Form, Icon, Divider } from "semantic-ui-react";

import PropTypes from 'prop-types';
import Cookies from "js-cookie";

import { seiyuu_name } from "../App";

/**
 * A row of service config
 * @param {object} props - see prop
 * @prop {string} title - title of service config
 * @prop {boolean} active - is service active
 * @prop {number} interval - interval between posts
 * @prop {function} handleApply - callback function when apply button is clicked
 * @returns 
 */
function ServiceConfig(props) {
    const [config, setConfig] = useState({
        "posts_interval": 0,
        "active": false
    });



    useEffect(() => {
        setConfig({
            "posts_interval": props.interval,
            "active": props.active
        });
    }, [props.active, props.posts_interval]);


    function handleIntervalChange(e) {
        setConfig({ ...config, "posts_interval": parseInt(e.target.value) });
    }

    function handleActiveChange(e) {
        setConfig({ ...config, "active": !config.active });
    }

    function handleApply() {
        fetch(`/bot/api/config/update/${props.title}/`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": Cookies.get("csrftoken")
            },
            body: JSON.stringify({
                "seiyuu_id_name": props.title,
                "interval": config.posts_interval,
                "is_active": config.active
            })
        }).then(res => {
            if (res.status === 200) {
                props.handleApply();
            }
        })
    }

    return (
        <>
            <h2>{seiyuu_name[props.title]}</h2>
            <Form>
                <Form.Group inline>
                    <Form.Input label="Posts Interval" control="input" type="number" value={config.posts_interval} min={1} max={24} onChange={handleIntervalChange} />
                    <Form.Checkbox label='Activate' checked={config.active} onChange={handleActiveChange} name="active" toggle />
                    {config.active === props.active && config.posts_interval === props.interval ? null : <Form.Button positive onClick={handleApply}>Apply</Form.Button>}
                </Form.Group>
            </Form>
            <Divider></Divider>
        </>
    )
}
ServiceConfig.propTypes = {
    title: PropTypes.string.isRequired,
    active: PropTypes.bool.isRequired,
    interval: PropTypes.number.isRequired,
    handleApply: PropTypes.func.isRequired
}

function ConfigPage(props) {
    const [config, setConfig] = useState([]);

    useEffect(() => {
        getConfig();
    }, []);

    function getConfig() {
        fetch("/bot/api/config/get/").then(res => {
            if (res.status === 200 && res.status) {
                res.json().then(data => {
                    setConfig(data.data);
                });
            }
        })
    }

    return (
        <>
            {config.map((service, index) => {
                return (
                    <ServiceConfig key={index} title={service.seiyuu_id_name} active={service.is_active} interval={service.interval} handleApply={getConfig}></ServiceConfig>
                )
            })}
        </>
    )
}

export default ConfigPage;

