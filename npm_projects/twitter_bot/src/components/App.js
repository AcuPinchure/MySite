import BotLayout from './layout';
import About from './page/about';
import Admin from './page/admin';
import { Stats, StatsOptions } from "./page/stats";

import React from 'react';
import { HashRouter, Route, Switch } from 'react-router-dom';
import 'semantic-ui-css/semantic.min.css';

function App() {
  return (
    <HashRouter>
        <Switch>
            <Route exact path="/" component={About} />
            <Route path="/stats" component={()=>
                (<BotLayout rightBarOptions={<StatsOptions defaultStartDate="2023-06-30" defaultEndDate="2023-07-31" defaultSeiyuu="kaorin" />} ><Stats></Stats></BotLayout>)
              } />
            <Route path="/settings" component={()=>
                (<BotLayout></BotLayout>)
              } />
            <Route path="/library" component={()=>
                (<BotLayout></BotLayout>)
              } />
            <Route path="/logs" component={()=>
                (<BotLayout></BotLayout>)
              } />
        </Switch>
    </HashRouter>
  );
}

export default App;
