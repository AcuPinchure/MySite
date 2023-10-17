import { useEffect, useState } from "react";
import { Segment, Statistic, Icon, Grid } from "semantic-ui-react";


function StatsBlock(props) {
    // props: size<int:1-3>, title<str>, iconName<str>, value<str>, subinfo<str>, loading<bool>
    return (
        <Grid.Column width={props.size}>
            <Segment loading={props.loading}>
                <h3>
                    <Icon name={props.iconName} />
                    {props.title}
                </h3>
                <Statistic>
                    <Statistic.Value>{props.value}</Statistic.Value>
                </Statistic>
                <div className="bot stats subinfo">
                    {props.subinfo}
                </div>
            </Segment>
        </Grid.Column>
    )
}


function Stats(props) {
    // props: seiyuu<str:"kaorin","akarin","chemi">, startDate<str:"YYYY-MM-DD">, endDate<str:"YYYY-MM-DD">
    const [stats, setStats] = useState({
        "seiyuu_name": "前田佳織里",
        "seiyuu_id": "@kaorin__bot",
        "start_date": "2023-06-01 00:00",
        "end_date": "2023-07-01 23:59",
        "interval": 223, // hours
        "posts": 223,
        "likes": 3425,
        "rts": 302,
        "top_likes": [
            {

            }
        ],
        "top_rts": [],
        "followers": [
            {
                "date": "2023-06-01 00:00:05",
                "followers": 2350
            }
        ]
    });

    const [loading, setLoading] = useState(true);

    return (
        <>  
            <h1>{stats.seiyuu_name + " " + stats.seiyuu_id}</h1>
            <Grid columns={3} stackable>
                <StatsBlock loading={loading} size={1} title="Posts" iconName="file alternate" value={stats.posts} subinfo="Posts in the given time period"></StatsBlock>
            </Grid>
        </>
    )
}

export default Stats;