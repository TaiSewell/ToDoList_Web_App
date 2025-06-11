import React from 'react';
import { Navigate } from 'react-router-dom';
import PropTypes from "prop-types";

/*******************************************************
Function: PrivateRoute()
Description: This function handles private routes in the application.
It checks if the user is authenticated by verifying the token in local storage.
*******************************************************/
const PrivateRoute = ({ children }) => {
    const token = localStorage.getItem('token'); // Replace with your authentication logic
    return token ? children : <Navigate to="/login" />;
};  

PrivateRoute.propTypes = {
  children: PropTypes.node.isRequired,
};

export default PrivateRoute;
