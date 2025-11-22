import React, { useState, useEffect } from "react";

const API_URL = "http://localhost:5000/api/plans/";
const API_LATEST_URL = "http://localhost:5000/api/plans/latest";

interface Exercise { name: string; sets?: number; reps?: number; duration_min?: number }
export interface Day { day: number; title?: string; exercises?: Exercise[]; completed: boolean }
export interface MealDay { day: number; breakfast: string; lunch: string; dinner: string; snack?: string; breakfast_completed: boolean; lunch_completed: boolean; dinner_completed: boolean }
export interface Plan { id?: number; plan_name: string; plan_type: "workout" | "diet"; duration_days: number; days?: Day[]; meals?: MealDay[]; note?: string; progress?: number }

interface ApiPlanResponse { id?: number; plan_type: "workout" | "diet"; content: string | { days?: Day[]; meals?: MealDay[]; note?: string }; plan_name?: string; duration_days?: number; note?: string }
type PlanDraft = Omit<Plan, 'plan_name' | 'duration_days'> & Partial<Pick<Plan, 'plan_name' | 'duration_days'>>
interface AiPlanCardProps { onPlanUpdate?: (plan: Plan, type: "workout" | "diet") => void; onPlansLoaded?: (plans: { workout?: Plan; diet?: Plan }) => void; onXpUpdate?: (xp: number, level: number, xpToNext: number) => void; }

