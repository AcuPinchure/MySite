import { createSlice } from "@reduxjs/toolkit";

const LibrarySlice = createSlice({
    name: "LibrarySlice",
    initialState: {
        active_tab: "filter",
        filter_options: {
            seiyuu_id_name: "",
            start_date: "", // post date
            end_date: "", // post date
            min_likes: "",
            max_likes: "",
            min_rts: "",
            max_rts: "",
            min_posts: "",
            max_posts: "",
            tweet_id: ""
        },
        display_options: {
            loading: false,
            sort_by: "latest_post_time",
            order: "desc",
            page: 1,
            total_pages: 1,
            sort_options: [
                { key: "last_date", text: "Last Post Date", value: "latest_post_time" },
                { key: "first_date", text: "First Post Date", value: "earliest_post_time" },
                { key: "likes", text: "Max Likes", value: "likes" },
                { key: "rts", text: "Max Retweets", value: "rts" },
                { key: "posts", text: "Number of Posts", value: "posts" }
            ]
        },
        /**
         * {
                "id": 2982,
                "file": "/media/data/media/Library/KaorinPicture/%E7%B9%94_200109_0238.jpg",
                "file_name": "織_200109_0238.jpg",
                "file_type": "image/jpg",
                "weight": 1.0,
                "seiyuu_name": "前田佳織里",
                "seiyuu_screen_name": "kaorin__bot",
                "seiyuu_id_name": "kaorin",
                "posts": 15,
                "likes": 3108,
                "rts": 689
            },
         */
        query_results: []
    },
    reducers: {
        setActiveTab: (state, action) => {
            if (action.payload === "tweet_id") {
                state.active_tab = "tweet_id";
            }
            else {
                state.active_tab = "filter";
            }
        },
        setFilterOptions: (state, action) => {
            state.filter_options = {
                ...state.filter_options,
                ...action.payload
            };
        },
        setLibraryLoading: (state, action) => {
            state.display_options.loading = action.payload === true ? true : false;
        },
        clearFilterOptions: (state, action) => {
            state.filter_options = {
                seiyuu_id_name: "",
                start_date: "", // post date
                end_date: "", // post date
                min_likes: "",
                max_likes: "",
                min_rts: "",
                max_rts: "",
                min_posts: "",
                max_posts: "",
                tweet_id: ""
            };
        },
        setOrderOptions: (state, action) => {
            state.display_options = {
                ...state.display_options,
                sort_by: action.payload.sort_by,
                order: action.payload.order,
            };
        },
        setPageOptions: (state, action) => {
            state.display_options = {
                ...state.display_options,
                page: action.payload.page,
                total_pages: action.payload.total_pages,
            };
        },
        setQueryResults: (state, action) => {
            state.query_results = action.payload;
        }
    },
});


export const {
    setFilterOptions,
    clearFilterOptions,
    setLibraryLoading,
    setActiveTab,
    setOrderOptions,
    setPageOptions,
    setQueryResults
} = LibrarySlice.actions;

export default LibrarySlice.reducer;