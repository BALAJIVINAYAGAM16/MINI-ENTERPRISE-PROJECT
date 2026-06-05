import { Routes, Route } from "react-router-dom";

import ProtectedRoute from "../components/ProtectedRoute";

// Tenant Management
import Tenants from "../pages/tenants/Tenants";
import CreateTenant from "../pages/tenants/CreateTenant";
import TenantView from "../pages/tenants/TenantView";
import TenantOnboarding from "../pages/tenants/TenantOnboarding";
import CollaborationSettings from "../pages/tenants/CollaborationSettings";
import CollaborationUsage from "../pages/tenants/CollaborationUsage";

// Workspace Management
import Workspaces from "../pages/workspaces/Workspaces";
import CreateWorkspace from "../pages/workspaces/CreateWorkspace";
import WorkspaceView from "../pages/workspaces/WorkspaceView";
import WorkspaceMembersPage from "../pages/workspaces/WorkspaceMembersPage";

// Channel Management
import Channels from "../pages/channels/Channels";
import CreateChannel from "../pages/channels/CreateChannel";
import ChannelView from "../pages/channels/ChannelView";
import ChannelMembersPage from "../pages/channels/ChannelMembersPage";

// SLA Module
import SLADashboard from "../pages/SLADashboard";
import SLARules from "../pages/SLARules";
import ApprovalEscalations from "../pages/ApprovalEscalations";
import ApprovalDelegations from "../pages/ApprovalDelegations";
import NotificationPreferences from "../pages/NotificationPreferences";
import AuditLogs from "../pages/AuditLogs";

export default function AppRoutes() {
  return (
    <Routes>

      {/* ===================== */}
      {/* Tenant Management */}
      {/* ===================== */}

      <Route
        path="/tenants"
        element={
          <ProtectedRoute>
            <Tenants />
          </ProtectedRoute>
        }
      />

      <Route
        path="/tenants/create"
        element={
          <ProtectedRoute>
            <CreateTenant />
          </ProtectedRoute>
        }
      />

      <Route
        path="/tenants/:id"
        element={
          <ProtectedRoute>
            <TenantView />
          </ProtectedRoute>
        }
      />

      <Route
        path="/tenants/onboarding"
        element={
          <ProtectedRoute>
            <TenantOnboarding />
          </ProtectedRoute>
        }
      />

      <Route
        path="/tenants/settings"
        element={
          <ProtectedRoute>
            <CollaborationSettings />
          </ProtectedRoute>
        }
      />

      <Route
        path="/tenants/usage"
        element={
          <ProtectedRoute>
            <CollaborationUsage />
          </ProtectedRoute>
        }
      />

      {/* ===================== */}
      {/* Workspace Management */}
      {/* ===================== */}

      <Route
        path="/workspaces"
        element={
          <ProtectedRoute>
            <Workspaces />
          </ProtectedRoute>
        }
      />

      <Route
        path="/workspaces/create"
        element={
          <ProtectedRoute>
            <CreateWorkspace />
          </ProtectedRoute>
        }
      />

      <Route
        path="/workspaces/:id"
        element={
          <ProtectedRoute>
            <WorkspaceView />
          </ProtectedRoute>
        }
      />

      <Route
        path="/workspaces/:id/members"
        element={
          <ProtectedRoute>
            <WorkspaceMembersPage />
          </ProtectedRoute>
        }
      />

      {/* ===================== */}
      {/* Channel Management */}
      {/* ===================== */}

      <Route
        path="/channels"
        element={
          <ProtectedRoute>
            <Channels />
          </ProtectedRoute>
        }
      />

      <Route
        path="/channels/create"
        element={
          <ProtectedRoute>
            <CreateChannel />
          </ProtectedRoute>
        }
      />

      <Route
        path="/channels/:id"
        element={
          <ProtectedRoute>
            <ChannelView />
          </ProtectedRoute>
        }
      />

      <Route
        path="/channels/:id/members"
        element={
          <ProtectedRoute>
            <ChannelMembersPage />
          </ProtectedRoute>
        }
      />

      {/* ===================== */}
      {/* SLA Management */}
      {/* ===================== */}

      <Route
        path="/dashboard/sla"
        element={
          <ProtectedRoute>
            <SLADashboard />
          </ProtectedRoute>
        }
      />

      <Route
        path="/admin/sla-rules"
        element={
          <ProtectedRoute>
            <SLARules />
          </ProtectedRoute>
        }
      />

      <Route
        path="/approval-escalations"
        element={
          <ProtectedRoute>
            <ApprovalEscalations />
          </ProtectedRoute>
        }
      />

      <Route
        path="/approval-delegations"
        element={
          <ProtectedRoute>
            <ApprovalDelegations />
          </ProtectedRoute>
        }
      />

      <Route
        path="/settings/notification-preferences"
        element={
          <ProtectedRoute>
            <NotificationPreferences />
          </ProtectedRoute>
        }
      />

      <Route
        path="/admin/audit-logs"
        element={
          <ProtectedRoute>
            <AuditLogs />
          </ProtectedRoute>
        }
      />

    </Routes>
  );
}
