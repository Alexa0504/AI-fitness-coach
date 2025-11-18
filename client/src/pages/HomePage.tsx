import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import ThemeSwitcher from "../components/ThemeSwitcher.tsx";
import { useTheme } from "../components/ThemeContext.tsx";
import AiPlanCard, { type Plan, type Day, type MealDay } from "../components/AIPlanComponent.tsx";
import GamificationCard from "../components/StatComponent.tsx";
import GoalsCard from "../components/GoalsComponent.tsx";
import Taskbar from "../components/Taskbar.tsx";
import { motion } from "framer-motion";

const ProgressIndicator: React.FC<{ title: string; progress: number }> = ({ title, progress }) => {
    return (
        <div className="w-full">
            <div className="flex justify-between items-center mb-1">
                <span className="text-sm font-semibold text-base-content/80">{title}:</span>
                <span className="text-sm font-bold text-base-content">{progress}%</span>
            </div>
            <Taskbar progress={progress} />
        </div>
    );
};

const HeaderBar: React.FC = () => {
    const navigate = useNavigate();
    const handleLogout = async () => {
        const token = localStorage.getItem("authToken");
        if (!token) {
            navigate("/login");
            return;
        }
        try {
            const res = await fetch("http://localhost:5000/api/auth/logout", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            });
            if (res.ok) {
                localStorage.removeItem("authToken");
                localStorage.removeItem("user");
                navigate("/login");
            }
        } catch (error) {
            console.error("Logout error:", error);
        }
    };
    return (
        <header className="sticky top-0 z-20 w-full bg-base-100/70 dark:bg-base-300/50 backdrop-blur-lg shadow-md border-b border-base-300 transition-colors duration-300">
            <div className="max-w-7xl mx-auto flex flex-wrap justify-between items-center px-4 sm:px-6 py-3 gap-3">
                <h1 className="text-xl sm:text-2xl font-extrabold bg-gradient-to-r from-purple-500 to-pink-400 bg-clip-text text-transparent drop-shadow-md dark:from-purple-300 dark:to-pink-200 transition-colors duration-300">
                    AI Fitness Coach
                </h1>
                <div className="flex items-center gap-2 sm:gap-4">
                    <button
                        onClick={() => navigate("/profile")}
                        className="px-3 sm:px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg font-semibold shadow-md hover:shadow-indigo-400/30 transition-all duration-200 text-sm sm:text-base"
                    >
                        Profile
                    </button>
                    <div className="flex items-center justify-center">
                        <ThemeSwitcher />
                    </div>
                    <button
                        onClick={handleLogout}
                        className="px-3 sm:px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg font-semibold shadow-md hover:shadow-indigo-400/30 transition-all duration-200 text-sm sm:text-base"
                    >
                        Logout
                    </button>
                </div>
            </div>
        </header>
    );
};

