import { useEffect, useState } from "react";

import API from "../api/axios";

import PageHeader from "../components/PageHeader";

import SLABadge from "../components/SLABadge";

export default function SLADashboard() {

  const [records, setRecords] = useState([]);

  useEffect(() => {
    fetchRecords();
  }, []);

  const fetchRecords = async () => {

    try {

      const res = await API.get(
        "/sla-tracking/active"
      );

      setRecords(res.data);

    } catch (error) {

      console.error(error);

    }
  };

  return (

    <div className="p-6">

      <PageHeader
        title="SLA Dashboard"
        subtitle="Track SLA performance"
      />

      <div className="grid grid-cols-4 gap-4 mb-8">

        <div className="bg-white rounded-2xl shadow p-5">

          <p className="text-gray-500">
            Active SLA
          </p>

          <h2 className="text-4xl font-bold">
            {records.length}
          </h2>

        </div>

      </div>

      <div className="bg-white rounded-2xl shadow overflow-hidden">

        <table className="w-full">

          <thead className="bg-gray-100">

            <tr>

              <th className="p-4 text-left">
                Module
              </th>

              <th className="p-4 text-left">
                Record ID
              </th>

              <th className="p-4 text-left">
                SLA Status
              </th>

              <th className="p-4 text-left">
                Due Time
              </th>

            </tr>

          </thead>

          <tbody>

            {records.map((item) => (

              <tr
                key={item.id}
                className="border-t"
              >

                <td className="p-4">
                  {item.module_name}
                </td>

                <td className="p-4">
                  {item.record_id}
                </td>

                <td className="p-4">
                  <SLABadge
                    status={item.status}
                  />
                </td>

                <td className="p-4">
                  {item.due_time}
                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

    </div>
  );
}