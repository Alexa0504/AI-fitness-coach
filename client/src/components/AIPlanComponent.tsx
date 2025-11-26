
import React, { useState, useEffect } from "react";

const API_URL = "http://localhost:5000/api/plans/";
const API_LATEST_URL = "http://localhost:5000/api/plans/latest";


interface Exercise {
    name: string;
    sets?: number;
    reps?: number;
    duration_min?: number;
}

export interface Day {
    day: number;
    title?: string;
    exercises?: Exercise[];
    completed: boolean;
}

export interface MealDay {
    day: number;
    breakfast: string;
    lunch: string;
    dinner: string;
    snack?: string;
    breakfast_completed: boolean;
    lunch_completed: boolean;
    dinner_completed: boolean;
}

export interface Plan {
    id?: number;
    plan_name: string;
    plan_type: "workout" | "diet";
    duration_days: number;
    days?: Day[];
    meals?: MealDay[];
    note?: string;
    progress?: number;
}

interface ApiPlanResponse {
    id?: number;
    plan_type: "workout" | "diet";
    content: string | { days?: Day[]; meals?: MealDay[]; note?: string };
    plan_name?: string;
    duration_days?: number;
    note?: string;
}

interface AiPlanCardProps {
    workoutPlan?: Plan | null;
    dietPlan?: Plan | null;
    onPlanUpdate?: (plan: Plan, type: "workout" | "diet") => void;
    onPlansLoaded?: (plans: { workout?: Plan; diet?: Plan }) => void;
    addXp: (xp: number) => void;
    xp: number;
    level: number;
}

