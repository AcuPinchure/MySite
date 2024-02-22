import { configureStore } from "@reduxjs/toolkit";

import StatsSlice from "./stats_slice";
import StatusSlice from "./status_slice";
import ImageSlice from "./image_slice";
import LayoutSlice from "./layout_slice";


const store = configureStore({
    reducer: {
        StatsSlice,
        StatusSlice,
        ImageSlice,
        LayoutSlice
    },
    devTools: window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__()
});

export default store;