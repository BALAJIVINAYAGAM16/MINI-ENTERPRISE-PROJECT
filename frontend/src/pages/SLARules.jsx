import { useEffect, useState } from "react";

import API from "../api/axios";

import PageHeader from "../components/PageHeader";

import DataTable from "../components/DataTable";

import StatusBadge from "../components/StatusBadge";

export default function SLARules() {

  const [rules, setRules] = useState([]);

  useEffect(() => {
    fetchRules();
  }, []);

  const fetchRules = async () => {

    try {

      const res = await API.get("/sla-rules");

      setRules(res.data);

    } catch (error) {

      console.error(error);

    }
  };

  const columns = [

    {
      key: "module_name",
      label: "Module",
    },

    {
      key: "priority",
      label: "Priority",
    },

    {
      key: "allowed_hours",
      label: "Allowed Hours",
    },

    {
      key: "escalation_after_hours",
      label: "Escalation After",
    },
  ];

  return (

    <div className="p-6">

      <PageHeader
        title="SLA Rules"
        subtitle="Manage SLA Rules"
      />

      <DataTable
        columns={columns}
        data={rules.map((rule) => ({
          ...rule,

          escalation_after_hours:
            rule.escalation_after_hours || "-",
        }))}
        renderActions={(row) => (

          <StatusBadge
            text={
              row.is_active
                ? "ACTIVE"
                : "DISABLED"
            }
            type={
              row.is_active
                ? "success"
                : "danger"
            }
          />

        )}
      />

    </div>
  );
}