import { set } from "date-fns";
import React, { useState, useEffect } from "react";
import { useSelector } from "react-redux";
import { Table, Button, Menu, Form, Card, Grid, Icon, Divider, Loader, Pagination, Message, Segment, Image, Modal, Dimmer } from "semantic-ui-react";
import store from "../../store";
import { setActiveTab, setFilterOptions, clearFilterOptions, setOrderOptions, setPageOptions, setQueryResults, setLibraryLoading } from "../../store/library_slice";

import PropTypes from 'prop-types';
import { setRightActive } from "../../store/layout_slice";
import Cookies from "js-cookie";

import "./library.css";



/**
 * 
 * @param {object} props see prop
 * @prop {number} id - id of the image
 * @prop {bool} open - control open state
 * @prop {function} setOpen - set open state
 * @returns 
 */
function ImageDetailModal(props) {

    const csrf_token = Cookies.get("csrftoken");

    const [loading, setLoading] = useState(false);
    const [weightLocal, setWeightLocal] = useState(0);
    const [imageData, setImageData] = useState({
        id: 0,
        file: "",
        file_type: "",
        file_name: "",
        seiyuu_name: "",
        seiyuu_screen_name: "",
        weight: 0,
        posts: 0,
        likes: 0,
        rts: 0,
        tweets: []
    });


    useEffect(() => {
        if (!props.open) return;

        reloadImage();

    }, [props.open]);

    function reloadImage() {
        setLoading(true);
        fetch(`/bot/api/image/get/${props.id}/`)
            .then(response => {
                if (response.ok) {
                    return response.json();
                }
                throw new Error("Network response was not ok.");
            })
            .then(data => {
                setImageData(data);
                setWeightLocal(data.weight);
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            })
            .finally(() => {
                setLoading(false);
            });
    }

    function handleUpdateWeight() {
        setLoading(true);
        fetch(`/bot/api/image/setWeight/${props.id}/`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrf_token
            },
            body: JSON.stringify({
                weight: weightLocal
            })
        })
            .then(response => {
                if (response.ok) {
                    reloadImage();
                }
                throw new Error("Network response was not ok.");
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            })
            .finally(() => {
                setLoading(false);
            });
    }

    function handleCancel() {
        setWeightLocal(imageData.weight);
    }

    return (
        <Modal
            open={props.open}
            onClose={() => props.setOpen(false)}
            onOpen={() => props.setOpen(true)}
        >
            <Modal.Header>Image Detail</Modal.Header>
            <Modal.Content image scrolling>
                {
                    imageData.file_type === "video/mp4"
                        ?
                        <Image as="video" size="medium" wrapped controls>
                            <source src={imageData.file.replace("data/media/", "")} type="video/mp4" />
                            Your browser does not support the video tag.
                        </Image>
                        :
                        <Image src={imageData.file.replace("data/media/", "")} wrapped size="medium" />
                }
                <Modal.Description>
                    <Table basic="very">
                        <Table.Body>
                            <Table.Row>
                                <Table.Cell collapsing>ID</Table.Cell>
                                <Table.Cell>{imageData.id}</Table.Cell>
                            </Table.Row>
                            <Table.Row>
                                <Table.Cell collapsing>File Name</Table.Cell>
                                <Table.Cell>{imageData.file_name}</Table.Cell>
                            </Table.Row>
                            <Table.Row>
                                <Table.Cell collapsing>File Type</Table.Cell>
                                <Table.Cell>{imageData.file_type}</Table.Cell>
                            </Table.Row>
                            <Table.Row>
                                <Table.Cell collapsing>Seiyuu</Table.Cell>
                                <Table.Cell>{imageData.seiyuu_name} {imageData.seiyuu_screen_name}</Table.Cell>
                            </Table.Row>
                            <Table.Row>
                                <Table.Cell collapsing>Total Posts</Table.Cell>
                                <Table.Cell>{imageData.posts}</Table.Cell>
                            </Table.Row>
                            <Table.Row>
                                <Table.Cell collapsing>Max Likes</Table.Cell>
                                <Table.Cell>{imageData.likes}</Table.Cell>
                            </Table.Row>
                            <Table.Row>
                                <Table.Cell collapsing>Max Retweets</Table.Cell>
                                <Table.Cell>{imageData.rts}</Table.Cell>
                            </Table.Row>
                        </Table.Body>
                    </Table>
                    <Form>
                        <Form.Group inline>
                            <Form.Input
                                label="Weight"
                                type="number"
                                value={weightLocal}
                                min="0"
                                max="100"
                                step="0.01"
                                onChange={(e, { value }) => setWeightLocal(value)}
                            />
                            Approximate Chance: {(parseFloat(weightLocal) / imageData.total_weight * 100).toFixed(4)}%
                        </Form.Group>
                        <Form.Group>
                            <Form.Button
                                width={8}
                                fluid
                                disabled={weightLocal == imageData.weight}
                                color="teal"
                                onClick={handleUpdateWeight}
                            >Save</Form.Button>
                            <Form.Button
                                width={8}
                                fluid
                                disabled={weightLocal == imageData.weight}
                                onClick={handleCancel}
                            >Cancel</Form.Button>
                        </Form.Group>
                    </Form>
                    <Divider />
                    <h3>Tweets</h3>
                    <div style={{ overflowX: "auto" }}>

                        <Table celled unstackable>
                            <Table.Header>
                                <Table.Row>
                                    <Table.HeaderCell>Index</Table.HeaderCell>
                                    <Table.HeaderCell>Tweet</Table.HeaderCell>
                                    <Table.HeaderCell>Likes</Table.HeaderCell>
                                    <Table.HeaderCell>Retweets</Table.HeaderCell>
                                    <Table.HeaderCell>Followers</Table.HeaderCell>
                                </Table.Row>
                            </Table.Header>
                            <Table.Body>
                                {
                                    imageData.tweets.map((tweet, index) => (
                                        <Table.Row key={tweet.id}>
                                            <Table.Cell>{index + 1}</Table.Cell>
                                            <Table.Cell>
                                                <a target="_blank" href={`https://twitter.com/_/status/${tweet.id}`}>{tweet.id}</a>
                                                <br />
                                                {new Date(tweet.post_time).toLocaleString()}
                                            </Table.Cell>
                                            <Table.Cell>{tweet.like}</Table.Cell>
                                            <Table.Cell>{tweet.rt}</Table.Cell>
                                            <Table.Cell>{tweet.followers}</Table.Cell>
                                        </Table.Row>
                                    ))
                                }
                            </Table.Body>
                        </Table>
                    </div>
                </Modal.Description>
                <Dimmer active={loading} inverted>
                    <Loader inverted>Loading</Loader>
                </Dimmer>
            </Modal.Content>
            <Modal.Actions>
                <Button onClick={() => props.setOpen(false)}>Close</Button>
            </Modal.Actions>
        </Modal>
    )
}
ImageDetailModal.propTypes = {
    id: PropTypes.number.isRequired,
    open: PropTypes.bool.isRequired,
    setOpen: PropTypes.func.isRequired
}


