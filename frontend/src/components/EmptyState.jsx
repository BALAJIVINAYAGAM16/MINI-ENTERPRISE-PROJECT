export default function EmptyState({

  text = "No Data Found"

}) {

  return (

    <div className="bg-white rounded-2xl shadow p-10 text-center">

      <p className="text-gray-500 text-lg">
        {text}
      </p>

    </div>

  );
}