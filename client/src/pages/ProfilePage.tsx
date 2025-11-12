import React, { useEffect, useState, type ChangeEvent } from "react";
import { useNavigate } from "react-router-dom";
import { useTheme } from "../components/ThemeContext";
import ThemeSwitcher from "../components/ThemeSwitcher";

export default function ProfilePage() {
  const navigate = useNavigate();
  const { theme } = useTheme();

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [profile, setProfile] = useState({
    gender: "",
    height_cm: "",
    weight_kg: "",
    target_weight_kg: "",
  });

  const fetchProfile = async () => {
    try {
      const res = await fetch("http://localhost:5000/api/users/profile", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("authToken")}`,
        },
      });
      const data = await res.json();
      if (res.ok) {
        setProfile({
          gender: data.gender || "",
          height_cm: data.height_cm || "",
          weight_kg: data.weight_kg || "",
          target_weight_kg: data.target_weight_kg || "",
        });
      } else {
        setMessage(data.message || "Failed to load profile");
      }
    } catch {
      setMessage("Error fetching profile data");
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      const res = await fetch("http://localhost:5000/api/users/profile", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("authToken")}`,
        },
        body: JSON.stringify(profile),
      });
      const data = await res.json();
      if (res.ok) {
        setMessage("✅ Profile updated successfully!");
      } else {
        setMessage(data.message || "Error updating profile");
      }
    } catch {
      setMessage("Network error");
    } finally {
      setSaving(false);
    }
  };

  useEffect(() => {
    fetchProfile();
  }, []);

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setProfile({ ...profile, [e.target.name]: e.target.value });
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen bg-gradient-to-br from-purple-600 via-pink-500 to-blue-500 text-white">
        Loading profile...
      </div>
    );
  }

  return (
    <div className={`relative min-h-screen ${theme} transition-colors duration-500`}>
      <div className="absolute inset-0 bg-gradient-to-br from-purple-600 via-pink-500 to-blue-500 dark:from-gray-900 dark:via-gray-800 dark:to-black transition-colors duration-500" />
      <div className="absolute inset-0 bg-black/10 dark:bg-black/50 backdrop-blur-[1px]" />
      <div className="relative z-10 max-w-3xl mx-auto px-6 py-10 text-white">
        {/* Header */}
        <div className="flex justify-between items-center mb-10">
          <h1 className="text-4xl font-extrabold drop-shadow-md">Your Profile</h1>
          <div className="flex gap-3 items-center">
            <ThemeSwitcher />
            <button
              onClick={() => navigate("/")}
              className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg font-semibold shadow-md transition-all duration-200"
            >
              Back to Dashboard
            </button>
          </div>
        </div>

        {/* Message */}
        {message && (
          <div className="mb-4 text-center bg-black/30 p-3 rounded-lg">
            {message}
          </div>
        )}

        {/* Profile Card */}
        <div className="bg-white/10 backdrop-blur-lg border border-white/20 rounded-2xl p-6 space-y-4 shadow-lg">
          <div>
            <label className="block mb-1 font-semibold">Gender</label>
            <input
              name="gender"
              value={profile.gender}
              onChange={handleChange}
              placeholder="male / female"
              className="w-full px-3 py-2 rounded-lg bg-white/20 text-white placeholder:text-white/60 focus:outline-none focus:ring-2 focus:ring-pink-300"
            />
          </div>

          <div>
            <label className="block mb-1 font-semibold">Height (cm)</label>
            <input
              type="number"
              name="height_cm"
              value={profile.height_cm}
              onChange={handleChange}
              placeholder="e.g. 180"
              className="w-full px-3 py-2 rounded-lg bg-white/20 text-white placeholder:text-white/60 focus:outline-none focus:ring-2 focus:ring-pink-300"
            />
          </div>

          <div>
            <label className="block mb-1 font-semibold">Current Weight (kg)</label>
            <input
              type="number"
              name="weight_kg"
              value={profile.weight_kg}
              onChange={handleChange}
              placeholder="e.g. 75"
              className="w-full px-3 py-2 rounded-lg bg-white/20 text-white placeholder:text-white/60 focus:outline-none focus:ring-2 focus:ring-pink-300"
            />
          </div>

          <div>
            <label className="block mb-1 font-semibold">Target Weight (kg)</label>
            <input
              type="number"
              name="target_weight_kg"
              value={profile.target_weight_kg}
              onChange={handleChange}
              placeholder="e.g. 70"
              className="w-full px-3 py-2 rounded-lg bg-white/20 text-white placeholder:text-white/60 focus:outline-none focus:ring-2 focus:ring-pink-300"
            />
          </div>

          <button
            onClick={handleSave}
            disabled={saving}
            className="w-full mt-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg font-semibold shadow-md transition-all"
          >
            {saving ? "Saving..." : "Save Changes"}
          </button>
        </div>
      </div>
    </div>
  );
}
