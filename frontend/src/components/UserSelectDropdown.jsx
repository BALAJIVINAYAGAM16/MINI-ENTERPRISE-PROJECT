import { useEffect, useState } from "react";

import API from "../api/axios";

export default function UserSelectDropdown({

  value,

  onChange,

}) {

  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {

    try {

      const res = await API.get("/users");

      setUsers(res.data);

    } catch (error) {

      console.error(error);

    }
  };

  return (

    <select
      value={value}
      onChange={(e) =>
        onChange(e.target.value)
      }
      className="border rounded-lg px-3 py-2 w-full"
    >

      <option value="">
        Select User
      </option>

      {users.map((user) => (

        <option
          key={user.id}
          value={user.id}
        >
          {user.name}
        </option>

      ))}

    </select>
  );
}