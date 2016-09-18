import React from 'react';
import { Router, Route, browserHistory, hashHistory, IndexRoute } from 'react-router';

// Layout
import PageLayout from './components/page-layout';

// Pages
import Main from './components/main';
import EditItem from './components/edit-item-container';
import Sizes from './components/sizes';

export default (
  <Router history={hashHistory}>
    <Route path="/" component={PageLayout}>
      <IndexRoute component={Main} />
      <Route path="edit/:id" component={EditItem} />
      <Route path="new" component={EditItem} />
      <Route path="sizes" component={Sizes} />
    </Route>
  </Router>
);