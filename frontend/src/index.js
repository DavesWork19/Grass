import React from 'react';
import ReactDOM from 'react-dom/client';
// Bootstrap CSS
import 'bootstrap/dist/css/bootstrap.min.css';
// Bootstrap Bundle JS
import 'bootstrap/dist/js/bootstrap.bundle.min';

// Import router
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import './index.css';
import HomeScreen from './digitPages/HomeScreen';
import NFLHomePage from './nflPages/HomePage';
import NBAHomePage from './nbaPages/HomePage';
import NBAGamePage from './nbaPages/NBAGamePage';
import GamblingHomePage from './gamblingPages/GamblingHomePage';
import MatchupPage from './nflPages/MatchupPage';
import GameContainer from './digitPages/GameContainer';
import NoPage from './NoPage';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <BrowserRouter>
    <Routes>
      <Route path='/' element={<HomeScreen />} />
      <Route path='/daGame' element={<GameContainer />} />
      <Route path='/2332220' element={<GamblingHomePage />} />
      <Route path='/2332220/Basketball' element={<NBAHomePage />} />
      <Route path='/2332220/Basketball/:teams' element={<NBAGamePage />} />
      <Route path='/2332220/Football' element={<NFLHomePage />} />
      <Route path='/2332220/Football/:teams' element={<MatchupPage />} />
      <Route path='*' element={<NoPage />} />
    </Routes>
  </BrowserRouter>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
