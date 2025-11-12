import React from "react";
import { motion } from "framer-motion";

export interface WeeklyGoal {
    id: number;
    goal_name: string;
    mon: boolean;
    tue: boolean;
    wed: boolean;
    thu: boolean;
    fri: boolean;
    sat: boolean;
    sun: boolean;
    progress: number;
}

interface WeeklyGoalsProps {
    goals: WeeklyGoal[];
    toggleDay: (
        goalId: number,
        day: keyof Omit<WeeklyGoal, "id" | "goal_name" | "progress">
    ) => void;
}

const WeeklyGoals: React.FC<WeeklyGoalsProps> = ({ goals, toggleDay }) => {
    if (goals.length === 0) return <div>No weekly goals yet.</div>;

    return (
        <div className="space-y-4">
            {goals.map((g) => (
                <motion.div
                    key={g.id}
                    className="p-4 bg-base-200 rounded-xl shadow-md border border-base-300"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                >
                    <div className="flex justify-between items-center mb-2">
                        <span className="font-medium">{g.goal_name}</span>
                        <span>{Math.round(g.progress)}%</span>
                    </div>
                    <div className="w-full bg-base-300 rounded-full h-3 overflow-hidden mb-2">
                        <motion.div
                            className="h-3 rounded-full bg-gradient-to-r from-pink-500 to-purple-500"
                            style={{ width: `${g.progress}%` }}
                            initial={{ width: 0 }}
                            animate={{ width: `${g.progress}%` }}
                            transition={{ duration: 0.3 }}
                        />
                    </div>
                    <div className="grid grid-cols-7 gap-2">
                        {(["mon","tue","wed","thu","fri","sat","sun"] as const).map((day) => (
                            <label key={day} className="flex flex-col items-center">
                                <input
                                    type="checkbox"
                                    checked={g[day]}
                                    onChange={() => toggleDay(g.id, day)}
                                    className="w-5 h-5 accent-pink-500"
                                />
                                <span className="text-xs">{day.toUpperCase()}</span>
                            </label>
                        ))}
                    </div>
                </motion.div>
            ))}
        </div>
    );
};

export default WeeklyGoals;
