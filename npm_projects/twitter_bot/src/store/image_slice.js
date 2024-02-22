import { createSlice } from "@reduxjs/toolkit";

const ImageSlice = createSlice({
    name: "ImageSlice",
    /**
     * initialState: {
     *  name: "",
     *  screen_name: "",
     *  activated: false,
     *  last_post: "",
     *  interval: 0,
     */
    initialState: {
        image_options: {
            method: 'filter',
            filter: {
                seiyuu_id_name: "",
                start_date: "",
                end_date: "",
                min_likes: 0,
                max_likes: 0,
                min_rts: 0,
                max_rts: 0,
                min_posts: 0,
                max_posts: 0,
            },
            tweet_id: "",
        },
        query: {
            sort: "ID",
            order: "ASC",
            page_selected: 1,
            page_total: 1,
            result: [],
        }
    },
    reducers: {
        setImageSearchMethod: (state, action) => {
            state.image_options.method = action.payload === "filter" ? "filter" : "tweet_id";
        },
        setImageSearchFilter: (state, action) => {
            state.image_options.filter = {
                ...state.image_options.filter,
                ...action.payload
            };
        }
    },
});


export const { setImageSearchMethod, setImageSearchFilter } = ImageSlice.actions;

export default ImageSlice.reducer;