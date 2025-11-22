import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import ThemeSwitcher from "../components/ThemeSwitcher";
import { useTheme } from "../components/ThemeContext";
import AiPlanCard, { type Plan } from "../components/AIPlanComponent";
import GamificationCard from "../components/StatComponent";
import GoalsCard from "../components/GoalsComponent";
import Taskbar from "../components/Taskbar";
import { motion } from "framer-motion";


type WorkoutDay = { completed: boolean };
type MealDay = { breakfast_completed: boolean; lunch_completed: boolean; dinner_completed: boolean };

const ProgressIndicator: React.FC<{ title: string; progress: number }> = ({ title, progress }) => (
    <div className="w-full">
        <div className="flex justify-between items-center mb-1">
            <span className="text-sm font-semibold text-base-content/80">{title}:</span>
            <span className="text-sm font-bold text-base-content">{progress}%</span>
        </div>
        <Taskbar progress={progress} />
    </div>
);

const HeaderBar: React.FC = () => {
    const navigate = useNavigate();
    const handleLogout = async () => {
        const token = localStorage.getItem("authToken");
        if (!token) { navigate("/login"); return; }

        try {
            const res = await fetch("http://localhost:5000/api/auth/logout", {
                method: "POST",
                headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
            });
            if (res.ok) {
                localStorage.removeItem("authToken");
                localStorage.removeItem("user");
                navigate("/login");
            }
        } catch {
            console.error("Logout error");
        }
    };

    return (
        <header className="sticky top-0 z-20 w-full bg-base-100/70 dark:bg-base-300/50 backdrop-blur-lg shadow-md border-b border-base-300 transition-colors duration-300">
            <div className="max-w-7xl mx-auto flex flex-wrap justify-between items-center px-4 sm:px-6 py-3 gap-3">
                <h1 className="text-xl sm:text-2xl font-extrabold bg-gradient-to-r from-purple-500 to-pink-400 bg-clip-text text-transparent drop-shadow-md dark:from-purple-300 dark:to-pink-200 transition-colors duration-300">AI Fitness Coach</h1>
                <div className="flex items-center gap-2 sm:gap-4">
                    <button onClick={() => navigate("/profile")} className="px-3 sm:px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg font-semibold shadow-md hover:shadow-indigo-400/30 transition-all duration-200 text-sm sm:text-base">Profile</button>
                    <div className="flex items-center justify-center"><ThemeSwitcher /></div>
                    <button onClick={handleLogout} className="px-3 sm:px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg font-semibold shadow-md hover:shadow-indigo-400/30 transition-all duration-200 text-sm sm:text-base">Logout</button>
                </div>
            </div>
        </header>
    );
};

const DashboardSection: React.FC<{ title: string; children: React.ReactNode }> = ({ title, children }) => (
    <motion.section initial={{ opacity: 0, y: 25 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6, ease: "easeOut" }} className="p-6 rounded-2xl shadow-2xl border border-base-300 bg-base-100/90 dark:bg-base-200/80 backdrop-blur-md hover:shadow-[0_0_25px_rgba(255,255,255,0.15)] transition-all duration-300">
        <h2 className="text-2xl font-bold text-base-content mb-4 border-b border-base-300 pb-2 transition-colors duration-300">{title}</h2>
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
    const [workoutDays, setWorkoutDays] = useState<WorkoutDay[]>([]);
    const [dietMeals, setDietMeals] = useState<MealDay[]>([]);
    const [workoutProgress, setWorkoutProgress] = useState<number>(0);
    const [dietProgress, setDietProgress] = useState<number>(0);
    const [overallPerformance, setOverallPerformance] = useState<number>(0);
    const [xp, setXp] = useState<number>(0);
    const [level, setLevel] = useState<number>(1);
    const [xpToNext, setXpToNext] = useState<number>(0);

    const fetchBackendStats = async () => {
        const token = localStorage.getItem("authToken");
        if (!token) return;

        try {
            const xpRes = await fetch("http://localhost:5000/api/xp/status", { headers: { Authorization: `Bearer ${token}` } });
            if (xpRes.ok) {
                const data = await xpRes.json();
                setXp(data.xp ?? 0);
                setLevel(data.level ?? 1);
                setXpToNext(data.xpToNext ?? 0);
            }
        } catch {
            console.error("Failed to load XP stats");
        }

        try {
            const progRes = await fetch("http://localhost:5000/api/progress/status", { headers: { Authorization: `Bearer ${token}` } });
            if (progRes.ok) {
                const data = await progRes.json();
                setWorkoutDays(data.workoutDays ?? []);
                setDietMeals(data.dietMeals ?? []);
                calculateProgress(data.workoutDays ?? [], data.dietMeals ?? []);
            }
        } catch {
            console.error("Failed to load progress stats");
        }
    };

    const calculateProgress = (workoutList: WorkoutDay[] = workoutDays, dietList: MealDay[] = dietMeals) => {
        const workoutTotal = workoutList.length;
        const workoutCompleted = workoutList.filter(d => d.completed).length;

        const dietTotal = dietList.length * 3;
        const dietCompleted = dietList.reduce((sum, day) =>
            sum + (day.breakfast_completed ? 1 : 0) + (day.lunch_completed ? 1 : 0) + (day.dinner_completed ? 1 : 0), 0
        );

        const newWorkoutProgress = workoutTotal ? Math.round((workoutCompleted / workoutTotal) * 100) : 0;
        const newDietProgress = dietTotal ? Math.round((dietCompleted / dietTotal) * 100) : 0;

        setWorkoutProgress(newWorkoutProgress);
        setDietProgress(newDietProgress);
        setOverallPerformance(Math.round((newWorkoutProgress + newDietProgress) / 2));
    };

    const handlePlanUpdate = (plan: Plan, type: "workout" | "diet") => {
        if (type === "workout" && plan.days) {
            setWorkoutDays(plan.days);
            calculateProgress(plan.days, dietMeals);
        }
        if (type === "diet" && plan.meals) {
            setDietMeals(plan.meals);
            calculateProgress(workoutDays, plan.meals);
        }
        setXp(prev => prev + 10);
    };

    const handlePlansLoaded = (loadedPlans: { workout?: Plan; diet?: Plan }) => {
        const newWorkout = loadedPlans.workout?.days ?? workoutDays;
        const newDiet = loadedPlans.diet?.meals ?? dietMeals;
        setWorkoutDays(newWorkout);
        setDietMeals(newDiet);
        calculateProgress(newWorkout, newDiet);
    };

    const hasProgress = workoutProgress > 0 || dietProgress > 0 || overallPerformance > 0;

    useEffect(() => { fetchBackendStats(); }, []);

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
                                            <ProgressIndicator title="Workout Plan Progress" progress={workoutProgress} />
                                            <ProgressIndicator title="Diet Plan Progress" progress={dietProgress} />
                                            <ProgressIndicator title="Overall Combined Progress" progress={overallPerformance} />
                                        </div>
                                    )}
                                </div>
                            </DashboardSection>

                            <DashboardSection title="AI Workout and Diet Plan">
                                <AiPlanCard onPlanUpdate={handlePlanUpdate} onPlansLoaded={handlePlansLoaded} />
                            </DashboardSection>
                        </div>

                        <aside className="lg:col-span-1 space-y-8">
                            <DashboardSection title="Statistics and Score">
                                <GamificationCard performance={overallPerformance} xp={xp} level={level} xpToNext={xpToNext} />
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
