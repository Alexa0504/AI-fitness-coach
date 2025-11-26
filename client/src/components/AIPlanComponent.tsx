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

type PlanDraft = Omit<Plan, "plan_name" | "duration_days"> &
  Partial<Pick<Plan, "plan_name" | "duration_days">>;

interface AiPlanCardProps {
  onPlanUpdate?: (plan: Plan, type: "workout" | "diet") => void;
  onPlansLoaded?: (plans: { workout?: Plan; diet?: Plan }) => void;
  onXpUpdate?: (xp: number, level: number, xpToNext: number) => void;
}

const AiPlanCard: React.FC<AiPlanCardProps> = ({
  onPlanUpdate,
  onPlansLoaded,
  onXpUpdate,
}) => {
  const defaultPlans: { workout: Plan; diet: Plan } = {
    workout: {
      plan_name: "7-Day Beginner Workout Plan",
      plan_type: "workout",
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
      plan_type: "diet",
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

  const [plans, setPlans] = useState<{ workout: Plan; diet: Plan }>(
    defaultPlans
  );
  const [activeType, setActiveType] = useState<"workout" | "diet">("workout");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const token = localStorage.getItem("authToken");

  const calculateProgress = (plan: Plan): number => {
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

  useEffect(() => {
    if (!token) return;

    const fetchLatestPlans = async () => {
      try {
        const res = await fetch(API_LATEST_URL, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!res.ok) return;
        const data = await res.json();

        const loadedPlans: { workout?: Plan; diet?: Plan } = {};
        data.plans?.forEach((p: ApiPlanResponse) => {
          const parsed =
            typeof p.content === "string" ? JSON.parse(p.content) : p.content;
          const fullPlan: Plan = {
            ...p,
            ...parsed,
            plan_name: p.plan_name || `Default ${p.plan_type} Plan`,
            duration_days: p.duration_days || 7,
          };
          fullPlan.progress = calculateProgress(fullPlan);
          loadedPlans[p.plan_type] = fullPlan;
        });

        setPlans((prevPlans) => {
          const workoutPlan = loadedPlans.workout ?? prevPlans.workout;
          const dietPlan = loadedPlans.diet ?? prevPlans.diet;
          const mergedPlans = {
            workout: workoutPlan,
            diet: dietPlan,
          };
          onPlansLoaded?.(mergedPlans);
          return mergedPlans;
        });
      } catch (err) {
        console.error("Error fetching latest plans:", err);
      }
    };

    fetchLatestPlans();
  }, [token, onPlansLoaded]);

  const handleToggle = async (
    day: number,
    meal?: "breakfast" | "lunch" | "dinner"
  ) => {
    const plan = plans[activeType];
    if (!plan) return;

    if (activeType === "workout" && plan.days) {
      const updatedDays = plan.days.map((d: Day) =>
        d.day === day && !d.completed ? { ...d, completed: true } : d
      );
      const updatedPlan = {
        ...plan,
        days: updatedDays,
        progress: calculateProgress({ ...plan, days: updatedDays }),
      };

      setPlans((prevPlans) => ({ ...prevPlans, [activeType]: updatedPlan }));
      onPlanUpdate?.(updatedPlan, activeType);
    } else if (activeType === "diet" && plan.meals && meal) {
      const updatedMeals = plan.meals.map((m: MealDay) =>
        m.day === day && !m[`${meal}_completed`]
          ? { ...m, [`${meal}_completed`]: true }
          : m
      );
      const updatedPlan = {
        ...plan,
        meals: updatedMeals,
        progress: calculateProgress({ ...plan, meals: updatedMeals }),
      };
      setPlans((prevPlans) => ({ ...prevPlans, [activeType]: updatedPlan }));
      onPlanUpdate?.(updatedPlan, activeType);
    }

    if (!plan.id) return;

    const toggleType: "workout_day" | "diet_meal" =
      activeType === "workout" ? "workout_day" : "diet_meal";

    try {
      await fetch(`${API_URL}${plan.id}/toggle`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        credentials: "include",
        body: JSON.stringify({ type: toggleType, day, meal }),
      });
    } catch (e) {
      console.error("Error updating progress or XP", e);
    }
  };

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
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        credentials: "include",
        body: JSON.stringify({ plan_type: activeType }),
      });
      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.message || "Error generating plan.");
      }

      const data: { plan: ApiPlanResponse } = await res.json();
      const parsedContent =
        typeof data.plan.content === "string"
          ? JSON.parse(data.plan.content)
          : data.plan.content;

      const fullPlan: Plan = {
        ...data.plan,
        ...parsedContent,
        plan_name: parsedContent.plan_name || `New ${activeType} Plan`,
        duration_days: parsedContent.duration_days || 7,
        days: parsedContent.days
          ? parsedContent.days.map((d: Day) => ({ ...d, completed: false }))
          : Array.from(
              { length: parsedContent.duration_days || 7 },
              (_, i) => ({
                day: i + 1,
                title: `Day ${i + 1}`,
                exercises: [],
                completed: false,
              })
            ),
        meals: parsedContent.meals
          ? parsedContent.meals.map((m: MealDay) => ({
              ...m,
              breakfast_completed: false,
              lunch_completed: false,
              dinner_completed: false,
            }))
          : Array.from(
              { length: parsedContent.duration_days || 7 },
              (_, i) => ({
                day: i + 1,
                breakfast: "",
                lunch: "",
                dinner: "",
                snack: "",
                breakfast_completed: false,
                lunch_completed: false,
                dinner_completed: false,
              })
            ),
        progress: 0,
      };

      setPlans((prevPlans) => ({ ...prevPlans, [activeType]: fullPlan }));
      onPlanUpdate?.(fullPlan, activeType);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : String(err));
    } finally {
      setLoading(false);
    }
  };

  const plan = plans[activeType];
  const currentProgress = plan.progress ?? 0;

  return (
    <div className="space-y-6">
      {error && (
        <div className="p-3 rounded-lg bg-red-500/20 text-red-300 border border-red-500/40">
          {error}
        </div>
      )}
      <div className="flex gap-3">
        <button
          onClick={() => setActiveType("workout")}
          className={`btn flex-1 ${
            activeType === "workout" ? "btn-primary" : "btn-outline"
          }`}
        >
          🏋️ Workout
        </button>
        <button
          onClick={() => setActiveType("diet")}
          className={`btn flex-1 ${
            activeType === "diet" ? "btn-primary" : "btn-outline"
          }`}
        >
          🥗 Diet
        </button>
      </div>
      <div className="bg-base-200/70 p-4 rounded-xl border border-base-300 shadow-md text-base-content space-y-4">
        <h3 className="text-xl font-bold">{plan.plan_name}</h3>
        <p className="text-sm opacity-80">
          Duration: {plan.duration_days} days
        </p>
        <div className="h-2 w-full bg-base-300 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-pink-500 to-purple-500"
            style={{ width: `${currentProgress}%` }}
          ></div>
        </div>

        {activeType === "workout" &&
          plan.days?.map((d: Day) => (
            <div
              key={d.day}
              className="p-3 rounded-lg bg-base-300/60 border border-base-300"
            >
              <div className="flex items-center justify-between">
                <h4 className="font-semibold">
                  Day {d.day}: {d.title}
                </h4>
                <label className="flex items-center gap-2">
                  <input type="checkbox" checked={d.completed} readOnly /> Done
                </label>
              </div>
              <ul className="mt-2 space-y-1 text-sm">
                {d.exercises?.map((ex, i) => (
                  <li key={i}>
                    {ex.name} — {ex.sets || ""}x{ex.reps || ""}{" "}
                    {ex.duration_min && `(${ex.duration_min} min)`}
                  </li>
                ))}
              </ul>
            </div>
          ))}

        {activeType === "diet" &&
          plan.meals?.map((m: MealDay) => (
            <div
              key={m.day}
              className="p-3 rounded-lg bg-base-300/60 border border-base-300"
            >
              <h4 className="font-semibold">Day {m.day}</h4>
              <div className="mt-1 text-sm space-y-1">
                {(["breakfast", "lunch", "dinner"] as const).map((meal) => (
                  <label
                    key={meal}
                    className="flex items-center justify-between"
                  >
                    <span>
                      🍽️{" "}
                      <span className="font-medium">
                        {meal.charAt(0).toUpperCase() + meal.slice(1)}:
                      </span>{" "}
                      {m[meal]}
                    </span>
                    <input
                      type="checkbox"
                      checked={Boolean(m[`${meal}_completed`])}
                      readOnly
                    />
                  </label>
                ))}
              </div>
            </div>
          ))}
      </div>

      <button
        onClick={handleGenerateNewPlan}
        disabled={loading}
        className="btn btn-primary w-full max-w-sm text-lg"
      >
        {loading ? "Generating..." : "Request new AI plan!"}
      </button>
    </div>
  );
};

export default AiPlanCard;
