import { useEffect, useState } from "react";

import API from "../api/axios";

import PageHeader from "../components/PageHeader";

export default function AuditLogs() {

  const [logs, setLogs] = useState([]);

  useEffect(() => {
    fetchLogs();
  }, []);

  const fetchLogs = async () => {

    try {

      const res = await API.get(
        "/audit-logs"
      );

      setLogs(res.data);

    } catch (error) {

      console.error(error);

    }
  };

  return (

    <div className="p-6">

      <PageHeader
        title="Audit Logs"
        subtitle="Monitor backend activity"
      />

      <div className="bg-white rounded-2xl shadow overflow-hidden">

        <table className="w-full">

          <thead className="bg-gray-100">

            <tr>

              <th className="p-4 text-left">
                User
              </th>

              <th className="p-4 text-left">
                Module
              </th>

              <th className="p-4 text-left">
                Action
              </th>

              <th className="p-4 text-left">
                Record ID
              </th>

              <th className="p-4 text-left">
                Created At
              </th>

            </tr>

          </thead>

          <tbody>

            {logs.map((log) => (

              <tr
                key={log.id}
                className="border-t"
              >

                <td className="p-4">
                  {log.user_id}
                </td>

                <td className="p-4">
                  {log.module_name}
                </td>

                <td className="p-4">
                  {log.action_type}
                </td>

                <td className="p-4">
                  {log.record_id}
                </td>

                <td className="p-4">
                  {log.created_at}
                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

    </div>
  );
}