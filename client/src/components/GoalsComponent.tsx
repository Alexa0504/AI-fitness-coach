import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";

interface Goal {
    id: number;
    goal_type?: string;
    target_value?: number;
    unit?: string;
    goal_name?: string;
    is_completed?: boolean;
}

const GoalsComponent: React.FC = () => {
    const [longGoals, setLongGoals] = useState<Goal[]>([]);
    const [weeklyGoals, setWeeklyGoals] = useState<Goal[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const token = localStorage.getItem("authToken") || "";

    const fetchLongGoals = async () => {
        try {
            const res = await fetch("http://localhost:5000/api/goals/", {
                headers: { Authorization: `Bearer ${token}` },
            });
            const data: { message?: string } & Goal[] = await res.json();
            if (!res.ok) throw new Error(data.message || "Failed to fetch goals.");
            setLongGoals(data as Goal[]);
        } catch (e) {
            const msg = e instanceof Error ? e.message : "Error fetching goals.";
            setError(msg);
        }
    };

    const fetchWeeklyGoals = async () => {
        try {
            const res = await fetch("http://localhost:5000/api/goals/weekly", {
                headers: { Authorization: `Bearer ${token}` },
            });
            const data: { message?: string } & Goal[] = await res.json();
            if (!res.ok) throw new Error(data.message || "Failed to fetch weekly goals.");
            setWeeklyGoals(data as Goal[]);
        } catch (e) {
            const msg = e instanceof Error ? e.message : "Error fetching weekly goals.";
            setError(msg);
        }
    };

    const toggleWeeklyGoal = async (id: number) => {
        try {
            const res = await fetch(`http://localhost:5000/api/goals/weekly/${id}/toggle`, {
                method: "PATCH",
                headers: { Authorization: `Bearer ${token}` },
            });
            const data: { message?: string } & Goal = await res.json();
            if (!res.ok) throw new Error(data.message || "Failed to toggle goal.");
            setWeeklyGoals(prev => prev.map(g => g.id === id ? { ...g, is_completed: !g.is_completed } : g));
        } catch (e) {
            const msg = e instanceof Error ? e.message : "Error toggling weekly goal.";
            setError(msg);
        }
    };

    useEffect(() => {
        const fetchAll = async () => {
            setLoading(true);
            await fetchLongGoals();
            await fetchWeeklyGoals();
            setLoading(false);
        };
        fetchAll();
    }, []);

    return (
        <div className="space-y-6">
            {error && <div className="p-3 rounded-lg bg-red-500/20 text-red-300 border border-red-500/40">{error}</div>}
            {loading && <div className="text-center text-base-content/70">Loading goals...</div>}

            {longGoals.map((g, i) => {
                const progress = Math.min(Math.random() * 100, 100);
                return (
                    <motion.div
                        key={`long-${g.id}`}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: i * 0.15 }}
                        className="bg-base-200/60 dark:bg-base-300/60 rounded-xl p-4 shadow-md border border-base-300 transition-colors duration-300"
                    >
                        <div className="flex justify-between items-center mb-2">
                            <span className="font-medium text-base-content">{g.goal_type}</span>
                            <span className="text-sm text-base-content/70">Target: {g.target_value} {g.unit || ""}</span>
                        </div>
                        <div className="w-full bg-base-300 rounded-full h-3 overflow-hidden">
                            <motion.div
                                className="h-3 rounded-full bg-gradient-to-r from-pink-500 to-purple-500"
                                style={{ width: `${progress}%` }}
                                initial={{ width: 0 }}
                                animate={{ width: `${progress}%` }}
                                transition={{ duration: 1, ease: "easeOut" }}
                            />
                        </div>
                    </motion.div>
                );
            })}

            {weeklyGoals.map((g, i) => (
                <motion.div
                    key={`weekly-${g.id}`}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.15 }}
                    className="bg-base-200/60 dark:bg-base-300/60 rounded-xl p-4 shadow-md border border-base-300 flex justify-between items-center transition-colors duration-300"
                >
                    <span className="font-medium text-base-content">{g.goal_name}</span>
                    <input
                        type="checkbox"
                        checked={!!g.is_completed}
                        onChange={() => toggleWeeklyGoal(g.id!)}
                        className="w-5 h-5 accent-pink-500"
                    />
                </motion.div>
            ))}

            {!loading && longGoals.length === 0 && weeklyGoals.length === 0 && !error && (
                <div className="text-center text-base-content/70">You don’t have any goals yet.</div>
            )}
        </div>
    );
};

export default GoalsComponent;
