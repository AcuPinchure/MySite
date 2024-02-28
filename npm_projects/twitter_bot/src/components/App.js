import BotLayout from './layout';

import store from '../store';
import { Provider } from 'react-redux';
import { setShowAdminMenu, setViewWidth } from '../store/layout_slice';
import { setSeiyuuList } from '../store/stats_slice';

import React, { useEffect } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

function App() {

  useEffect(() => {

    function updateViewWidth() {
      store.dispatch(setViewWidth(window.innerWidth));
    }

    // Attach the event listener to update viewWidth when the window is resized
    window.addEventListener('resize', updateViewWidth);

    // Clean up the event listener when the component unmounts
    return () => {
      window.removeEventListener('resize', updateViewWidth);
    };
  }, []);


  useEffect(() => {
    fetch("/bot/api/testAuth/").then(res => {
      store.dispatch(setShowAdminMenu(res.status === 200));
    })
    fetch("/bot/api/config/get/").then(res => {
      if (res.status === 200) {
        res.json().then(data => {
          store.dispatch(setSeiyuuList(data.data));
        });
      }
    })
  }, []);
  return (
    <Provider store={store}>
      <Router>
        <BotLayout />
      </Router>
    </Provider>

  );
}

export default App;
export const seiyuu_name = {
  "kaorin": "前田佳織里 kaorin__bot",
  "akarin": "鬼頭明里 akarin__bot",
  "chemi": "田中ちえ美 Chiemi__bot",
  "konachi": "月音こな konachi__bot"
}
