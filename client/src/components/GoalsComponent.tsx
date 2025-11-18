import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import Taskbar from "./Taskbar.tsx";
import WeeklyGoals, { type WeeklyGoal } from "./WeeklyGoalsComponent.tsx";

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

    const fetchLongGoals = async () => {
        const res = await fetch("http://localhost:5000/api/goals/", { headers: { Authorization: `Bearer ${token}` } });
        const data = await res.json();
        if (!res.ok) throw new Error(data.message || "Failed to fetch goals.");
        setLongGoals(data);
    };


    const fetchWeeklyGoals = async () => {
        const res = await fetch("http://localhost:5000/api/goals/weekly", { headers: { Authorization: `Bearer ${token}` } });
        const data: WeeklyGoal[] = await res.json();
        if (!res.ok) throw new Error("Failed to fetch weekly goals.");
        setWeeklyGoals(data);
    };

    const calculateWeeklyProgress = (goal: WeeklyGoal) => {
        const days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"] as const;
        const completed = days.filter(d => goal[d]).length;
        return Math.round((completed / days.length) * 100);
    };

    const toggleWeeklyGoal = (
        goalId: number,
        day?: keyof Omit<WeeklyGoal, "id" | "goal_name" | "progress" | "is_completed">
    ) => {
        setWeeklyGoals(prev =>
            prev.map(g => {
                if (g.id === goalId) {
                    const newGoal: WeeklyGoal = { ...g }; // <-- explicit típus
                    if (day) newGoal[day] = !(g[day] ?? false);
                    else newGoal.is_completed = !(g.is_completed ?? false);
                    return newGoal;
                }
                return g;
            })
        );

        if (day) {
            fetch(`http://localhost:5000/api/goals/weekly/${goalId}/toggle?day=${day}`, {
                method: "PATCH",
                headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
            });
        }
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

            {longGoals.map((g, i) => (
                <motion.div
                    key={`long-${g.id}`}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: i * 0.15 }}
                    className="bg-base-200/60 dark:bg-base-300/60 rounded-xl p-4 shadow-md border border-base-300 transition-colors duration-300"
                >
                    <div className="flex justify-between items-center mb-2">
                        <span className="font-medium text-base-content">{g.goal_type}</span>
                        <span className="text-sm text-base-content/70">
              Target: {g.target_value} {g.unit || ""}
            </span>
                    </div>
                    <Taskbar progress={g.is_completed ? 100 : 0} />
                </motion.div>
            ))}

            <WeeklyGoals
                goals={weeklyGoals.map(g => ({ ...g, progress: calculateWeeklyProgress(g) }))}
                toggleDay={toggleWeeklyGoal}
            />

            {!loading && longGoals.length === 0 && weeklyGoals.length === 0 && !error && (
                <div className="text-center text-base-content/70">You don’t have any goals yet.</div>
            )}
        </div>
    );
};

export default GoalsComponent;
