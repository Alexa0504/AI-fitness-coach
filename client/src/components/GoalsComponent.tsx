import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import WeeklyGoals, {type WeeklyGoal } from "./WeeklyGoalsComponent.tsx";

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
    const [weeklyGoals, setWeeklyGoals] = useState<WeeklyGoal[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const token = localStorage.getItem("authToken") || "";

    const calculateProgress = (goal: WeeklyGoal) => {
        const days = ["mon","tue","wed","thu","fri","sat","sun"] as const;
        const completed = days.filter(day => goal[day]).length;
        return (completed / days.length) * 100;
    };

    const fetchLongGoals = async () => {
        const res = await fetch("http://localhost:5000/api/goals/", {
            headers: { Authorization: `Bearer ${token}` },
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.message || "Failed to fetch goals.");
        setLongGoals(data);
    };

    const fetchWeeklyGoals = async () => {
        const res = await fetch("http://localhost:5000/api/weekly-goals/", {
            headers: { Authorization: `Bearer ${token}` },
        });
        const data: WeeklyGoal[] = await res.json();
        if (!res.ok) throw new Error("Failed to fetch weekly goals.");
        // számítsuk ki a progress-t frontend oldalon is
        const updated = data.map(g => ({ ...g, progress: calculateProgress(g) }));
        setWeeklyGoals(updated);
    };

    const toggleWeeklyGoalDay = (
        goalId: number,
        day: keyof Omit<WeeklyGoal, "id" | "goal_name" | "progress">
    ) => {
        // 1. Frontend frissítés azonnal
        setWeeklyGoals(prev =>
            prev.map(g => {
                if (g.id === goalId) {
                    const updatedGoal = { ...g, [day]: !g[day] };
                    return { ...updatedGoal, progress: calculateProgress(updatedGoal) };
                }
                return g;
            })
        );

        // 2. Backend frissítés
        fetch(`http://localhost:5000/api/weekly-goals/${goalId}/toggle/${day}`, {
            method: "PATCH",
            headers: { Authorization: `Bearer ${token}` },
        });
    };

    useEffect(() => {
        const fetchAll = async () => {
            setLoading(true);
            try {
                await fetchLongGoals();
                await fetchWeeklyGoals();
            } catch (e) {
                const msg = e instanceof Error ? e.message : "Error fetching goals.";
                setError(msg);
            } finally {
                setLoading(false);
            }
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

            <WeeklyGoals goals={weeklyGoals} toggleDay={toggleWeeklyGoalDay} />

            {!loading && longGoals.length === 0 && weeklyGoals.length === 0 && !error && (
                <div className="text-center text-base-content/70">You don’t have any goals yet.</div>
            )}
        </div>
    );
};

export default GoalsComponent;