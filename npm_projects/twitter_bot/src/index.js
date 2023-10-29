import React from "react";
import { createRoot } from "react-dom/client";
import App from "./components/App";

const root = createRoot(document.getElementById("root"));

// wait 5 seconds before rendering
// setTimeout(() => {
//     document.getElementById("loading").style.opacity = "0";
//     root.render(<App />);
// }, 2000);

root.render(<App />);

