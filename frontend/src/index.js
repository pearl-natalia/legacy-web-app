import React, { Suspense } from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import { CSSTransition, TransitionGroup } from 'react-transition-group';

// Lazy loading the components
const App = React.lazy(() => import('./App'));
const SearchBar = React.lazy(() => import('./Search').then(module => ({ default: module.SearchBar })));
const Predict = React.lazy(() => import('./Predict'));

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <>
    <Router>
      <div id="header">
        <div id="logo-parent-div">
          <img src="images/legacy-logo.webp" alt="Company Logo" className="logo" />
        </div>
        <div id="menu">
          <Link to="/" className="menu-link">
            <button className="menu-button">
              Advice
            </button>
          </Link>
          <Link to="/search" className="menu-link">
            <button className="menu-button">
              Search
            </button>
          </Link>
          <Link to="/predict" className="menu-link">
            <button className="menu-button">
              Predict
            </button>
          </Link>
        </div>
      </div>

      <Suspense fallback={<div>Loading...</div>}>
        <TransitionGroup>
          <CSSTransition timeout={300} classNames="fade" key={window.location.pathname}>
            <Routes>
              <Route path="/" element={<App />} />
              <Route path="/search" element={<SearchBar />} />
              <Route path="/predict" element={<Predict />} />
            </Routes>
          </CSSTransition>
        </TransitionGroup>
      </Suspense>
    </Router>
  </>
);