/**
 * 
 * @param {object} props see prop
 * @prop {number} id - id of the image
 * @prop {string} image - image file url
 * @prop {string} imageType - image file type
 * @prop {string} name - image file name
 * @prop {string} seiyuuName - seiyuu name
 * @prop {string} screenName - seiyuu screen name
 * @prop {number} posts - number of posts
 * @prop {number} likes - max likes
 * @prop {number} rts - max retweets
 * @returns 
 */
function ImageCard(props) {

    const [openModal, setOpenModal] = useState(false);

    return (
        <>
            <ImageDetailModal
                id={props.id}
                open={openModal}
                setOpen={setOpenModal}
            />
            <Card link onClick={() => setOpenModal(true)}>
                <div className="bot card-image-wrapper">
                    {
                        props.imageType === "video/mp4"
                            ?
                            <Image as="video" controls>
                                <source src={props.image.replace("data/media/", "")} type="video/mp4" />
                                Your browser does not support the video tag.
                            </Image>
                            :
                            <Image src={props.image.replace("data/media/", "")} ui={false} />
                    }
                </div>
                <Card.Content>
                    <Card.Header>
                        <p style={{ textOverflow: "ellipsis", overflow: "hidden" }}>{props.name}</p>
                    </Card.Header>
                    <Card.Meta>
                        {`${props.seiyuuName} ${props.screenName}`}
                        <br />
                        {props.imageType}
                    </Card.Meta>
                </Card.Content>
                <Card.Content extra>
                    <Grid columns={3} divided>
                        <Grid.Row>
                            <Grid.Column>
                                <Icon name="twitter"></Icon>
                                {props.posts}
                            </Grid.Column>
                            <Grid.Column>
                                <Icon name="heart"></Icon>
                                {props.likes}
                            </Grid.Column>
                            <Grid.Column>
                                <Icon name="retweet"></Icon>
                                {props.rts}
                            </Grid.Column>
                        </Grid.Row>
                    </Grid>
                </Card.Content>
            </Card>
        </>
    )
}
ImageCard.propTypes = {
    id: PropTypes.number.isRequired,
    image: PropTypes.string.isRequired,
    imageType: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
    seiyuuName: PropTypes.string.isRequired,
    screenName: PropTypes.string.isRequired,
    posts: PropTypes.number.isRequired,
    likes: PropTypes.number.isRequired,
    rts: PropTypes.number.isRequired
}

