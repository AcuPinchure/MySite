import React, { useState, useEffect } from "react";
import { Accordion, Form, Icon, Divider } from "semantic-ui-react";

function ServiceConfig(props) {
    const [config, setConfig] = useState({
        "posts_interval": 1,
        "active": true
    });


    function handleConfigChange(e, { name, value, checked }) {
        if (name === "posts_interval") {
            setConfig({ ...config, "posts_interval": value });
        } else if (name === "active") {
            setConfig({ ...config, "active": checked });
        }
    }

    return (
        <>
            <h2>{props.title}</h2>
            <Form>
                <Form.Group inline>
                    <Form.Input label="Posts Interval" control="input" type="number" value={config.posts_interval} min={1} max={24} name="posts_interval" onChange={handleConfigChange} />
                    <Form.Checkbox label='Activate' checked={config.active} onChange={handleConfigChange} name="active" toggle />
                </Form.Group>
            </Form>
            <Divider></Divider>
        </>
    )
}

function ConfigPage(props) {
    return (
        <>
            <ServiceConfig title="Kaorin"></ServiceConfig>
            <ServiceConfig title="Akarin"></ServiceConfig>
            <ServiceConfig title="Chemi"></ServiceConfig>
            <ServiceConfig title="Konachi"></ServiceConfig>
        </>
    )
}

export default ConfigPage;

