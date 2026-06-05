import { useContext } from "react";
import { Navigate, useLocation } from "react-router-dom";
import { AuthContext } from "../context/auth-context";

const ProtectedRoute = ({ children }) => {
  const { token } = useContext(AuthContext);
  const location = useLocation();

  return token ? (
    children
  ) : (
    <Navigate to="/login" replace state={{ from: location }} />
  );
};

export default ProtectedRoute;
