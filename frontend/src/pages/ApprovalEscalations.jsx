import { useEffect, useState } from "react";

import API from "../api/axios";

import PageHeader from "../components/PageHeader";

import StatusBadge from "../components/StatusBadge";

export default function ApprovalEscalations() {

  const [escalations, setEscalations] =
    useState([]);

  useEffect(() => {
    fetchEscalations();
  }, []);

  const fetchEscalations = async () => {

    try {

      const res = await API.get(
        "/approval-escalations"
      );

      setEscalations(res.data);

    } catch (error) {

      console.error(error);

    }
  };

  return (

    <div className="p-6">

      <PageHeader
        title="Approval Escalations"
        subtitle="Manage escalated approvals"
      />

      <div className="bg-white rounded-2xl shadow overflow-hidden">

        <table className="w-full">

          <thead className="bg-gray-100">

            <tr>

              <th className="p-4 text-left">
                Approval ID
              </th>

              <th className="p-4 text-left">
                Escalated From
              </th>

              <th className="p-4 text-left">
                Escalated To
              </th>

              <th className="p-4 text-left">
                Status
              </th>

            </tr>

          </thead>

          <tbody>

            {escalations.map((item) => (

              <tr
                key={item.id}
                className="border-t"
              >

                <td className="p-4">
                  {item.approval_id}
                </td>

                <td className="p-4">
                  {item.escalated_from}
                </td>

                <td className="p-4">
                  {item.escalated_to}
                </td>

                <td className="p-4">

                  <StatusBadge
                    text={item.status}
                    type={
                      item.status === "PENDING"
                        ? "warning"
                        : "success"
                    }
                  />

                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

    </div>
  );
}