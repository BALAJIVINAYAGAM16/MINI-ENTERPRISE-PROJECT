import { useEffect, useState } from "react";

import API from "../api/axios";

import ToggleSwitch from "../components/ToggleSwitch";

import PageHeader from "../components/PageHeader";

export default function NotificationPreferences() {

  const [preferences, setPreferences] =
    useState(null);

  useEffect(() => {
    fetchPreferences();
  }, []);

  const fetchPreferences = async () => {

    try {

      const res = await API.get(
        "/notification-preferences/me"
      );

      setPreferences(res.data);

    } catch (error) {

      console.error(error);

    }
  };

  const handleToggle = (field) => {

    setPreferences({
      ...preferences,
      [field]: !preferences[field],
    });
  };

  const savePreferences = async () => {

    try {

      await API.put(
        "/notification-preferences/me",
        preferences
      );

      alert("Preferences Updated");

    } catch (error) {

      console.error(error);

    }
  };

  if (!preferences) return null;

  return (

    <div className="p-6 max-w-3xl">

      <PageHeader
        title="Notification Preferences"
        subtitle="Manage notifications"
      />

      <div className="bg-white rounded-2xl shadow p-6 space-y-6">

        {Object.keys(preferences)

          .filter(
            (key) =>
              typeof preferences[key] ===
              "boolean"
          )

          .map((key) => (

            <div
              key={key}
              className="flex justify-between items-center"
            >

              <span className="capitalize">
                {key.replaceAll("_", " ")}
              </span>

              <ToggleSwitch
                enabled={preferences[key]}
                onChange={() =>
                  handleToggle(key)
                }
              />

            </div>

          ))}

        <button
          onClick={savePreferences}
          className="bg-blue-600 text-white px-5 py-2 rounded-lg"
        >
          Save
        </button>

      </div>

    </div>
  );
}