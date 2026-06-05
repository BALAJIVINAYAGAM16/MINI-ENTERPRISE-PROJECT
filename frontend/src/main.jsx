import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";

import App from "./App";
import "./index.css";

import { AuthProvider } from "./context/AuthContext";
import { TenantProvider } from "./context/TenantContext";

import ToastContainer from "./components/ToastContainer";

ReactDOM.createRoot(
  document.getElementById("root")
).render(
  <React.StrictMode>

    <BrowserRouter>

      <AuthProvider>

        <TenantProvider>

          <App />

          <ToastContainer />

        </TenantProvider>

      </AuthProvider>

    </BrowserRouter>

  </React.StrictMode>
);