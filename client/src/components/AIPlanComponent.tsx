import React, { useState } from "react";

const API_URL = "http://localhost:5000/api/plans/";

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

      // store in correct slot (workout or diet)
      setPlans((prev) => ({ ...prev, [activeType]: content }));
      onPlanUpdate?.(content, activeType);
    } catch (err: any) {
      console.error(err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleToggle = async (day: number, type: string, meal?: string) => {
    const plan = plans[activeType];
    if (!plan || !token) return;

    let value = true;

    if (activeType === "workout") {
      // Narrow type: ensure days exists
      if (!plan.days) return;
      const targetDay = plan.days.find((d: any) => d.day === day);
      if (!targetDay) return;
      value = !targetDay.completed; // toggle current value
    } else if (activeType === "diet") {
      if (!plan.meals || !meal) return;
      const targetDay = plan.meals.find((d: any) => d.day === day);
      if (!targetDay) return;
      const key = `${meal}_consumed`;
      value = !targetDay[key]; // toggle current value
    }

    const body =
      activeType === "workout"
        ? { type: "workout_day", day, field: "completed", value }
        : { type: "diet_meal", day, meal, value };

    try {
      const res = await fetch(`${API_URL}${plan.id || 1}/toggle`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(body),
      });

      const data = await res.json();

      if (data?.plan?.content) {
        const updated =
          typeof data.plan.content === "string"
            ? JSON.parse(data.plan.content)
            : data.plan.content;

        setPlans((prev) => ({ ...prev, [activeType]: updated }));
        onPlanUpdate?.(updated, activeType);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const plan = plans[activeType];

  return (
    <div className="space-y-6">
      {/* Error message */}
      {error && (
        <div className="p-3 rounded-lg bg-red-500/20 text-red-300 border border-red-500/40">
          {error}
        </div>
      )}

      {/* Plan type selector */}
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

      {/* Plan display */}
      {plan ? (
        <div className="bg-base-200/70 p-4 rounded-xl border border-base-300 shadow-md text-base-content space-y-4">
          <h3 className="text-xl font-bold">{plan.plan_name}</h3>
          <p className="text-sm opacity-80">
            Duration: {plan.duration_days} days
          </p>

          {/* Workout plan display */}
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

          {/* Diet plan display */}
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
                          checked={!!day[`${meal}_consumed`]}
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
      ) : (
        <div className="text-base-content/80">
          <p className="mb-4">
            No {activeType} plan yet. Click below to generate one.
          </p>
        </div>
      )}

      {/* Generate button */}
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