const AiPlanCard: React.FC<AiPlanCardProps> = ({
                                                   workoutPlan,
                                                   dietPlan,
                                                   onPlanUpdate,
                                                   onPlansLoaded,
                                                   addXp,

                                               }) => {
    const [activeType, setActiveType] = useState<"workout" | "diet">("workout");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const token = localStorage.getItem("authToken");

    const calculateProgress = (plan: Plan): number => {
        if (!plan) return 0;
        if (plan.plan_type === "workout" && plan.days) {
            const total = plan.days.length;
            const completed = plan.days.filter((d) => d.completed).length;
            return total ? Math.round((completed / total) * 100) : 0;
        } else if (plan.plan_type === "diet" && plan.meals) {
            const total = plan.meals.length * 3;
            let completed = 0;
            plan.meals.forEach((m) => {
                if (m.breakfast_completed) completed++;
                if (m.lunch_completed) completed++;
                if (m.dinner_completed) completed++;
            });
            return total ? Math.round((completed / total) * 100) : 0;
        }
        return 0;
    };

    useEffect(() => {
        if (!token) return;

        const fetchData = async () => {
            try {

                const [plansRes] = await Promise.all([
                    fetch(API_LATEST_URL, { headers: { Authorization: `Bearer ${token}` } }),
                ]);

                if (!plansRes.ok) throw new Error("Failed to load latest plans.");

                const plansData: { plans: ApiPlanResponse[] } = await plansRes.json();

                const loadedPlans: { workout?: Plan; diet?: Plan } = {};
                plansData.plans?.forEach((p) => {
                    const parsed = typeof p.content === "string" ? JSON.parse(p.content) : p.content;
                    loadedPlans[p.plan_type] = {
                        id: p.id,
                        plan_type: p.plan_type,
                        plan_name: p.plan_name || `Default ${p.plan_type} Plan`,
                        duration_days: p.duration_days || 7,
                        days: parsed?.days ?? [],
                        meals: parsed?.meals ?? [],
                        note: parsed?.note,
                        progress: calculateProgress({
                            id: p.id,
                            plan_type: p.plan_type,
                            plan_name: "",
                            duration_days: 7,
                            days: parsed?.days,
                            meals: parsed?.meals,
                        }),
                    };
                });

                onPlansLoaded?.(loadedPlans);
            } catch (e: unknown) {
                setError(e instanceof Error ? e.message : String(e));
            }
        };

        fetchData();
    }, [token, onPlansLoaded]);

    const handleGenerateNewPlan = async () => {
        if (!token) {
            setError("Please log in first.");
            return;
        }
        setLoading(true);
        setError(null);

        try {
            const res = await fetch(API_URL, {
                method: "POST",
                headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
                body: JSON.stringify({ plan_type: activeType }),
            });
            if (!res.ok) {
                const errData = await res.json().catch(() => ({}));
                throw new Error(errData.message || "Error generating plan.");
            }

            const data: { plan: ApiPlanResponse } = await res.json();
            const contentObject = typeof data.plan.content === "string" ? JSON.parse(data.plan.content) : data.plan.content;

            const fullPlan: Plan = {
                id: data.plan.id,
                plan_type: data.plan.plan_type,
                plan_name: data.plan.plan_name || `New ${activeType} Plan`,
                duration_days: data.plan.duration_days || 7,
                days: contentObject?.days ?? [],
                meals: contentObject?.meals ?? [],
                note: contentObject?.note,
                progress: 0,
            };

            onPlanUpdate?.(fullPlan, activeType);
        } catch (err: unknown) {
            setError(err instanceof Error ? err.message : String(err));
        } finally {
            setLoading(false);
        }
    };

    const handleToggle = async (day: number, meal?: "breakfast" | "lunch" | "dinner") => {
        const plan = activeType === "workout" ? workoutPlan : dietPlan;
        if (!plan || !plan.id || !token) return;

        const updatedPlan: Plan = { ...plan };

        if (activeType === "workout" && plan.days) {
            updatedPlan.days = plan.days.map(d => d.day === day ? { ...d, completed: true } : d);
        } else if (activeType === "diet" && plan.meals && meal) {
            updatedPlan.meals = plan.meals.map(m =>
                m.day === day ? { ...m, [`${meal}_completed`]: true } : m
            );
        }

        onPlanUpdate?.(updatedPlan, activeType);

        try {
            const res = await fetch(`${API_URL}${updatedPlan.id}/toggle`, {
                method: "PATCH",
                headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
                body: JSON.stringify({
                    type: activeType === "workout" ? "workout_day" : "diet_meal",
                    day,
                    meal: activeType === "diet" ? meal : undefined,
                }),
            });
            if (!res.ok) throw new Error("Failed to update backend.");
            const data = await res.json();

            if (data.xpGained) {
                addXp(data.xpGained);
            }
        } catch (err: unknown) {
            setError(err instanceof Error ? err.message : String(err));
        }
    };

    const defaultPlans = {
        workout: {
            plan_name: "7-Day Beginner Workout Plan",
            plan_type: "workout" as const,
            duration_days: 7,
            days: Array.from({ length: 7 }, (_, i) => ({
                day: i + 1,
                title: `Workout Day ${i + 1}`,
                exercises: [],
                completed: false,
            })),
            progress: 0,
        },
        diet: {
            plan_name: "7-Day Sample Diet Plan",
            plan_type: "diet" as const,
            duration_days: 7,
            meals: Array.from({ length: 7 }, (_, i) => ({
                day: i + 1,
                breakfast: "",
                lunch: "",
                dinner: "",
                snack: "",
                breakfast_completed: false,
                lunch_completed: false,
                dinner_completed: false,
            })),
            progress: 0,
        },
    };

    const plan: Plan = activeType === "workout" ? workoutPlan || defaultPlans.workout : dietPlan || defaultPlans.diet;


    return (
        <div className="space-y-6">

            {}

            {error && (
                <div className="p-3 rounded-lg bg-red-500/20 text-red-300 border border-red-500/40">{error}</div>
            )}
            <div className="flex gap-3">
                <button
                    onClick={() => setActiveType("workout")}
                    className={`btn flex-1 ${activeType === "workout" ? "btn-primary" : "btn-outline"}`}
                >
                    🏋️ Workout
                </button>
                <button
                    onClick={() => setActiveType("diet")}
                    className={`btn flex-1 ${activeType === "diet" ? "btn-primary" : "btn-outline"}`}
                >
                    🥗 Diet
                </button>
            </div>
            <div className="bg-base-200/70 p-4 rounded-xl border border-base-300 shadow-md text-base-content space-y-4">
                <h3 className="text-xl font-bold">{plan.plan_name}</h3>
                <p className="text-sm opacity-80">Duration: {plan.duration_days} days</p>

                {}
                {}

                {activeType === "workout" &&
                    plan.days?.map((day, idx) => (
                        <div key={idx} className="p-3 rounded-lg bg-base-300/60 border border-base-300">
                            <div className="flex items-center justify-between">
                                <h4 className="font-semibold">Day {day.day}: {day.title}</h4>
                                <label className="flex items-center justify-between gap-2">
                                    <span>Done</span>
                                    <input type="checkbox" checked={day.completed} disabled={day.completed} onChange={() => handleToggle(day.day)} />
                                </label>
                            </div>
                            <ul className="mt-2 space-y-1 text-sm">
                                {day.exercises?.map((ex, i) => (
                                    <li key={i}>{ex.name} — {ex.sets || ""}x{ex.reps || ""} {ex.duration_min && `(${ex.duration_min} min)`}</li>
                                ))}
                            </ul>
                        </div>
                    ))}

                {activeType === "diet" &&
                    plan.meals?.map((day, idx) => (
                        <div key={idx} className="p-3 rounded-lg bg-base-300/60 border border-base-300">
                            <h4 className="font-semibold">Day {day.day}</h4>
                            <div className="mt-1 text-sm space-y-1">
                                {(["breakfast", "lunch", "dinner"] as const).map((meal) => (
                                    <label key={meal} className="flex items-center justify-between gap-2">
                                        <span>🍽️ <span className="font-medium">{meal.charAt(0).toUpperCase() + meal.slice(1)}:</span> {day[meal]}</span>
                                        <input type="checkbox" checked={Boolean(day[`${meal}_completed`])} disabled={day[`${meal}_completed`]} onChange={() => handleToggle(day.day, meal)} />
                                    </label>
                                ))}
                            </div>
                        </div>
                    ))}

            </div>

            <button onClick={handleGenerateNewPlan} disabled={loading} className="btn btn-primary w-full max-w-sm text-lg">
                {loading ? "Generating..." : "Request new AI plan!"}
            </button>
        </div>
    );
};

export default AiPlanCard;