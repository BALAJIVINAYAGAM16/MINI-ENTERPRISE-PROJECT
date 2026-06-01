export default function DateRangeFilter({

  startDate,

  endDate,

  onStartChange,

  onEndChange,

}) {

  return (

    <div className="flex gap-4 items-center">

      <div>

        <label className="block text-sm mb-1">
          Start Date
        </label>

        <input
          type="date"
          value={startDate}
          onChange={(e) =>
            onStartChange(e.target.value)
          }
          className="border rounded-lg px-3 py-2"
        />

      </div>

      <div>

        <label className="block text-sm mb-1">
          End Date
        </label>

        <input
          type="date"
          value={endDate}
          onChange={(e) =>
            onEndChange(e.target.value)
          }
          className="border rounded-lg px-3 py-2"
        />

      </div>

    </div>
  );
}