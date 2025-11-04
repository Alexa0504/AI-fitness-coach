import React, {useEffect, useState} from "react";
import {motion} from "framer-motion";

interface Goal {
    id: number;
    goal_type: string;
    target_value: number;
    unit?: string;
}

const GoalsComponent: React.FC = () => {
    const [goals, setGoals] = useState<Goal[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const fetchGoals = async () => {
        setLoading(true);
        setError(null);

        const token = localStorage.getItem("authToken");
        if (!token) {
            setError("Please log in to view your goals.");
            setLoading(false);
            return;
        }

        try {
            const response = await fetch("http://localhost:5000/api/goals/", {
                headers: {
                    "Authorization": `Bearer ${token}`,
                },
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || "Failed to fetch goals.");
            }

            setGoals(data);
        } catch (err: any) {
            console.error(err);
            setError(err.message || "Error fetching goals.");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchGoals();
    }, []);

    return (
        <div className="space-y-6">
            {error && (
                <div className="p-3 rounded-lg bg-red-500/20 text-red-300 border border-red-500/40">
                    {error}
                </div>
            )}

            {loading && (
                <div className="text-center text-base-content/70">Loading goals...</div>
            )}

            {!loading && goals.length === 0 && !error && (
                <div className="text-center text-base-content/70">
                    You don’t have any goals yet.
                </div>
            )}

            {goals.map((g, i) => {
                const progress = Math.min((Math.random() * 100), 100); // 🔹 ide tehetsz valós current progress logikát, ha lesz ilyen meződ
                return (
                    <motion.div
                        key={g.id}
                        initial={{opacity: 0, y: 10}}
                        animate={{opacity: 1, y: 0}}
                        transition={{delay: i * 0.15}}
                        className="bg-base-200/60 dark:bg-base-300/60 rounded-xl p-4 shadow-md border border-base-300 transition-colors duration-300"
                    >
                        <div className="flex justify-between items-center mb-2">
              <span className="font-medium text-base-content">
                {g.goal_type}
              </span>
                            <span className="text-sm text-base-content/70">
                Target: {g.target_value} {g.unit || ""}
              </span>
                        </div>
                        <div className="w-full bg-base-300 rounded-full h-3 overflow-hidden">
                            <motion.div
                                className="h-3 rounded-full bg-gradient-to-r from-pink-500 to-purple-500"
                                style={{width: `${progress}%`}}
                                initial={{width: 0}}
                                animate={{width: `${progress}%`}}
                                transition={{duration: 1, ease: "easeOut"}}
                            />
                        </div>
                    </motion.div>
                );
            })}
        </div>
    );
};

export default GoalsComponent;
