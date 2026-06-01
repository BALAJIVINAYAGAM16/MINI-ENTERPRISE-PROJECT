import {
  Route,
} from "react-router-dom";

import SLADashboard from "../pages/SLADashboard";

import SLARules from "../pages/SLARules";

import ApprovalEscalations from "../pages/ApprovalEscalations";

import ApprovalDelegations from "../pages/ApprovalDelegations";

import NotificationPreferences from "../pages/NotificationPreferences";

import AuditLogs from "../pages/AuditLogs";
import ProtectedRoute from "../components/ProtectedRoute";

export default function AppRoutes() {

  return (
    <>

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
    </>
  );
}
