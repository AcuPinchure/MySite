import BotLayout from './layout';
import About from './page/about';
import { Stats, StatsOptions } from "./page/stats";
import Login from './page/login';
import ConfigPage from './page/service_config';
import StatusPage from './page/service_status';
import { LibraryOptions, ImageLibrary } from './page/library';

import store from '../store';
import { Provider } from 'react-redux';
import { setShowAdminMenu } from '../store/layout_slice';
import { setSeiyuuList } from '../store/stats_slice';

import React, { useEffect } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

function App() {
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
        <Switch>
          <Route exact path="/bot/" component={About} />
          <Route path="/bot/stats/" component={() =>
            (<BotLayout rightBarOptions={<StatsOptions defaultStartDate="2023-06-30" defaultEndDate="2023-07-31" defaultSeiyuu="kaorin" />} ><Stats></Stats></BotLayout>)
          } />
          <Route path="/bot/login/" component={() =>
          (<BotLayout>
            <Login></Login>
          </BotLayout>)
          } />
          <Route path="/bot/status/" component={() =>
          (<BotLayout>
            <StatusPage></StatusPage>
          </BotLayout>)
          } />
          <Route path="/bot/config/" component={() =>
          (<BotLayout>
            <ConfigPage />
          </BotLayout>)
          } />
          <Route path="/bot/library/" component={() =>
          (<BotLayout rightBarOptions={<LibraryOptions></LibraryOptions>}>
            <ImageLibrary></ImageLibrary>
          </BotLayout>)
          } />
          <Route path="/bot/logs/" component={() =>
            (<BotLayout></BotLayout>)
          } />
        </Switch>
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