const AiPlanCard: React.FC<AiPlanCardProps> = ({ onPlanUpdate, onPlansLoaded, onXpUpdate }) => {
    const [plans, setPlans] = useState<{ workout?: Plan; diet?: Plan }>({});
    const [activeType, setActiveType] = useState<"workout" | "diet">("workout");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const token = localStorage.getItem("authToken");

    const calculateProgress = (plan: Plan): number => {
        if (plan.plan_type === "workout" && plan.days) {
            const total = plan.days.length;
            const completed = plan.days.filter(d => d.completed).length;
            return total ? Math.round((completed / total) * 100) : 0;
        } else if (plan.plan_type === "diet" && plan.meals) {
            const total = plan.meals.length * 3;
            let completed = 0;
            plan.meals.forEach(m => { if (m.breakfast_completed) completed++; if (m.lunch_completed) completed++; if (m.dinner_completed) completed++; });
            return total ? Math.round((completed / total) * 100) : 0;
        }
        return 0;
    };

    useEffect(() => {
        const fetchLatestPlans = async () => {
            if (!token) return;
            try {
                const res = await fetch(API_LATEST_URL, { headers: { Authorization: `Bearer ${token}` } });
                if (!res.ok) throw new Error("Failed to load latest plans.");
                const data: { plans: ApiPlanResponse[] } = await res.json();
                const loadedPlans: { workout?: Plan; diet?: Plan } = {};
                data.plans?.forEach(p => {
                    const parsed = typeof p.content === "string" ? JSON.parse(p.content) : p.content;
                    const fullPlanDraft: PlanDraft = { ...p, ...parsed };
                    const fullPlan: Plan = {
                        ...fullPlanDraft,
                        plan_name: fullPlanDraft.plan_name || `Default ${p.plan_type} Plan`,
                        duration_days: fullPlanDraft.duration_days || 7
                    } as Plan;
                    fullPlan.progress = calculateProgress(fullPlan);
                    loadedPlans[p.plan_type] = fullPlan;
                });
                setPlans(prev => ({
                    workout: prev.workout || loadedPlans.workout,
                    diet: prev.diet || loadedPlans.diet
                }));
                onPlansLoaded?.(loadedPlans);
            } catch (e: unknown) { setError(e instanceof Error ? e.message : String(e)); }
        };
        fetchLatestPlans();
    }, [token, onPlansLoaded]);

    const handleGenerateNewPlan = async () => {
        if (!token) { setError("Please log in first."); return; }
        setLoading(true); setError(null);
        try {
            const res = await fetch(API_URL, {
                method: "POST",
                headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
                body: JSON.stringify({ plan_type: activeType })
            });
            if (!res.ok) {
                const errData = await res.json().catch(() => ({}));
                throw new Error(errData.message || "Error generating plan.");
            }
            const data: { plan: ApiPlanResponse } = await res.json();
            const contentObject = typeof data.plan.content === "string" ? JSON.parse(data.plan.content) : data.plan.content;
            const parsedContent = contentObject as { days?: Day[]; meals?: MealDay[]; note?: string; plan_name?: string; duration_days?: number };

            const fullPlanDraft: PlanDraft = { ...data.plan, ...parsedContent };
            const fullPlan: Plan = {
                ...fullPlanDraft,
                plan_name: fullPlanDraft.plan_name || `New ${activeType} Plan`,
                duration_days: fullPlanDraft.duration_days || 7,
                days: parsedContent.days?.map(d => ({ ...d, completed: false })),
                meals: parsedContent.meals?.map(m => ({
                    ...m,
                    breakfast_completed: false,
                    lunch_completed: false,
                    dinner_completed: false
                })) || Array.from({ length: 7 }, (_, i) => ({
                    day: i + 1,
                    breakfast: "",
                    lunch: "",
                    dinner: "",
                    snack: "",
                    breakfast_completed: false,
                    lunch_completed: false,
                    dinner_completed: false
                })),
                progress: 0
            } as Plan;

            setPlans(prev => ({ ...prev, [activeType]: fullPlan }));
            onPlanUpdate?.({ ...fullPlan, progress: 0 }, activeType);
        } catch (err: unknown) { setError(err instanceof Error ? err.message : String(err)); }
        finally { setLoading(false); }
    };

    const handleToggle = async (day: number, meal?: "breakfast" | "lunch" | "dinner") => {
        const plan = plans[activeType];
        if (!plan) return;

        const updatedPlan: Plan = { ...plan };

        if (activeType === "workout" && plan.days) {
            updatedPlan.days = plan.days.map(d => {
                if (d.day !== day) return d;
                if (d.completed) return d;
                return { ...d, completed: true };
            });
        } else if (activeType === "diet" && plan.meals && meal) {
            updatedPlan.meals = updatedPlan.meals?.map(m => {
                if (m.day !== day) return m;
                const key = `${meal}_completed` as keyof MealDay;
                if (m[key]) return m;
                return { ...m, [key]: true };
            }) as MealDay[];
        }

        updatedPlan.progress = calculateProgress(updatedPlan);
        setPlans(prev => ({ ...prev, [activeType]: updatedPlan }));
        onPlanUpdate?.(updatedPlan, activeType);

        if (!plan.id) return;
        const toggleType: "workout_day" | "diet_meal" = activeType === "workout" ? "workout_day" : "diet_meal";

        try {
            const toggleRes = await fetch(`${API_URL}${plan.id}/toggle`, {
                method: "PATCH",
                headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
                body: JSON.stringify({ type: toggleType, day, meal })
            });
            if (toggleRes.ok) {
                const toggleData = await toggleRes.json();
                const xpData = toggleData.xp;
                if (xpData) onXpUpdate?.(xpData.xp, xpData.level, xpData.xpToNext);
            }
        } catch (e) { console.error("Error updating progress or XP", e); }
    };

    const defaultPlans = {
        workout: { plan_name: "7-Day Beginner Workout Plan", plan_type: "workout" as const, duration_days: 7, days: Array.from({ length: 7 }, (_, i) => ({ day: i + 1, title: `Workout Day ${i + 1}`, exercises: [], completed: false })), progress: 0 },
        diet: { plan_name: "7-Day Sample Diet Plan", plan_type: "diet" as const, duration_days: 7, meals: Array.from({ length: 7 }, (_, i) => ({ day: i + 1, breakfast: "", lunch: "", dinner: "", snack: "", breakfast_completed: false, lunch_completed: false, dinner_completed: false })), progress: 0 },
    };

    const plan: Plan = plans[activeType] || defaultPlans[activeType];
    const currentProgress = plan.progress ?? 0;

    return (
        <div className="space-y-6">
            {error && <div className="p-3 rounded-lg bg-red-500/20 text-red-300 border border-red-500/40">{error}</div>}
            <div className="flex gap-3">
                <button onClick={() => setActiveType("workout")} className={`btn flex-1 ${activeType === "workout" ? "btn-primary" : "btn-outline"}`}>🏋️ Workout</button>
                <button onClick={() => setActiveType("diet")} className={`btn flex-1 ${activeType === "diet" ? "btn-primary" : "btn-outline"}`}>🥗 Diet</button>
            </div>
            <div className="bg-base-200/70 p-4 rounded-xl border border-base-300 shadow-md text-base-content space-y-4">
                <h3 className="text-xl font-bold">{plan.plan_name}</h3>
                <p className="text-sm opacity-80">Duration: {plan.duration_days} days</p>
                <div className="h-2 w-full bg-base-300 rounded-full overflow-hidden">
                    <div className="h-full bg-gradient-to-r from-pink-500 to-purple-500" style={{ width: `${currentProgress}%` }}></div>
                </div>

                {activeType === "workout" && plan.days && plan.days.map((day, idx) => (
                    <div key={idx} className="p-3 rounded-lg bg-base-300/60 border border-base-300">
                        <div className="flex items-center justify-between">
                            <h4 className="font-semibold">Day {day.day}: {day.title}</h4>
                            <label className="flex items-center gap-2">
                                <input type="checkbox" checked={day.completed} onChange={() => handleToggle(day.day)} /> Done
                            </label>
                        </div>
                        <ul className="mt-2 space-y-1 text-sm">{day.exercises?.map((ex, i) => <li key={i}>{ex.name} — {ex.sets || ""}x{ex.reps || ""} {ex.duration_min && `(${ex.duration_min} min)`}</li>)}</ul>
                    </div>
                ))}

                {activeType === "diet" && plan.meals && plan.meals.map((day, idx) => (
                    <div key={idx} className="p-3 rounded-lg bg-base-300/60 border border-base-300">
                        <h4 className="font-semibold">Day {day.day}</h4>
                        <div className="mt-1 text-sm space-y-1">
                            {(["breakfast", "lunch", "dinner"] as const).map(meal => (
                                <label key={meal} className="flex items-center justify-between">
                                    <span>🍽️ <span className="font-medium">{meal.charAt(0).toUpperCase() + meal.slice(1)}:</span> {day[meal]}</span>
                                    <input type="checkbox" checked={Boolean(day[`${meal}_completed`])} onChange={() => handleToggle(day.day, meal)} />
                                </label>
                            ))}
                        </div>
                    </div>
                ))}
            </div>

            <button onClick={handleGenerateNewPlan} disabled={loading} className="btn btn-primary w-full max-w-sm text-lg">{loading ? "Generating..." : "Request new AI plan!"}</button>
        </div>
    );
};

export default AiPlanCard;
