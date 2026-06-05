import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

let refreshPromise = null;

const clearAuth = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("refreshToken");
  window.dispatchEvent(new Event("auth:logout"));
};

API.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

API.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status !== 401 || originalRequest._retry) {
      return Promise.reject(error);
    }

    const refreshToken = localStorage.getItem("refreshToken");
    if (!refreshToken) {
      return Promise.reject(error);
    }

    originalRequest._retry = true;

    try {
      refreshPromise ??= axios
        .post(`${API.defaults.baseURL}/auth/refresh`, {
          refresh_token: refreshToken,
        })
        .finally(() => {
          refreshPromise = null;
        });

      const res = await refreshPromise;

      localStorage.setItem("token", res.data.access_token);
      if (res.data.refresh_token) {
        localStorage.setItem("refreshToken", res.data.refresh_token);
      }
      originalRequest.headers = originalRequest.headers || {};
      originalRequest.headers.Authorization = `Bearer ${res.data.access_token}`;
      return API(originalRequest);
    } catch (refreshError) {
      clearAuth();
      return Promise.reject(refreshError);
    }
  }
);

export default API;
