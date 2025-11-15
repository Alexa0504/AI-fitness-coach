import React, { useState, useEffect } from "react";

const API_URL = "http://localhost:5000/api/plans/";
const API_LATEST_URL = "http://localhost:5000/api/plans/latest";

interface Plan {
  id?: number;
  plan_name: string;
  plan_type: "workout" | "diet";
  duration_days: number;
  days?: any[];
  meals?: any[];
  note?: string;
}

interface AiPlanCardProps {
  onPlanUpdate?: (plan: any, type: "workout" | "diet") => void;
}

const AiPlanCard: React.FC<AiPlanCardProps> = ({ onPlanUpdate }) => {
  const [plans, setPlans] = useState<{ workout?: Plan; diet?: Plan }>({});
  const [activeType, setActiveType] = useState<"workout" | "diet">("workout");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const token = localStorage.getItem("authToken");

  useEffect(() => {
    const fetchLatestPlans = async () => {
      if (!token) return;
      try {
        const res = await fetch(API_LATEST_URL, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!res.ok) throw new Error("Failed to load latest plans.");
        const data = await res.json();
        const loadedPlans: { workout?: Plan; diet?: Plan } = {};
        data.plans?.forEach((p: any) => {
          const parsed =
            typeof p.content === "string" ? JSON.parse(p.content) : p.content;
          if (p.plan_type === "workout")
            loadedPlans.workout = { ...parsed, ...p };
          else if (p.plan_type === "diet")
            loadedPlans.diet = { ...parsed, ...p };
        });
        setPlans(loadedPlans);
      } catch (e: any) {
        setError(e.message);
      }
    };
    fetchLatestPlans();
  }, [token]);

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
        body: JSON.stringify({ plan_type: activeType }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.message || "Error generating plan.");
      const content =
        typeof data.plan.content === "string"
          ? JSON.parse(data.plan.content)
          : data.plan.content;
      const fullPlan = { ...data.plan, ...content };
      setPlans((prev) => ({ ...prev, [activeType]: fullPlan }));
      onPlanUpdate?.(fullPlan, activeType);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleToggle = async (day: number, type: string, meal?: string) => {
    const plan = plans[activeType];
    if (!plan || !token) return;
    const planId = plan.id;
    if (!planId) {
      setError("Plan ID missing. Cannot toggle completion status.");
      return;
    }
    const body =
      activeType === "workout"
        ? { type: "workout_day", day, field: "completed", value: true }
        : { type: "diet_meal", day, meal, value: true };
    const res = await fetch(`${API_URL}${planId}/toggle`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(body),
    });
    const data = await res.json();
    if (!res.ok) {
      setError(data.message || "Error toggling completion.");
      return;
    }
    if (data?.plan) {
      const newContent =
        typeof data.plan.content === "string"
          ? JSON.parse(data.plan.content)
          : data.plan.content;
      const merged = { ...plans[activeType], ...data.plan, ...newContent };
      setPlans((prev) => ({ ...prev, [activeType]: merged }));
      onPlanUpdate?.(merged, activeType);
    }
  };

  const defaultPlan =
    activeType === "workout"
      ? {
          plan_name: "7-Day Beginner Workout Plan",
          plan_type: "workout" as const,
          duration_days: 7,
          days: Array.from({ length: 7 }, (_, i) => ({
            day: i + 1,
            title: `Workout Day ${i + 1}`,
            exercises: [],
            completed: false,
          })),
        }
      : {
          plan_name: "7-Day Sample Diet Plan",
          plan_type: "diet" as const,
          duration_days: 7,
          meals: Array.from({ length: 7 }, (_, i) => ({
            day: i + 1,
            breakfast: "",
            lunch: "",
            dinner: "",
            snack: "",
          })),
        };

  const plan = plans[activeType] || defaultPlan;

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
        {activeType === "workout" && plan.days && (
          <div className="space-y-3">
            {plan.days.map((day: any, idx: number) => (
              <div
                key={idx}
                className="p-3 rounded-lg bg-base-300/60 border border-base-300"
              >
                <div className="flex items-center justify-between">
                  <h4 className="font-semibold">
                    Day {day.day}: {day.title || "Workout"}
                  </h4>
                  <label className="flex items-center gap-2">
                    <input
                      type="checkbox"
                      checked={!!day.completed}
                      onChange={() => handleToggle(day.day, "workout_day")}
                    />
                    Done
                  </label>
                </div>
                <ul className="mt-2 space-y-1 text-sm">
                  {day.exercises?.map((ex: any, i: number) => (
                    <li key={i}>
                      {ex.name} — {ex.sets || ""}x{ex.reps || ""}{" "}
                      {ex.duration_min && `(${ex.duration_min} min)`}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        )}
        {activeType === "diet" && plan.meals && (
          <div className="space-y-3">
            {plan.meals.map((day: any, idx: number) => (
              <div
                key={idx}
                className="p-3 rounded-lg bg-base-300/60 border border-base-300"
              >
                <h4 className="font-semibold">Day {day.day}</h4>
                <div className="mt-1 text-sm space-y-1">
                  {["breakfast", "lunch", "dinner"].map((meal) => (
                    <label
                      key={meal}
                      className="flex items-center justify-between"
                    >
                      <span>
                        🍽️{" "}
                        <span className="font-medium">
                          {meal.charAt(0).toUpperCase() + meal.slice(1)}:
                        </span>{" "}
                        {day[meal]}
                      </span>
                      <input
                        type="checkbox"
                        checked={!!day[`${meal}_completed`]}
                        onChange={() =>
                          handleToggle(day.day, "diet_meal", meal)
                        }
                      />
                    </label>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
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