function ImageLibrary() {

    const query_results = useSelector(state => state.LibrarySlice.query_results);
    const display_options = useSelector(state => state.LibrarySlice.display_options);
    const search_data = useSelector(state => state.LibrarySlice.filter_options);
    const active_tab = useSelector(state => state.LibrarySlice.active_tab);

    const view_width = useSelector(state => state.LayoutSlice.view_width);
    const responsive_width = useSelector(state => state.LayoutSlice.responsive_width);

    function handlePageChange(e, { activePage }) {
        store.dispatch(setPageOptions({ page: activePage }));
        store.dispatch(setLibraryLoading(true));
    }

    function handleChangeOrder(sort_by) {
        if (display_options.sort_by === sort_by) {
            store.dispatch(setOrderOptions({ sort_by: sort_by, order: display_options.order === "asc" ? "desc" : "asc" }));
        }
        else {
            store.dispatch(setOrderOptions({ sort_by: sort_by, order: display_options.order }));
        }
        store.dispatch(setLibraryLoading(true));
    }

    useEffect(() => {
        if (!display_options.loading) return;

        store.dispatch(setQueryResults([]));
        const search_params = new URLSearchParams();
        if (active_tab === "tweet_id") {
            search_params.append("tweet_id", search_data.tweet_id);
        }
        else {
            for (const [key, value] of Object.entries(search_data)) {
                if (value && key !== "tweet_id") {
                    search_params.append(key, value);
                }
            }
        }

        search_params.append("page", display_options.page);
        search_params.append("sort_by", display_options.sort_by);
        search_params.append("order", display_options.order);

        fetch(`/bot/api/image/list/?${search_params.toString()}`)
            .then(response => {
                if (response.ok) {
                    return response.json();
                }
                throw new Error("Network response was not ok.");
            })
            .then(data => {
                store.dispatch(setPageOptions({
                    page: data.page,
                    total_pages: data.total_pages
                }));
                store.dispatch(setOrderOptions({
                    sort_by: data.sort_by,
                    order: data.order
                }));
                store.dispatch(setQueryResults(data.data));
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            })
            .finally(() => {
                store.dispatch(setLibraryLoading(false));
            });
    }, [display_options.loading, display_options.page]);

    return (
        <>
            {
                display_options.loading ?
                    <Loader active inline="centered" />
                    :
                    (
                        query_results.length > 0 ?
                            <>
                                <h2>Search Results</h2>
                                <Menu text vertical={view_width <= responsive_width} style={{ overflowX: "auto" }}>
                                    <Menu.Item header>Sort By</Menu.Item>
                                    {display_options.sort_options.map(option => (
                                        <Menu.Item
                                            key={option.key}
                                            active={display_options.sort_by === option.value}
                                            onClick={() => handleChangeOrder(option.value)}
                                        >
                                            {option.text}
                                            {
                                                display_options.sort_by === option.value
                                                &&
                                                <Icon name={display_options.order === "desc" ? "arrow down" : "arrow up"} />
                                            }
                                        </Menu.Item>
                                    ))}
                                </Menu>
                                {
                                    display_options.total_pages > 1
                                    &&
                                    <div style={{
                                        textAlign: view_width <= responsive_width ? "center" : "left",
                                        marginTop: "1rem",
                                        marginBottom: view_width <= responsive_width ? "2rem" : "1rem"
                                    }}>
                                        <Pagination
                                            size="mini"
                                            activePage={display_options.page}
                                            totalPages={display_options.total_pages}
                                            onPageChange={handlePageChange}
                                            firstItem={null}
                                            lastItem={null}
                                            boundaryRange={2}
                                            siblingRange={0}
                                        />
                                    </div>
                                }
                                <Card.Group itemsPerRow={3} stackable>
                                    {query_results.map(image => (
                                        <ImageCard
                                            key={image.id}
                                            id={image.id}
                                            image={image.file}
                                            imageType={image.file_type}
                                            name={image.file_name}
                                            seiyuuName={image.seiyuu_name}
                                            screenName={image.seiyuu_screen_name}
                                            posts={image.posts}
                                            likes={image.likes}
                                            rts={image.rts}
                                        />
                                    ))}
                                </Card.Group>
                                {
                                    display_options.total_pages > 1
                                    &&
                                    <div style={{
                                        textAlign: view_width <= responsive_width ? "center" : "left",
                                        marginTop: "1rem",
                                        marginBottom: "1rem"
                                    }}>
                                        <Pagination
                                            size="mini"
                                            activePage={display_options.page}
                                            totalPages={display_options.total_pages}
                                            onPageChange={handlePageChange}
                                            firstItem={null}
                                            lastItem={null}
                                            boundaryRange={2}
                                            siblingRange={0}
                                        />
                                    </div>
                                }

                            </>
                            :
                            <Message
                                icon="search"
                                header="No Results"
                                content="Current search returned no results. Please try again with different search parameters."
                            />
                    )

            }
        </>
    )
}


