import React, { useState, Suspense } from 'react';
import axios from "axios";
import ReactDOM from 'react-dom/client';
import './index.css';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import { CSSTransition, TransitionGroup } from 'react-transition-group';

// Lazy loading the components
const App = React.lazy(() => import('./App'));
const SearchBar = React.lazy(() => import('./Search').then(module => ({ default: module.SearchBar })));
const Predict = React.lazy(() => import('./Predict'));

const root = ReactDOM.createRoot(document.getElementById('root'));

const StartServerButton = () => {
  const [isStarting, setIsStarting] = useState(false);
  const [serverStatus, setServerStatus] = useState('Start Server');
  const [serverRunning, setServerRunning] = useState(false);

  const handleStartServer = async () => {
    setIsStarting(true);
    setServerStatus('Starting...');

    try {
      // Simulate server start by calling an API
      const response = await axios.post("https://pearl-natalia--flask-app-api.modal.run/");

      if (response.status === 200 && response.data.message) {
        setTimeout(() => {
          setServerStatus('Server Running');
          setServerRunning(true);
        }, 5000);

      }
    } catch (error) {
      setServerStatus('Error. Is server running?'); // Display "Error" if failure

      // Reset status after 2 seconds
      setTimeout(() => {
        setServerStatus('Start Server');
      }, 2000); // Delay for 2 seconds
    } finally {
      setIsStarting(false); // Stop loading
    }
  };

  return (
    <button
      className="menu-button"
      id="server-button"
      onClick={handleStartServer}
      style={{
        backgroundColor: serverRunning ? 'green' : '#960b16', // Color change based on server status
        color: 'white',
        fontSize: '15px',
        msOverflowY: false
      }}
      disabled={isStarting} // Disable the button while starting the server
    >
      {isStarting ? 'Starting...' : serverStatus}
    </button>
  );
};

root.render(
  <>
    <Router>
      <div id="header">
        <div id="logo-parent-div">
          <img src="images/legacy-logo.webp" alt="Company Logo" className="logo" />
        </div>
        <div id="menu">
          <Link className="menu-link" >
            <StartServerButton />
          </Link>
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
    </Router >
  </>
);
