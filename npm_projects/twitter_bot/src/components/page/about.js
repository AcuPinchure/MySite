import BotLogo from "../../assets/bot_logo.svg";
import BotLogoL from "../../assets/bot_L_logo.svg";
import KaorinLink from "../../assets/Kaorin_Link.jpg";
import AkarinLink from "../../assets/Akarin_Link.jpg";
import ChemiLink from "../../assets/Chemi_Link.jpg";
import KonachiLink from "../../assets/Konachi_Link.jpg";

import Slide1 from "../../assets/about_images/slide_1.jpg";
import Slide2 from "../../assets/about_images/slide_2.jpg";
import Slide3 from "../../assets/about_images/slide_3.jpg";
import Slide4 from "../../assets/about_images/slide_4.jpg";
import Motion from "../../assets/about_images/motion.gif";
import Library from "../../assets/about_images/library.png";
import TweetDemo from "../../assets/about_images/tweet_demo.png";
import StatsDemo from "../../assets/about_images/stats.jpeg";

import React, { useState, useEffect } from "react";
import { useHistory } from "react-router-dom";
import "./about.css"
import { Grid, Image, Menu, Segment, Divider, Modal, Button, List, Table, Icon } from "semantic-ui-react";


/**
 * An image slider that shows the example images
 * @param {object} props see prop
 * @prop {array} images - The array of image urls
 * @prop {integer} interval - The interval between each image in seconds
 */
function ImageSlider(props) {
    const [currentImageIndex, setCurrentImageIndex] = useState(0);

    useEffect(() => {
        const interval = setInterval(() => {
            if (currentImageIndex < props.images.length - 1) {
                setCurrentImageIndex(currentImageIndex + 1);
            } else {
                setCurrentImageIndex(0);
            }
        }, props.interval * 1000);

        return () => clearInterval(interval);
    }, [currentImageIndex, props.images, props.interval]);


    return (
        <div className="bot about image_slider">
            {props.images.map((image, index) => {
                return (
                    <Image centered src={image} className={index === currentImageIndex ? "" : "vanish"} key={index} />
                )
            })}
        </div>
    )
}


/**
 * The menu bar at the top of the page
 * @param {object} props see prop
 * @prop {boolean} inverted - Whether the menu bar color is inverted or not
 * @returns JSX
 */
function TopMenu(props) {
    const history = useHistory();
    return (
        <Menu text inverted={props.inverted} fixed="top" size="huge" className={`bot about navi_menu ${props.inverted ? "" : "show"}`}>
            <Menu.Item header>
                <Image size="mini" src={BotLogoL} style={{ height: "1.5rem" }} />
            </Menu.Item>
            <Menu.Item onClick={() => { window.location = "/bot/stats/" }}>Statistics</Menu.Item>
            <Menu.Item onClick={() => { window.location = "/bot/login/" }}>Admin</Menu.Item>
        </Menu>

    )
}

/**
 * The banner at the top of the page, with LOGO and subtitle
 * @param {object} props see prop
 * @prop {JSX} children - The content of the banner
 * @returns JSX
 */
function HeaderBanner(props) {
    return (
        <div className="bot about header">
            {props.children}
        </div>
    )
}

/**
 * The modal that shows the detail description of a feature
 * @param {object} props see prop
 * @prop {JSX} triggerText - The text that triggers the modal
 * @prop {string} title - The title of the modal
 * @prop {JSX} children - The content of the modal
 * @returns JSX
 */
function FeatureDetailModal(props) {
    const [open, setOpen] = useState(false);
    return (
        <Modal
            trigger={<a style={{ cursor: "pointer" }}>{props.triggerText}</a>}
            open={open}
            onClose={() => setOpen(false)}
            onOpen={() => setOpen(true)}
        >
            <Modal.Header>{props.title}</Modal.Header>
            <Modal.Content>
                {props.children}
            </Modal.Content>
            <Modal.Actions>
                <Button onClick={() => setOpen(false)}>Close</Button>
            </Modal.Actions>
        </Modal>
    )
}


/**
 * The section that describes a feature
 * @param {object} props see prop
 * @prop {string} imageSide - The side of the image, either "left" or "right"
 * @prop {JSX} image - The image of the feature
 * @prop {JSX} children - The content of the feature
 * @returns JSX
 */
function FeatureSection(props) {
    return (
        <Grid.Row verticalAlign="middle" className="bot about feature section">
            {props.imageSide === "right" ? <Grid.Column width={10} textAlign="right">
                {props.children}
            </Grid.Column> : null}
            <Grid.Column width={6} textAlign="center">
                {props.image ? props.image : <Image src={BotLogoL} size="small" centered />}
            </Grid.Column>
            {props.imageSide === "left" ? <Grid.Column width={10} textAlign="left">
                {props.children}
            </Grid.Column> : null}

        </Grid.Row>
    )
}

