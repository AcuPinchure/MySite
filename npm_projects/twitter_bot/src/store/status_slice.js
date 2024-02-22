import { createSlice } from "@reduxjs/toolkit";

const StatusSlice = createSlice({
    name: "StatusSlice",
    /**
     * initialState: {
     *  name: "",
     *  screen_name: "",
     *  activated: false,
     *  last_post: "",
     *  interval: 0,
     */
    initialState: [],
    reducers: {
        setStatus: (state, action) => {
            state = action.payload;
        },
    },
});


export const { setStatus } = StatusSlice.actions;

export default StatusSlice.reducer;