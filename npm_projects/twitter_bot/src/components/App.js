import BotLayout from './layout';
import About from './page/about';
import { Stats, StatsOptions } from "./page/stats";
import Login from './page/login';
import ConfigPage from './page/service_config';
import { LibraryOptions, ImageLibrary } from './page/library';

import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import 'semantic-ui-css/semantic.min.css';

function App() {
  return (
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
  );
}

export default App;