/**
 * The link to a bot's twitter account
 * @param {object} props see prop
 * @prop {string} name - The name of the bot
 * @prop {string} image - The image of the bot
 * @returns JSX
 */
function TwitterLink(props) {
    return (
        <a href={props.link} target="_blank" rel="noreferrer" className="bot about twitter_link">
            <Image centered circular size="small" src={props.image}></Image>
            <h3>{props.name}</h3>
        </a>
    )
}

/**
 * The footer of the page
 * @returns JSX
 */
function Footer() {
    return (
        <div className="bot about footer">
            <p className="bot about feature title">Stay Tuned</p>
            <p className="bot about feature description">
                Our service currently owns 4 accounts, click the avatar to view them on Twitter.
            </p>
            <Grid doubling columns={4} stackable className="bot about twitter_link_group">
                <Grid.Column>
                    <TwitterLink name="前田佳織里" image={KaorinLink} link="https://twitter.com/kaorin__bot"></TwitterLink>
                </Grid.Column>
                <Grid.Column>
                    <TwitterLink name="鬼頭明里" image={AkarinLink} link="https://twitter.com/akarin__bot"></TwitterLink>
                </Grid.Column>
                <Grid.Column>
                    <TwitterLink name="田中ちえ美" image={ChemiLink} link="https://twitter.com/chiemi__bot"></TwitterLink>
                </Grid.Column>
                <Grid.Column>
                    <TwitterLink name="月音こな" image={KonachiLink} link="https://twitter.com/konachi__bot"></TwitterLink>
                </Grid.Column>
            </Grid>
            <div className="bot about footer_bottom">
                <p>
                    © 2020 Lovelive Seiyuu Bot Project | create by AcuPinchure
                </p>
                <p>

                    <a href="https://github.com/AcuPinchure/MySite">
                        <Icon name="github"></Icon>
                        view source code
                    </a>
                </p>
            </div>
        </div>
    )
}

/**
 * The about page
 * @returns JSX
 */
