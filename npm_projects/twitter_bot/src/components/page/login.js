import React, { useState, useEffect } from "react";
import { Form, Message, Container, Segment } from "semantic-ui-react";
import Cookies from "js-cookie";

function LoginForm(props) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [loginMessage, setLoginMessage] = useState(null);

    const csrf_token = Cookies.get("csrftoken");

    useEffect(() => {
        setLoginMessage(null);
    }, [username, password])

    function handleUsernameChange(e) {
        setUsername(e.target.value);
    }

    function handlePasswordChange(e) {
        setPassword(e.target.value);
    }


    function handleSubmit(e) {
        e.preventDefault();
        fetch('/bot/api/testLogin/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // 'X-CSRFToken': Cookies.get('csrftoken')
                'X-CSRFToken': csrf_token
            },
            body: JSON.stringify({ username, password })
        }).then(response => {
            console.log(response);
            if (response.status === 200) {
                e.target.submit();
            }
            else {
                setLoginMessage("Incorrect Username or Password");
            }
        })
    }

    return (
        <Form onSubmit={handleSubmit} method="post">
            <input type="hidden" name="csrfmiddlewaretoken" value={csrf_token} />
            <Form.Input icon="user" iconPosition='left' label="Username" name="username" value={username} onChange={handleUsernameChange} />
            <Form.Input icon="lock" iconPosition='left' label="Password" name="password" type="password" value={password} onChange={handlePasswordChange} />
            <Form.Button type="submit" fluid primary>Login</Form.Button>
            {loginMessage ?
                <Message negative>
                    <Message.Header>Login Failed</Message.Header>
                    <p>{loginMessage}</p>
                </Message>
                : null}
        </Form>
    )
}


function Login(props) {
    return (
        <div style={{ maxWidth: "32rem", margin: "auto", paddingTop: "20vh" }}>
            <h1 style={{ textAlign: "center" }}>Login as Admin to Continue</h1>
            <LoginForm setLoginStatus={props.setLoginStatus}></LoginForm>
        </div>
    )
}

export default Login;