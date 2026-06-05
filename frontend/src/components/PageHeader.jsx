export default function PageHeader({
  title,
  subtitle,
  action,
}) {
  return (
    <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">

      <div>
        <h1 className="text-3xl font-bold text-gray-800">
          {title}
        </h1>

        {subtitle && (
          <p className="mt-1 text-sm text-gray-500">
            {subtitle}
          </p>
        )}
      </div>

      {action && (
        <div className="flex items-center">
          {action}
        </div>
      )}

    </div>
  );
}