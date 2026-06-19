import { Routes, Route } from "react-router-dom";

import Sidebar from "./components/Sidebar";
import Navbar from "./components/Navbar";
import ProtectedRoute from "./components/ProtectedRoute";

import Login from "./pages/Login";
import Register from "./pages/Register";

import Dashboard from "./pages/Dashboard";
import CreateTask from "./pages/CreateTask";
import EditTask from "./pages/Edittask";
import Users from "./pages/Users";
import Documents from "./pages/Documents";
import Notifications from "./pages/Notifications";
import AIInsights from "./pages/AIInsights";
import Billing from "./pages/Billing";
import Plans from "./pages/Plans";
import Organization from "./pages/Organization";

import KanbanBoard from "./components/KanbanBoard";
import ApprovalPanel from "./components/ApprovalPanel";

import AppRoutes from "./api/AppRoutes";
import WorkspaceMessages from "./pages/workspaces/WorkspaceMessages";
import WorkspaceTasks from "./pages/workspaces/WorkspaceTasks";

function Layout() {
  return (
    <div className="flex min-h-screen bg-gray-100">

      <Sidebar />

      <div className="flex flex-1 flex-col">

        <Navbar />

        <main className="flex-1 p-6 overflow-auto">

          <Routes>

            {/* Existing Project Routes */}

            <Route
              path="/"
              element={<Dashboard />}
            />

            <Route
              path="/dashboard"
              element={<Dashboard />}
            />

            <Route
              path="/create"
              element={<CreateTask />}
            />

            <Route
              path="/edit/:id"
              element={<EditTask />}
            />

            <Route
              path="/users"
              element={<Users />}
            />

            <Route
              path="/kanban"
              element={<KanbanBoard />}
            />

            <Route
              path="/approvals"
              element={<ApprovalPanel />}
            />

            <Route
              path="/documents"
              element={<Documents />}
            />

            <Route
              path="/notifications"
              element={<Notifications />}
            />

            <Route
              path="/ai-insights"
              element={<AIInsights />}
            />

            <Route
              path="/billing"
              element={<Billing />}
            />

            <Route
              path="/plans"
              element={<Plans />}
            />

            <Route
              path="/organization"
              element={<Organization />}
            />

            {/* Phase 10A Routes */}
            <Route
              path="/*"
              element={<AppRoutes />}
            />

          </Routes>

        </main>

      </div>

    </div>
  );
}

export default function App() {
  return (
    <Routes>

      {/* Public Routes */}

      <Route
        path="/login"
        element={<Login />}
      />

      <Route
        path="/register"
        element={<Register />}
      />

      {/* Protected Application */}
      <Route
  path="/workspaces/:id/messages"
  element={<WorkspaceMessages />}
/>

<Route
  path="/workspaces/:id/tasks"
  element={<WorkspaceTasks />}
/>

      <Route
        path="/*"
        element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }
      />

    </Routes>
  );
}
