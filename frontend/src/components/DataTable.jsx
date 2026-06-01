export default function DataTable({

  columns,

  data,

  renderActions,

}) {

  return (

    <div className="bg-white rounded-2xl shadow overflow-hidden">

      <table className="w-full">

        <thead className="bg-gray-100">

          <tr>

            {columns.map((column) => (

              <th
                key={column.key}
                className="p-4 text-left text-sm font-semibold text-gray-700"
              >
                {column.label}
              </th>

            ))}

            {renderActions && (
              <th className="p-4 text-left">
                Actions
              </th>
            )}

          </tr>

        </thead>

        <tbody>

          {data.map((row, index) => (

            <tr
              key={index}
              className="border-t hover:bg-gray-50"
            >

              {columns.map((column) => (

                <td
                  key={column.key}
                  className="p-4"
                >
                  {row[column.key]}
                </td>

              ))}

              {renderActions && (

                <td className="p-4">
                  {renderActions(row)}
                </td>

              )}

            </tr>

          ))}

        </tbody>

      </table>

    </div>
  );
}