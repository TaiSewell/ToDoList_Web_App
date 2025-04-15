// src/App.js
import React from 'react';
import './App.css';
import Register from './Pages/Register';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

// Import Component Pages
import Home from './Pages/Home';
import Login from './Pages/Login';
import Dashboard from './Pages/Dashboard';
import NotFound from './Pages/NotFound';
import PrivateRoute from './Pages/PrivateRoute';



function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/dashboard" element={
            <PrivateRoute> 
            <Dashboard /> 
            </PrivateRoute>} />
            
          <Route path="*" element={<NotFound />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
