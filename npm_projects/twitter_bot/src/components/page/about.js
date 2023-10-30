import BotLogo from "../../assets/bot_logo.svg";
import BotLogoL from "../../assets/bot_L_logo.svg";
import KaorinLink from "../../assets/Kaorin_Link.jpg";
import AkarinLink from "../../assets/Akarin_Link.jpg";
import ChemiLink from "../../assets/Chemi_Link.jpg";
import KonachiLink from "../../assets/Konachi_Link.jpg";

import React, { useState, useEffect } from "react";
import { useHistory } from "react-router-dom";
import "./about.css"
import { Grid, Image, Menu, Segment, Divider } from "semantic-ui-react";

function TopMenu(props) {
    const history = useHistory();
    return (
        <Menu text inverted={props.inverted} fixed="top" size="large" className={`bot about navi_menu ${props.inverted ? "" : "show"}`}>
            <Menu.Item header>
                <Image size="mini" src={BotLogoL} style={{ height: "1rem" }} />
            </Menu.Item>
            <Menu.Item onClick={() => history.push("/stats")}>Statistics</Menu.Item>
            <Menu.Item onClick={() => history.push("/config")}>Admin</Menu.Item>
        </Menu>
    )
}

function HeaderBanner(props) {
    return (
        <div className="bot about header">
            {props.children}
        </div>
    )
}

function FeatureSection(props) {
    return (
        <Grid.Row verticalAlign="middle" className="bot about feature section">
            {props.imageSide === "left" ? <Grid.Column width={6} textAlign="right">
                <Image size="small" centered src={props.image ? props.image : BotLogoL}></Image>
            </Grid.Column> : null}
            <Grid.Column width={10}>
                {props.children}
            </Grid.Column>
            {props.imageSide === "right" ? <Grid.Column width={6} textAlign="left">
                <Image size="small" centered src={props.image ? props.image : BotLogoL}></Image>
            </Grid.Column> : null}
        </Grid.Row>
    )
}

function TwitterLink(props) {
    return (
        <a href={props.link} target="_blank" rel="noreferrer" className="bot about twitter_link">
            <Image centered circular size="small" src={props.image}></Image>
            <h3>{props.name}</h3>
        </a>
    )
}

function Footer(props) {
    return (
        <div basic inverted className="bot about footer">
            <p className="bot about feature title">Stay Tuned</p>
            <p className="bot about feature description">
                Our service currently owns 4 bot accounts, check them out right now.
            </p>
            <Grid doubling columns={4} stackable>
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
        </div>
    )
}

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
            <Segment basic padded="very">
                <Grid stackable>
                    <FeatureSection imageSide="left">
                        <p className="bot about feature title">Discover Random Surprise</p>
                        <p className="bot about feature description">
                            Our bot randomly picks images of your favorite seiyuu and posts them on twitter. You'll never miss that perfect profile pic, moments or meme!
                        </p>
                    </FeatureSection>
                    <Divider></Divider>
                    <FeatureSection imageSide="right">
                        <p className="bot about feature title">Reminisce, <br />as well as Stay up-to-date</p>
                        <p className="bot about feature description">
                            While we continuously update our libraries with new images, we also retain those special older gems. That way you can rediscover and enjoy your favorites' gorgeous moments from years past that should never be forgotten.
                        </p>
                    </FeatureSection>
                    <Divider></Divider>
                    <FeatureSection imageSide="left">
                        <p className="bot about feature title">Scheduled, hourly Joy</p>
                        <p className="bot about feature description">
                            With new images posted hourly*, you'll get a regular dose of joy when your favorite seiyuu pops up in your feed. It's a great way to stay connected to your “oshi”!
                        </p>
                    </FeatureSection>
                    <Divider></Divider>
                    <FeatureSection imageSide="right">
                        <p className="bot about feature title">Kawaii, Gorgeous, in Motion!!</p>
                        <p className="bot about feature description">
                            Our libraries include not only static images, but also delightful gifs and short video clips capturing moments of your favorites. See their personalities and emotions shine through these dynamic slices of life!
                        </p>
                    </FeatureSection>
                    <Divider></Divider>
                    <FeatureSection imageSide="left">
                        <p className="bot about feature title">Data-Driven Curation</p>
                        <p className="bot about feature description">
                            We analyze the popularity of each post to learn what images resonate most with fans. This means our libraries continuously improve to feature your favorites.
                        </p>
                    </FeatureSection>
                    <Divider></Divider>
                    <FeatureSection imageSide="right">
                        <p className="bot about feature title">Purely for friends</p>
                        <p className="bot about feature description">
                            Our bot is designed solely to benefit fans. You'll never see ads or sponsored posts - just great images.
                        </p>
                    </FeatureSection>
                </Grid>
            </Segment>

            <Footer></Footer>
        </>
    )
}

export default About;