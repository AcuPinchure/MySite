import React, { useState, useEffect } from "react";
import { Table, Button, Menu, Form } from "semantic-ui-react";

function ImageLibrary() {
    const [images, setImages] = useState([
        {
            "name": "image1.jpg",
            "type": "jpg",
            "posts": 1,
            "weight": 1
        },
    ]);

    return (
        <Table celled>
            <Table.Header>
                <Table.Row>
                    <Table.HeaderCell>Image File Name</Table.HeaderCell>
                    <Table.HeaderCell>Type</Table.HeaderCell>
                    <Table.HeaderCell>Number of Posts</Table.HeaderCell>
                    <Table.HeaderCell>Weight</Table.HeaderCell>
                    <Table.HeaderCell>Actions</Table.HeaderCell>
                </Table.Row>
            </Table.Header>
            <Table.Body>
                {images.map((image, index) => {
                    return (
                        <Table.Row key={index}>
                            <Table.Cell>{image.name}</Table.Cell>
                            <Table.Cell>{image.type}</Table.Cell>
                            <Table.Cell>{image.posts}</Table.Cell>
                            <Table.Cell>{image.weight}</Table.Cell>
                            <Table.Cell>
                                <Button.Group>
                                    <Button icon="edit"></Button>
                                </Button.Group>
                            </Table.Cell>
                        </Table.Row>
                    )
                })}
            </Table.Body>
        </Table>
    )
}


function LibraryOptions(props) {
    const [postID, setPostID] = useState(null);
    const [selectSeiyuu, setSelectSeiyuu] = useState(null);
    function handleSelectSeiyuu(e) {
        setSelectSeiyuu(e.target.getAttribute("data-seiyuu"));
    }


    return (
        <>
            <h3>Account</h3>
            <Menu text vertical>
                <Menu.Item data-seiyuu="kaorin" active={selectSeiyuu === "kaorin"} onClick={handleSelectSeiyuu}>前田佳織里</Menu.Item>
                <Menu.Item data-seiyuu="chemi" active={selectSeiyuu === "chemi"} onClick={handleSelectSeiyuu}>田中ちえ美</Menu.Item>
                <Menu.Item data-seiyuu="akarin" active={selectSeiyuu === "akarin"} onClick={handleSelectSeiyuu}>鬼頭明里</Menu.Item>
                <Menu.Item data-seiyuu="konachi" active={selectSeiyuu === "konachi"} onClick={handleSelectSeiyuu}>月音こな</Menu.Item>
            </Menu>
            <h3>Find by Post ID</h3>
            <Form>
                <Form.Input label="Post ID" type="text" value={postID} onChange={({ value }) => setPostID(value)}></Form.Input>
                <Form.Field>
                    <Button fluid>Find Image</Button>
                </Form.Field>
            </Form>
        </>
    )
}

export { ImageLibrary, LibraryOptions };