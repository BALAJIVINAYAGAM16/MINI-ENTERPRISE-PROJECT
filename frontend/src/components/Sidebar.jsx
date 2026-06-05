import { Link, useLocation } from "react-router-dom";

import {
  LayoutDashboard,
  FileText,
  KanbanSquare,
  Bell,
  ClipboardList,
  BrainCircuit,
  CreditCard,
  Building2,
  Settings,
  ShieldCheck,
  UserCheck,
  UserCog,
  FolderKanban,
  MessageSquare,
  Users,
  Activity,
} from "lucide-react";

export default function Sidebar() {
  const location = useLocation();

  const navClass = (path, exact = false) => {
    const isActive = exact
      ? location.pathname === path
      : location.pathname === path ||
        location.pathname.startsWith(`${path}/`);

    return (
    `flex items-center gap-3 px-4 py-3 rounded-xl transition text-sm font-medium ${
      isActive
        ? "bg-white text-slate-900 shadow"
        : "text-slate-300 hover:bg-slate-800 hover:text-white"
    }`
    );
  };

  return (
    <aside className="w-72 min-h-screen bg-slate-700 border-r border-slate-800 p-5 overflow-y-auto">

      {/* Logo */}
      <div className="mb-10">
        <h1 className="text-2xl font-bold text-white">
          TaskFlow
        </h1>

        <p className="text-slate-400 text-sm mt-1">
          Enterprise SaaS Platform
        </p>
      </div>

      {/* Main Navigation */}
      <div>
        <p className="text-xs uppercase tracking-widest text-slate-500 mb-4 px-2">
          Main
        </p>

        <div className="space-y-2">

          <Link
            to="/dashboard"
            className={navClass("/dashboard", true)}
          >
            <LayoutDashboard size={18} />
            Dashboard
          </Link>

          <Link
            to="/documents"
            className={navClass("/documents")}
          >
            <FileText size={18} />
            Documents
          </Link>

          <Link
            to="/kanban"
            className={navClass("/kanban")}
          >
            <KanbanSquare size={18} />
            Kanban
          </Link>

          <Link
            to="/notifications"
            className={navClass("/notifications")}
          >
            <Bell size={18} />
            Notifications
          </Link>

          <Link
            to="/ai-insights"
            className={navClass("/ai-insights")}
          >
            <BrainCircuit size={18} />
            AI Insights
          </Link>

        </div>
      </div>

      {/* Tenant Management */}
      <div className="mt-10">

        <p className="text-xs uppercase tracking-widest text-slate-500 mb-4 px-2">
          Tenant Management
        </p>

        <div className="space-y-2">

          <Link
            to="/tenants"
            className={navClass("/tenants", true)}
          >
            <Building2 size={18} />
            Tenants
          </Link>

          <Link
            to="/tenants/create"
            className={navClass("/tenants/create")}
          >
            <Users size={18} />
            Create Tenant
          </Link>

          <Link
            to="/tenants/onboarding"
            className={navClass("/tenants/onboarding")}
          >
            <Users size={18} />
            Tenant Onboarding
          </Link>

          <Link
            to="/tenants/settings"
            className={navClass("/tenants/settings")}
          >
            <Settings size={18} />
            Collaboration Settings
          </Link>

          <Link
            to="/tenants/usage"
            className={navClass("/tenants/usage")}
          >
            <Activity size={18} />
            Collaboration Usage
          </Link>

        </div>
      </div>

      {/* Workspace & Channel */}
      <div className="mt-10">

        <p className="text-xs uppercase tracking-widest text-slate-500 mb-4 px-2">
          Collaboration
        </p>

        <div className="space-y-2">

          <Link
            to="/workspaces"
            className={navClass("/workspaces", true)}
          >
            <FolderKanban size={18} />
            Workspaces
          </Link>

          <Link
            to="/workspaces/create"
            className={navClass("/workspaces/create")}
          >
            <FolderKanban size={18} />
            Create Workspace
          </Link>

          <Link
            to="/channels"
            className={navClass("/channels", true)}
          >
            <MessageSquare size={18} />
            Channels
          </Link>

          <Link
            to="/channels/create"
            className={navClass("/channels/create")}
          >
            <MessageSquare size={18} />
            Create Channel
          </Link>

        </div>
      </div>

      {/* Workflow Governance */}
      <div className="mt-10">

        <p className="text-xs uppercase tracking-widest text-slate-500 mb-4 px-2">
          Workflow Governance
        </p>

        <div className="space-y-2">

          <Link
            to="/admin/sla-rules"
            className={navClass("/admin/sla-rules")}
          >
            <ShieldCheck size={18} />
            SLA Rules
          </Link>

          <Link
            to="/approval-escalations"
            className={navClass("/approval-escalations")}
          >
            <UserCheck size={18} />
            Approval Escalations
          </Link>

          <Link
            to="/approval-delegations"
            className={navClass("/approval-delegations")}
          >
            <UserCog size={18} />
            Approval Delegations
          </Link>

          <Link
            to="/settings/notification-preferences"
            className={navClass("/settings/notification-preferences")}
          >
            <Bell size={18} />
            Notification Preferences
          </Link>

          <Link
            to="/admin/audit-logs"
            className={navClass("/admin/audit-logs")}
          >
            <ClipboardList size={18} />
            Audit Logs
          </Link>

        </div>
      </div>

      {/* SaaS Management */}
      <div className="mt-10">

        <p className="text-xs uppercase tracking-widest text-slate-500 mb-4 px-2">
          SaaS Management
        </p>

        <div className="space-y-2">

          <Link
            to="/plans"
            className={navClass("/plans")}
          >
            <CreditCard size={18} />
            Plans
          </Link>

          <Link
            to="/billing"
            className={navClass("/billing")}
          >
            <CreditCard size={18} />
            Billing
          </Link>

          <Link
            to="/organization"
            className={navClass("/organization")}
          >
            <Building2 size={18} />
            Organization
          </Link>

        </div>
      </div>

      {/* Current Plan Card */}
      <div className="mt-12 bg-slate-900 border border-slate-800 rounded-2xl p-4">

        <h3 className="text-white font-semibold">
          Current Plan
        </h3>

        <p className="text-indigo-400 text-2xl font-bold mt-2">
          Silver
        </p>

        <p className="text-slate-400 text-sm mt-1">
          1000 Credits Included
        </p>

        <Link
          to="/plans"
          className="mt-4 inline-block w-full text-center bg-indigo-600 hover:bg-indigo-500 transition text-white py-2 rounded-xl text-sm font-medium"
        >
          Upgrade Plan
        </Link>

      </div>

    </aside>
  );
}
