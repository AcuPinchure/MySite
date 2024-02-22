import { createSlice } from "@reduxjs/toolkit";

const StatsSlice = createSlice({
    name: "StatsSlice",
    initialState: {
        stats_options: {
            seiyuu_id_name: "",
            start_date: "",
            end_date: "",
            /**
             *  seiyuu_list: [
             *      {
             *          "id": 2,
             *          "name": "前田佳織里",
             *          "id_name": "kaorin",
             *          "screen_name": "kaorin__bot",
             *          "interval": 1,
             *          "activated": true,
             *          "last_post_time": "2024-02-11 14:20:09"
             *      }
             *  ]
             */
            seiyuu_list: [],
            preset_dates: [
                {
                    name: "Last 7 days",
                    start_date: `${new Date(new Date().setDate(new Date().getDate() - 7)).toISOString().split("T")[0]}`,
                    end_date: `${new Date().toISOString().split("T")[0]}`,
                },
                {
                    name: "Last 30 days",
                    start_date: `${new Date(new Date().setDate(new Date().getDate() - 30)).toISOString().split("T")[0]}`,
                    end_date: `${new Date().toISOString().split("T")[0]}`,
                },
                {
                    name: "Last 365 days",
                    start_date: `${new Date(new Date().setDate(new Date().getDate() - 365)).toISOString().split("T")[0]}`,
                    end_date: `${new Date().toISOString().split("T")[0]}`,
                },
                {
                    name: "All time",
                    start_date: "2021-01-01",
                    end_date: `${new Date().toISOString().split("T")[0]}`,
                }
            ],
        },
        summary: {
            seiyuu_name: "",
            seiyuu_id: "",
            start_date: "",
            end_date: "",
            interval: 0,
            posts: 0,
            likes: 0,
            rts: 0
        },
        /**
         * followers: {
         *  data_time: "",
         *  followers: 0
         * }
         */
        followers: [],
        posts_detail: {
            "start_date": "",
            "end_date": "",
            "interval": "",
            "posts": "",
            "scheduled_interval": 0,
            "actual_interval": 0,
            "is_active": false,
        },
        likes_detail: {
            "start_date": "",
            "end_date": "",
            "likes": 0,
            "avg_likes": 0,
            /**
             * max_likes: "id"
             */
            "max_likes": []
        },
        rts_detail: {
            "start_date": "",
            "end_date": "",
            "rts": 0,
            "avg_rts": 0,
            /**
             * max_rts: "id"
             */
            "max_rts": [],
        },
    },
    reducers: {
        setStatsOption: (state, action) => {
            state.stats_options = {
                ...state.stats_options,
                seiyuu_id_name: action.payload.seiyuu_id_name || "",
                start_date: action.payload.start_date || "",
                end_date: action.payload.end_date || "",
            };
        },
        setSeiyuuList: (state, action) => {
            state.stats_options.seiyuu_list = action.payload.map(seiyuu => ({
                id: seiyuu.id,
                name: seiyuu.name,
                id_name: seiyuu.id_name,
                screen_name: seiyuu.screen_name,
                interval: seiyuu.interval,
                activated: seiyuu.activated,
                last_post_time: seiyuu.last_post_time,
            }));
        },
        setSummary: (state, action) => {
            state.summary = action.payload;
        },
        setFollowers: (state, action) => {
            state.followers = action.payload;
        },
        setPostsDetail: (state, action) => {
            state.posts_detail = action.payload;
        },
        setLikesDetail: (state, action) => {
            state.likes_detail = action.payload;
        },
        setRtsDetail: (state, action) => {
            state.rts_detail = action.payload;
        },
    },
});


export const { setStatsOption, setPostsDetail, setLikesDetail, setRtsDetail, setSummary, setFollowers, setSeiyuuList } = StatsSlice.actions;

export default StatsSlice.reducer;