const DashboardSection: React.FC<{ title: string; children: React.ReactNode }> = ({ title, children }) => (
    <motion.section
        initial={{ opacity: 0, y: 25 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
        className="p-6 rounded-2xl shadow-2xl border border-base-300 bg-base-100/90 dark:bg-base-200/80 backdrop-blur-md hover:shadow-[0_0_25px_rgba(255,255,255,0.15)] transition-all duration-300"
    >
        <h2 className="text-2xl font-bold text-base-content mb-4 border-b border-base-300 pb-2 transition-colors duration-300">
            {title}
        </h2>
        <div className="text-base-content transition-colors duration-300">{children}</div>
    </motion.section>
);

const Footer: React.FC = () => (
    <footer className="py-6 text-center text-sm text-white/80 dark:text-gray-400 mt-10 transition-colors duration-300">
        © {new Date().getFullYear()} AI Planner. All rights reserved.
    </footer>
);

const HomePage: React.FC = () => {
    const { theme } = useTheme();
    const [workoutProgress, setWorkoutProgress] = useState(0);
    const [dietProgress, setDietProgress] = useState(0);
    const [overallPerformance, setOverallPerformance] = useState(0);

    const hasProgress = workoutProgress > 0 || dietProgress > 0 || overallPerformance > 0;


    useEffect(() => {
        const token = localStorage.getItem("authToken");
        if (!token) return;

        const fetchLatestPlans = async () => {
            try {
                const res = await fetch("http://localhost:5000/api/plans/latest", {
                    headers: { Authorization: `Bearer ${token}` },
                });
                if (!res.ok) throw new Error("Failed to fetch plans");
                const data = await res.json();

                const workoutPlan = data.plans.find((p: Plan) => p.plan_type === "workout");
                const dietPlan = data.plans.find((p: Plan) => p.plan_type === "diet");

                const calculateProgress = (plan: Plan | undefined) => {
                    if (!plan) return 0;
                    if (plan.plan_type === "workout" && plan.days) {
                        const total = plan.days.length;
                        const completed = plan.days.filter((d: Day) => d.completed).length;
                        return total ? Math.round((completed / total) * 100) : 0;
                    } else if (plan.plan_type === "diet" && plan.meals) {
                        const total = plan.meals.length * 3;
                        let completed = 0;
                        plan.meals.forEach((m: MealDay) => {
                            if (m.breakfast_completed) completed++;
                            if (m.lunch_completed) completed++;
                            if (m.dinner_completed) completed++;
                        });
                        return total ? Math.round((completed / total) * 100) : 0;
                    }
                    return 0;
                };

                const wp = calculateProgress(workoutPlan);
                const dp = calculateProgress(dietPlan);
                setWorkoutProgress(wp);
                setDietProgress(dp);
                setOverallPerformance(Math.round((wp + dp) / 2));
            } catch (err) {
                console.error("Error fetching latest plans:", err);
            }
        };

        fetchLatestPlans();
    }, []);


    const handlePlanUpdate = (plan: Plan, type: "workout" | "diet") => {
        let total = 0;
        let completed = 0;

        if (type === "workout" && plan.days) {
            total = plan.days.length;
            completed = plan.days.filter((d: Day) => d.completed).length;
        } else if (type === "diet" && plan.meals) {
            total = plan.meals.length * 3;
            completed = plan.meals.reduce((sum: number, day: MealDay) => {
                let dayCompleted = 0;
                if (day.breakfast_completed) dayCompleted++;
                if (day.lunch_completed) dayCompleted++;
                if (day.dinner_completed) dayCompleted++;
                return sum + dayCompleted;
            }, 0);
        }

        const calculatedProgress = total > 0 ? Math.round((completed / total) * 100) : 0;

        if (type === "workout") setWorkoutProgress(calculatedProgress);
        if (type === "diet") setDietProgress(calculatedProgress);

        const wp = type === "workout" ? calculatedProgress : workoutProgress;
        const dp = type === "diet" ? calculatedProgress : dietProgress;
        setOverallPerformance(Math.round((wp + dp) / 2));
    };

    return (
        <div className={`relative min-h-screen ${theme} transition-colors duration-500`}>
            <div className="absolute inset-0 bg-gradient-to-br from-purple-600 via-pink-500 to-blue-500 dark:from-gray-900 dark:via-gray-800 dark:to-black transition-colors duration-500" />
            <div className="absolute inset-0 bg-black/10 dark:bg-black/50 backdrop-blur-[1px] transition-colors duration-500" />
            <div className="relative z-10">
                <HeaderBar />
                <main className="max-w-7xl mx-auto px-6 py-10">
                    <motion.h1
                        initial={{ opacity: 0, y: -20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.7 }}
                        className="text-4xl font-extrabold text-white dark:text-gray-100 mb-10 text-center sm:text-left drop-shadow-[0_3px_5px_rgba(0,0,0,0.3)] transition-colors duration-500"
                    >
                        Dashboard
                    </motion.h1>
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                        <div className="lg:col-span-2 space-y-8">
                            <DashboardSection title="Your Goals and Progress">
                                <GoalsCard />
                                <div className="mt-6 pt-6 border-t border-base-300">
                                    {!hasProgress ? (
                                        <div className="text-center py-4 text-base-content/60 italic">
                                            No Plan Progress Yet. Start your workout or log a meal to see your progress!
                                        </div>
                                    ) : (
                                        <div className="space-y-4">
                                            <ProgressIndicator
                                                title="Workout Plan Progress"
                                                progress={workoutProgress}
                                            />
                                            <ProgressIndicator title="Diet Plan Progress" progress={dietProgress} />
                                            <ProgressIndicator
                                                title="Overall Combined Progress"
                                                progress={overallPerformance}
                                            />
                                        </div>
                                    )}
                                </div>
                            </DashboardSection>

                            <DashboardSection title="AI Workout and Diet Plan">
                                <AiPlanCard onPlanUpdate={handlePlanUpdate} />
                            </DashboardSection>
                        </div>
                        <aside className="lg:col-span-1 space-y-8">
                            <DashboardSection title="Statistics and Score">
                                <GamificationCard performance={overallPerformance} />
                            </DashboardSection>
                        </aside>
                    </div>
                </main>
                <Footer />
            </div>
        </div>
    );
};

export default HomePage;
