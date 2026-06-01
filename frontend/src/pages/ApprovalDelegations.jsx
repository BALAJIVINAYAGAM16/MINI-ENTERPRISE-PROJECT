import { useEffect, useState } from "react";

import API from "../api/axios";

import PageHeader from "../components/PageHeader";

export default function ApprovalDelegations() {

  const [delegations, setDelegations] =
    useState([]);

  useEffect(() => {
    fetchDelegations();
  }, []);

  const fetchDelegations = async () => {

    try {

      const res = await API.get(
        "/approval-delegations/active"
      );

      setDelegations(res.data);

    } catch (error) {

      console.error(error);

    }
  };

  return (

    <div className="p-6">

      <PageHeader
        title="Approval Delegations"
        subtitle="Manage delegation workflow"
      />

      <div className="bg-white rounded-2xl shadow overflow-hidden">

        <table className="w-full">

          <thead className="bg-gray-100">

            <tr>

              <th className="p-4 text-left">
                Delegator
              </th>

              <th className="p-4 text-left">
                Delegatee
              </th>

              <th className="p-4 text-left">
                Start Date
              </th>

              <th className="p-4 text-left">
                End Date
              </th>

            </tr>

          </thead>

          <tbody>

            {delegations.map((item) => (

              <tr
                key={item.id}
                className="border-t"
              >

                <td className="p-4">
                  {item.delegator_id}
                </td>

                <td className="p-4">
                  {item.delegatee_id}
                </td>

                <td className="p-4">
                  {item.start_date}
                </td>

                <td className="p-4">
                  {item.end_date}
                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

    </div>
  );
}