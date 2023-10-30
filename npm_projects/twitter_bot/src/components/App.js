import BotLayout from './layout';
import About from './page/about';
import { Stats, StatsOptions } from "./page/stats";
import ConfigPage from './page/service_config';
import { LibraryOptions, ImageLibrary } from './page/library';

import React from 'react';
import { HashRouter, Route, Switch } from 'react-router-dom';
import 'semantic-ui-css/semantic.min.css';

function App() {
  return (
    <HashRouter>
      <Switch>
        <Route exact path="/" component={About} />
        <Route path="/stats" component={() =>
          (<BotLayout rightBarOptions={<StatsOptions defaultStartDate="2023-06-30" defaultEndDate="2023-07-31" defaultSeiyuu="kaorin" />} ><Stats></Stats></BotLayout>)
        } />
        <Route path="/config" component={() =>
        (<BotLayout>
          <ConfigPage />
        </BotLayout>)
        } />
        <Route path="/library" component={() =>
        (<BotLayout rightBarOptions={<LibraryOptions></LibraryOptions>}>
          <ImageLibrary></ImageLibrary>
        </BotLayout>)
        } />
        <Route path="/logs" component={() =>
          (<BotLayout></BotLayout>)
        } />
      </Switch>
    </HashRouter>
  );
}

export default App;
