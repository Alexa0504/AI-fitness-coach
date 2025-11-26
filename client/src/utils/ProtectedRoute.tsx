import React from "react";
import { Navigate } from "react-router-dom";

interface Props {
  children: JSX.Element;
}

const ProtectedRoute: React.FC<Props> = ({ children }) => {
  const isAuthenticated = !!localStorage.getItem("authToken"); 

  return isAuthenticated ? children : <Navigate to="/login" />;
};

export default ProtectedRoute;
