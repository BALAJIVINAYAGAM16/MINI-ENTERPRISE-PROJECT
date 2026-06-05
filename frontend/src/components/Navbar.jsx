import { useContext, useEffect, useState } from "react";

import {
  Link,
  useNavigate,
  useLocation,
} from "react-router-dom";

import {
  Search,
  UserCircle,
  CreditCard,
} from "lucide-react";

import { AuthContext } from "../context/auth-context";

import API from "../api/axios";

import NotificationBell from "./NotificationBell";

export default function Navbar() {
  const { logout } =
    useContext(AuthContext);

  const [user, setUser] =
    useState(null);

  const [credits, setCredits] =
    useState(0);

  const [
    dropdownOpen,
    setDropdownOpen,
  ] = useState(false);

  const navigate =
    useNavigate();

  const location =
    useLocation();

  useEffect(() => {
    API.get("/auth/me")
      .then((res) => {
        setUser(res.data);

        setCredits(
          res.data.credits || 0
        );
      })
      .catch(() =>
        setUser(null)
      );
  }, []);

  const handleLogout = () => {
    logout();

    navigate("/login");
  };

  const linkClass = (path) =>
    `px-3 py-2 rounded-xl text-sm font-medium transition ${
      location.pathname === path
        ? "bg-slate-900 text-white shadow"
        : "text-slate-600 hover:bg-slate-100"
    }`;

  return (
    <header className="sticky top-0 z-50 bg-white border-b border-slate-200 shadow-sm">

      <div className="flex items-center justify-between px-6 py-4">

        {/* Left Section */}
        <div className="flex items-center gap-8">

          {/* Logo */}
          <div>
            <h1 className="text-2xl font-bold text-slate-800">
              TaskFlow SaaS
            </h1>

            <p className="text-xs text-slate-500">
              Enterprise Collaboration Platform
            </p>
          </div>

          {/* Search */}
          <div className="hidden md:flex items-center gap-2 bg-slate-100 px-3 py-2 rounded-xl">

            <Search size={18} />

            <input
              type="text"
              placeholder="Search..."
              className="bg-transparent outline-none text-sm"
            />

          </div>

          {/* Navigation */}
          <div className="hidden lg:flex items-center gap-2">

            <Link
              to="/dashboard"
              className={linkClass(
                "/dashboard"
              )}
            >
              Dashboard
            </Link>

            <Link
              to="/tenants"
              className={linkClass(
                "/tenants"
              )}
            >
              Tenants
            </Link>

            <Link
              to="/workspaces"
              className={linkClass(
                "/workspaces"
              )}
            >
              Workspaces
            </Link>

            <Link
              to="/channels"
              className={linkClass(
                "/channels"
              )}
            >
              Channels
            </Link>

            <Link
              to="/dashboard/sla"
              className={linkClass(
                "/dashboard/sla"
              )}
            >
              SLA
            </Link>

          </div>

        </div>

        {/* Right Section */}
        <div className="flex items-center gap-4">

          {/* Credits */}
          {user && (
            <div className="flex items-center gap-2 px-4 py-2 rounded-xl bg-indigo-50 border border-indigo-100 text-indigo-700">

              <CreditCard size={18} />

              <span className="font-semibold text-sm">
                {credits} Credits
              </span>

            </div>
          )}

          {/* Notification */}
          {user ? (
            <NotificationBell />
          ) : null}

          {/* User */}
          {user ? (

            <div className="relative">

              <button
                onClick={() =>
                  setDropdownOpen(
                    !dropdownOpen
                  )
                }
                className="flex items-center gap-3 bg-slate-100 hover:bg-slate-200 px-3 py-2 rounded-xl transition"
              >

                <div className="w-9 h-9 rounded-full bg-slate-900 text-white flex items-center justify-center font-semibold">

                  {user.email?.[0]?.toUpperCase()}

                </div>

                <div className="hidden sm:block text-left">

                  <p className="text-sm font-semibold text-slate-700">
                    {user.email}
                  </p>

                  <p className="text-xs text-slate-500 capitalize">
                    {user.role}
                  </p>

                </div>

              </button>

              {/* Dropdown */}
              {dropdownOpen && (

                <div className="absolute right-0 mt-3 w-56 bg-white border border-slate-200 rounded-2xl shadow-xl overflow-hidden">

                  <button
                    onClick={() =>
                      navigate(
                        "/profile"
                      )
                    }
                    className="w-full text-left px-5 py-3 hover:bg-slate-50 text-sm"
                  >
                    Profile
                  </button>

                  <button
                    onClick={() =>
                      navigate(
                        "/organization"
                      )
                    }
                    className="w-full text-left px-5 py-3 hover:bg-slate-50 text-sm"
                  >
                    Organization
                  </button>

                  <button
                    onClick={() =>
                      navigate(
                        "/billing"
                      )
                    }
                    className="w-full text-left px-5 py-3 hover:bg-slate-50 text-sm"
                  >
                    Billing
                  </button>

                  <button
                    onClick={() =>
                      navigate(
                        "/settings/notification-preferences"
                      )
                    }
                    className="w-full text-left px-5 py-3 hover:bg-slate-50 text-sm"
                  >
                    Settings
                  </button>

                  <hr />

                  <button
                    onClick={
                      handleLogout
                    }
                    className="w-full text-left px-5 py-3 text-red-500 hover:bg-red-50 text-sm"
                  >
                    Logout
                  </button>

                </div>

              )}

            </div>

          ) : (

            <div className="flex items-center gap-3">

              <Link
                to="/login"
                className="px-4 py-2 rounded-xl bg-slate-900 text-white text-sm font-medium hover:bg-slate-800"
              >
                Login
              </Link>

              <Link
                to="/register"
                className="px-4 py-2 rounded-xl border border-slate-300 text-sm font-medium hover:bg-slate-100"
              >
                Register
              </Link>

            </div>

          )}

        </div>

      </div>

    </header>
  );
}