function extractTweetId(url) {
    const regex = /\/status\/(\d+)/;
    const match = url.match(regex);
    if (match) {
        return match[1];
    }
    return url;
}


function LibraryOptions() {

    const search_data = useSelector(state => state.LibrarySlice.filter_options);
    const active_tab = useSelector(state => state.LibrarySlice.active_tab);

    function handleChange(new_data) {
        store.dispatch(setFilterOptions(new_data));
    }

    function parseTweetId(tweet_id) {
        if (tweet_id) {
            const parsed_str = extractTweetId(tweet_id);
            handleChange({ tweet_id: parsed_str });
        }
    }

    function handleSearch() {
        store.dispatch(setLibraryLoading(true));
        store.dispatch(setRightActive(false));
    }

    const seiyuu_list = useSelector(state => state.StatsSlice.stats_options.seiyuu_list);

    const seiyuu_options = seiyuu_list.map(item => ({
        key: item.id,
        value: item.id_name,
        text: item.name
    }));

    const curr_date = new Date();
    const curr_date_str = `${curr_date.getFullYear()}-${curr_date.getMonth() + 1}-${curr_date.getDate()}`;

    return (
        <>
            <h3>Search By</h3>
            <Menu widths={2} size="small">
                <Menu.Item
                    active={active_tab === "filter"}
                    onClick={() => store.dispatch(setActiveTab("filter"))}
                >Filter</Menu.Item>
                <Menu.Item
                    active={active_tab === "tweet_id"}
                    onClick={() => store.dispatch(setActiveTab("tweet_id"))}
                >Tweet ID</Menu.Item>
            </Menu>
            {
                active_tab === "filter"
                &&
                <Form>
                    <Form.Select
                        fluid
                        label="Seiyuu"
                        value={search_data.seiyuu_id_name}
                        options={seiyuu_options}
                        onChange={(e, { value }) => handleChange({ seiyuu_id_name: value })}
                        placeholder="Select Seiyuu"
                    />
                    <Form.Input
                        label="Post Start Date"
                        type="date"
                        max={search_data.end_date || curr_date_str}
                        value={search_data.start_date}
                        onChange={(e, { value }) => handleChange({ start_date: value })}
                    />
                    <Form.Input
                        label="Post End Date"
                        type="date"
                        min={search_data.start_date || undefined}
                        max={curr_date_str}
                        value={search_data.end_date}
                        onChange={(e, { value }) => handleChange({ end_date: value })}
                    />
                    <Form.Input
                        label="Min Posts"
                        type="number"
                        min="0"
                        max={search_data.max_posts || undefined}
                        value={search_data.min_posts}
                        onChange={(e, { value }) => handleChange({ min_posts: value })}
                    />
                    <Form.Input
                        label="Max Posts"
                        type="number"
                        min={search_data.min_posts || "0"}
                        value={search_data.max_posts}
                        onChange={(e, { value }) => handleChange({ max_posts: value })}
                    />
                    <Form.Input
                        label="Min Likes"
                        type="number"
                        min="0"
                        max={search_data.max_likes || undefined}
                        value={search_data.min_likes}
                        onChange={(e, { value }) => handleChange({ min_likes: value })}
                    />
                    <Form.Input
                        label="Max Likes"
                        type="number"
                        min={search_data.min_likes || "0"}
                        value={search_data.max_likes}
                        onChange={(e, { value }) => handleChange({ max_likes: value })}
                    />
                    <Form.Input
                        label="Min Retweets"
                        type="number"
                        min="0"
                        max={search_data.max_rts || undefined}
                        value={search_data.min_rts}
                        onChange={(e, { value }) => handleChange({ min_rts: value })}
                    />
                    <Form.Input
                        label="Max Retweets"
                        type="number"
                        min={search_data.min_rts || "0"}
                        value={search_data.max_rts}
                        onChange={(e, { value }) => handleChange({ max_rts: value })}
                    />
                    <Button fluid onClick={() => store.dispatch(clearFilterOptions())}>Clear Filter</Button>
                    <Divider />
                    <Button color="teal" fluid onClick={handleSearch}>Search</Button>
                </Form>
            }
            {
                active_tab === "tweet_id"
                &&
                <Form>
                    <Form.Input
                        label="Tweet ID"
                        type="text"
                        value={search_data.tweet_id}
                        placeholder="Enter Tweet ID or URL"
                        onChange={(e, { value }) => parseTweetId(value)}
                    />
                    <Button color="teal" fluid onClick={handleSearch}>Search</Button>
                </Form>
            }

        </>
    )
}

export { ImageLibrary, LibraryOptions };