function About() {
    const [viewWidth, setViewWidth] = useState(window.innerWidth);
    const [scrollDistance, setScrollDistance] = useState(0);

    useEffect(() => {
        function updateScrollDistance() {
            const scrollTop = window.scrollY;

            // Set the scroll distance state
            setScrollDistance(scrollTop);
        };

        function updateViewWidth() {
            setViewWidth(window.innerWidth);
        }

        // Attach the event listener to update viewWidth when the window is resized
        window.addEventListener('resize', updateViewWidth);
        // Attach the scroll event listener
        window.addEventListener('scroll', updateScrollDistance);

        // Clean up the event listener when the component unmounts
        return () => {
            window.removeEventListener('resize', updateViewWidth);
            window.removeEventListener('scroll', updateViewWidth);
        };
    }, []);

    return (
        <>
            <TopMenu inverted={scrollDistance < 200}></TopMenu>
            <HeaderBanner>
                <img src={BotLogo} alt="Bot Logo" className="bot about site_title"></img>
                <p className="bot about site_subtitle">We gather the gems, {viewWidth <= 768 ? <br></br> : null}so you don’t have to dig.</p>
            </HeaderBanner>
            <Segment basic style={{ padding: viewWidth > 768 ? "3rem" : "0.2rem" }}>
                <Grid stackable>
                    <FeatureSection imageSide="left" image={<ImageSlider images={[Slide1, Slide2, Slide3, Slide4]} interval={2}></ImageSlider>}>
                        <p className="bot about feature title">Discover Random Surprise</p>
                        <p className="bot about feature description">
                            Our bot randomly picks images of your favorite seiyuu and posts them on twitter. You'll never miss that perfect profile pic, moments or meme!
                        </p>
                        <FeatureDetailModal triggerText="Learn more about how we collect images" title="How do we collect images?">
                            <p>All images and clips are collected from the following source.</p>
                            <List bulleted>
                                <List.Item>Social media such as Twitter, Instagram, YouTube, etc.</List.Item>
                                <List.Item>News websites</List.Item>
                                <List.Item>Official websites</List.Item>
                                <List.Item>Other public source</List.Item>
                            </List>
                            <p>The media from the following source will not be included.</p>
                            <List bulleted>
                                <List.Item>Fan clubs</List.Item>
                                <List.Item>Magazine or photobook scans</List.Item>
                                <List.Item>Live concert streaming service</List.Item>
                                <List.Item>Live concert BD</List.Item>
                                <List.Item>Other paid source</List.Item>
                                <List.Item>Anything marked as redistribution prohibited</List.Item>
                            </List>
                        </FeatureDetailModal>
                    </FeatureSection>
                    <Divider></Divider>
                    <FeatureSection imageSide="right" image={<Image src={Library} style={{ width: "30rem" }} centered></Image>}>
                        <p className="bot about feature title">Reminisce<br /><span style={{ fontWeight: "normal" }}>as well as</span><br />Stay up-to-date</p>
                        <p className="bot about feature description">
                            While we continuously update with new images, older gems still remain. You always have chances to rediscover those gorgeous moments years later.
                        </p>
                    </FeatureSection>
                    <Divider></Divider>
                    <FeatureSection imageSide="left" image={<Image src={TweetDemo} style={{ height: "30rem" }} centered></Image>}>
                        <p className="bot about feature title">Scheduled, hourly Joy</p>
                        <p className="bot about feature description">
                            You'll get a regular dose of joy when your favorite seiyuu pops up in your feed. It's a great way to stay connected to your “oshi”!
                        </p>
                        <FeatureDetailModal triggerText="See posts interval of each account" title="Service status">
                            <Table basic="very" celled>
                                <Table.Header>
                                    <Table.Row>
                                        <Table.HeaderCell>Account</Table.HeaderCell>
                                        <Table.HeaderCell>Status</Table.HeaderCell>
                                        <Table.HeaderCell>Interval</Table.HeaderCell>
                                    </Table.Row>
                                </Table.Header>
                                <Table.Body>
                                    <Table.Row>
                                        <Table.Cell>前田佳織里</Table.Cell>
                                        <Table.Cell>
                                            <Icon name="check" color="green"></Icon>
                                            Online
                                        </Table.Cell>
                                        <Table.Cell>1 hour</Table.Cell>
                                    </Table.Row>
                                    <Table.Row>
                                        <Table.Cell>鬼頭明里</Table.Cell>
                                        <Table.Cell>
                                            <Icon name="check" color="green"></Icon>
                                            Online
                                        </Table.Cell>
                                        <Table.Cell>1 hour</Table.Cell>
                                    </Table.Row>
                                    <Table.Row>
                                        <Table.Cell>田中ちえ美</Table.Cell>
                                        <Table.Cell>
                                            <Icon name="check" color="green"></Icon>
                                            Online
                                        </Table.Cell>
                                        <Table.Cell>1 hour</Table.Cell>
                                    </Table.Row>
                                    <Table.Row>
                                        <Table.Cell>月音こな</Table.Cell>
                                        <Table.Cell>
                                            <Icon name="x" color="red"></Icon>
                                            Offline
                                        </Table.Cell>
                                        <Table.Cell>-</Table.Cell>
                                    </Table.Row>
                                </Table.Body>
                            </Table>
                        </FeatureDetailModal>
                    </FeatureSection>
                    <Divider></Divider>
                    <FeatureSection imageSide="right" image={<Image src={Motion} style={{ width: "30rem" }} centered></Image>}>
                        <p className="bot about feature title">Sometimes in Motion!!</p>
                        <p className="bot about feature description">
                            Our libraries include not only static images, but also short clips as well. See their personalities and emotions shine through these dynamic slices of life!
                        </p>

                    </FeatureSection>
                    <Divider></Divider>
                    <FeatureSection imageSide="left" image={<Image src={StatsDemo} style={{ width: "30rem" }} centered></Image>}>
                        <p className="bot about feature title">Data-Driven Curation</p>
                        <p className="bot about feature description">
                            We analyze the popularity of each post to learn what images resonate most with fans. This means our libraries continuously improve to feature your favorites.
                        </p>
                        <FeatureDetailModal triggerText="See how we collect data" title="What data do we collect?">
                            <p>In order to better understand the popularity of the posted images or clips, the bot records the following data from each tweet 72 hours after posting. No personal information from any account will be collected.</p>
                            <List bulleted>
                                <List.Item>The number of likes</List.Item>
                                <List.Item>The number of retweets (including quotes)</List.Item>
                                <List.Item>The number of followers of the account</List.Item>
                            </List>
                            <p>You can see the statistics of each account in <a href="/bot/stats/">the statistics page</a>.</p>
                        </FeatureDetailModal>
                    </FeatureSection>
                    <Divider></Divider>
                    <FeatureSection imageSide="right">
                        <p className="bot about feature title">Purely for friends</p>
                        <p className="bot about feature description">
                            Our bot is designed solely to benefit fans. You'll never see ads or sponsored posts - just great images.
                        </p>
                    </FeatureSection>
                </Grid>
            </Segment >

            <Footer></Footer>
        </>
    )
}

export default About;