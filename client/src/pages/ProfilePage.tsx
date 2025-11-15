import React, {useEffect, useState, type ChangeEvent} from "react";
import {useNavigate} from "react-router-dom";
import {useTheme} from "../components/ThemeContext";
import ThemeSwitcher from "../components/ThemeSwitcher";

export default function ProfilePage() {
    const navigate = useNavigate();
    const {theme} = useTheme();

    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [message, setMessage] = useState<string | null>(null);
    const [profile, setProfile] = useState({
        gender: "",
        height_cm: "",
        weight_kg: "",
        target_weight_kg: "",
        age: ""
    });

    // Fetch profile data from API
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
                    age: data.age || ""
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

    // Save updated profile to API
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

            if (res.ok) {
                navigate("/dashboard");
            } else {
                const data = await res.json();
                setMessage(data.message || "Error updating profile");
            }
        } catch {
            setMessage("Network error");
        } finally {
            setSaving(false);
        }
    };

    // Handle input changes
    const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        setProfile({...profile, [e.target.name]: e.target.value});
    };

    useEffect(() => {
        fetchProfile();
    }, []);

    // Loading state
    if (loading) {
        return (
            <div
                className="flex justify-center items-center h-screen bg-gradient-to-br from-purple-600 via-pink-500 to-blue-500 text-white">
                Loading profile...
            </div>
        );
    }

    return (
        <div className="relative w-full min-h-screen transition-colors duration-500">
            {/* Background gradient */}
            <div
                className="absolute inset-0 bg-gradient-to-br from-purple-600 via-pink-500 to-blue-500 dark:from-gray-900 dark:via-gray-800 dark:to-black transition-colors duration-500"/>
            <div className="absolute inset-0 bg-black/10 dark:bg-black/50 backdrop-blur-[1px]"/>

            {/* ThemeSwitcher button in the top-right corner */}
            <div className="absolute top-4 right-4 z-50">
                <ThemeSwitcher/>
            </div>

            {/* Scrollable content */}
            <div className="relative z-10 max-w-3xl mx-auto px-4 sm:px-6 lg:px-10 py-10 overflow-y-auto">
                {/* Header */}
                <h1 className="text-4xl font-extrabold text-white drop-shadow-md text-center sm:text-left mb-10">
                    Your Profile
                </h1>

                {/* Message alert */}
                {message && (
                    <div
                        className="mb-4 text-center bg-base-200/50 dark:bg-base-300/50 p-3 rounded-lg text-base-content transition-colors duration-300">
                        {message}
                    </div>
                )}

                {/* Profile card */}
                <div
                    className="bg-base-100/90 dark:bg-base-200/80 border border-base-300 dark:border-base-700 rounded-2xl p-6 space-y-4 shadow-lg transition-colors duration-300">
                    {/* Gender select */}
                    <div>
                        <label className="block mb-1 font-semibold text-base-content">Gender</label>
                        <select
                            name="gender"
                            value={profile.gender}
                            onChange={handleChange}
                            className="w-full px-3 py-2 rounded-lg bg-base-200 dark:bg-base-300 text-base-content dark:text-base-content focus:outline-none focus:ring-2 focus:ring-primary appearance-none transition-colors duration-300"
                        >
                            <option value="" disabled>Select gender</option>
                            <option value="male">Male</option>
                            <option value="female">Female</option>
                        </select>
                    </div>

                    {/* Height input */}
                    <div>
                        <label className="block mb-1 font-semibold text-base-content">Height (cm)</label>
                        <input
                            type="number"
                            name="height_cm"
                            value={profile.height_cm}
                            onChange={handleChange}
                            placeholder="e.g. 180"
                            className="w-full px-3 py-2 rounded-lg bg-base-200 dark:bg-base-300 text-base-content dark:text-base-content placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary transition-colors duration-300"
                        />
                    </div>

                    {/* Current weight input */}
                    <div>
                        <label className="block mb-1 font-semibold text-base-content">Current Weight (kg)</label>
                        <input
                            type="number"
                            name="weight_kg"
                            value={profile.weight_kg}
                            onChange={handleChange}
                            placeholder="e.g. 75"
                            className="w-full px-3 py-2 rounded-lg bg-base-200 dark:bg-base-300 text-base-content dark:text-base-content placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary transition-colors duration-300"
                        />
                    </div>

                    {/* Target weight input */}
                    <div>
                        <label className="block mb-1 font-semibold text-base-content">Target Weight (kg)</label>
                        <input
                            type="number"
                            name="target_weight_kg"
                            value={profile.target_weight_kg}
                            onChange={handleChange}
                            placeholder="e.g. 70"
                            className="w-full px-3 py-2 rounded-lg bg-base-200 dark:bg-base-300 text-base-content dark:text-base-content placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary transition-colors duration-300"
                        />
                    </div>
                    <div>
                        <label className="block mb-1 font-semibold text-base-content">Age</label>
                        <input
                            type="number"
                            name="age"
                            value={profile.age}
                            onChange={handleChange}
                            placeholder="e.g. 30"
                            className="w-full px-3 py-2 rounded-lg bg-base-200 dark:bg-base-300"
                        />
                    </div>


                    {/* Save button */}
                    <button
                        onClick={handleSave}
                        disabled={saving}
                        className="w-full mt-4 py-2 bg-primary text-primary-content hover:bg-primary-focus rounded-lg font-semibold shadow-md transition-colors duration-300"
                    >
                        {saving ? "Saving..." : "Save Changes"}
                    </button>
                </div>

                {/* Bottom spacing so the save button is not hidden on mobile */}
                <div className="h-16 sm:h-24"/>
            </div>
        </div>
    );
}
