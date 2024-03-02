import { createSlice } from "@reduxjs/toolkit";

const LayoutSlice = createSlice({
    name: "LayoutSlice",
    initialState: {
        left_active: window.innerWidth > 1000,
        right_active: false,
        view_width: window.innerWidth,
        responsive_width: 1000,
        show_admin_menu: false
    },
    reducers: {
        setLeftActive: (state, action) => {
            state.left_active = state.view_width > state.responsive_width ? true : action.payload;
            state.right_active = action.payload ? false : state.right_active;
        },
        setRightActive: (state, action) => {
            state.right_active = action.payload;
            state.left_active = action.payload && state.view_width <= state.responsive_width ? false : state.left_active;
        },
        setViewWidth: (state, action) => {
            state.view_width = action.payload;
            if (action.payload > state.responsive_width) {
                state.left_active = true;
            }
            else {
                state.left_active = false;
            }
        },
        setShowAdminMenu: (state, action) => {
            state.show_admin_menu = action.payload;
        }
    },
});


export const { setLeftActive, setRightActive, setViewWidth, setShowAdminMenu } = LayoutSlice.actions;

export default LayoutSlice.reducer;