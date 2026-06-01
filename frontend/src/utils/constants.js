export const SLA_STATUS = {

  ACTIVE: "ACTIVE",

  BREACHED: "BREACHED",

  COMPLETED: "COMPLETED",

  ESCALATED: "ESCALATED",

  COMPLETED_WITHIN_SLA:
    "COMPLETED_WITHIN_SLA",
};

export const APPROVAL_STATUS = {

  PENDING: "PENDING",

  APPROVED: "APPROVED",

  REJECTED: "REJECTED",

  ESCALATED: "ESCALATED",
};

export const ESCALATION_STATUS = {

  PENDING: "PENDING",

  RESOLVED: "RESOLVED",

  CANCELLED: "CANCELLED",
};

export const PRIORITY_LEVELS = [

  "LOW",

  "MEDIUM",

  "HIGH",

  "CRITICAL",
];

export const MODULES = [

  "TASK",

  "APPROVAL",

  "DOCUMENT",

  "WORKFLOW",
];

export const USER_ROLES = {

  ADMIN: "ADMIN",

  MANAGER: "MANAGER",

  EMPLOYEE: "EMPLOYEE",

  AUDITOR: "AUDITOR",
};

export const NOTIFICATION_TYPES = [

  "TASK",

  "APPROVAL",

  "ESCALATION",

  "DOCUMENT",
];

export const API_ENDPOINTS = {

  SLA_RULES:
    "/sla-rules",

  SLA_TRACKING:
    "/sla-tracking",

  APPROVAL_ESCALATIONS:
    "/approval-escalations",

  APPROVAL_DELEGATIONS:
    "/approval-delegations",

  NOTIFICATION_PREFERENCES:
    "/notification-preferences",

  AUDIT_LOGS:
    "/audit-logs",
};

export const TABLE_PAGE_SIZE = 10;

export const DATE_FORMAT =
  "YYYY-MM-DD";

export const DATETIME_FORMAT =
  "YYYY-MM-DD HH:mm:ss";