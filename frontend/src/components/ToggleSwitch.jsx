export default function ToggleSwitch({
  enabled,
  onChange,
}) {
  return (
    <button
      type="button"
      onClick={onChange}
      aria-pressed={enabled}
      className={`relative flex items-center w-16 h-8 rounded-full px-1 transition-colors duration-300 ${
        enabled
          ? "bg-green-500"
          : "bg-red-300"
      }`}
    >
      <div
        className={`absolute w-6 h-6 bg-white rounded-full shadow-md transition-transform duration-300 ${
          enabled
            ? "translate-x-8"
            : "translate-x-0"
        }`}
      />

      <span className="w-full text-xs font-medium text-black text-center">
        {enabled ? "ON" : "OFF"}
      </span>
    </button>
  );
}