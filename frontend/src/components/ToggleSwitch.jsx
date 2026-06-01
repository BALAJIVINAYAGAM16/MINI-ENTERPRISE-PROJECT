export default function ToggleSwitch({

  enabled,

  onChange,

}) {

  return (

    <button
      onClick={onChange}
      className={`w-14 h-7 rounded-full transition relative ${
        enabled
          ? "bg-green-500"
          : "bg-gray-300"
      }`}
    >

      <div
        className={`absolute top-0.5 bg-white w-6 h-6 rounded-full shadow transform transition ${
          enabled
            ? "translate-x-7"
            : "translate-x-1"
        }`}
      />

    </button>

  );
}