import React, {useState} from "react";

const AiPlanCard: React.FC = () => {
    const [plan, setPlan] = useState<any | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [planType, setPlanType] = useState<"workout" | "diet">("workout");

    const handleGenerateNewPlan = async () => {
        setLoading(true);
        setError(null);

        const token = localStorage.getItem("authToken");
        if (!token) {
            setError("Please log in to generate a new plan.");
            setLoading(false);
            return;
        }

        try {
            const response = await fetch("http://localhost:5000/api/plans/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({plan_type: planType}),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || "Error generating plan.");
            }

            const parsedContent =
                typeof data.plan.content === "string"
                    ? JSON.parse(data.plan.content)
                    : data.plan.content;

            setPlan(parsedContent);
        } catch (err: any) {
            console.error(err);
            setError(err.message || "Error communicating with the server.");
        } finally {
            setLoading(false);
        }
    };

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
                    onClick={() => setPlanType("workout")}
                    className={`btn flex-1 ${planType === "workout" ? "btn-primary" : "btn-outline"}`}
                >
                    🏋️ Workout Plan
                </button>
                <button
                    onClick={() => setPlanType("diet")}
                    className={`btn flex-1 ${planType === "diet" ? "btn-primary" : "btn-outline"}`}
                >
                    🥗 Diet Plan
                </button>
            </div>

            {/* Plan display */}
            {plan ? (
                <div
                    className="bg-base-200/70 p-4 rounded-xl border border-base-300 shadow-md text-base-content space-y-4">
                    <h3 className="text-xl font-bold">{plan.plan_name}</h3>
                    <p className="text-sm opacity-80">Duration: {plan.duration_days} days</p>

                    {/* Workout Plan */}
                    {planType === "workout" && plan.exercises && (
                        <div className="space-y-3">
                            {plan.exercises.map((ex: any, index: number) => (
                                <div
                                    key={index}
                                    className="p-3 rounded-lg bg-base-300/60 border border-base-300 shadow-sm"
                                >
                                    <p className="font-semibold">{ex.activity}</p>
                                    <p className="text-sm opacity-80">
                                        {ex.sets && ex.reps && (
                                            <>
                                                {ex.sets} sets × {ex.reps} reps
                                            </>
                                        )}
                                        {ex.duration_min && `${ex.duration_min} minutes`}
                                        {ex.duration_sec && `${ex.duration_sec} seconds`}
                                        {ex.activity.toLowerCase() === "rest" && "Rest Day"}
                                    </p>
                                    <p className="text-xs opacity-70 mt-1">📅 Day {ex.day}</p>
                                </div>
                            ))}
                        </div>
                    )}

                    {/* Diet Plan */}
                    {planType === "diet" && plan.meals && (
                        <div className="space-y-3">
                            {plan.meals.map((meal: any, index: number) => (
                                <div
                                    key={index}
                                    className="p-3 rounded-lg bg-base-300/60 border border-base-300 shadow-sm"
                                >
                                    <p className="font-semibold">📅 Day {meal.day || index + 1}</p>
                                    <div className="mt-1 text-sm space-y-1">
                                        <p>🍳 <span className="font-medium">Breakfast:</span> {meal.breakfast}</p>
                                        <p>🥗 <span className="font-medium">Lunch:</span> {meal.lunch}</p>
                                        <p>🍲 <span className="font-medium">Dinner:</span> {meal.dinner}</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            ) : (
                <div className="text-base-content/80">
                    <p className="mb-4">No plan available yet. Generate a new one below.</p>
                    <p className="text-sm italic">
                        Choose a plan type and click “Request new AI plan” to generate a personalized one.
                    </p>
                </div>
            )}

            {/* Generate button */}
            <button
                onClick={handleGenerateNewPlan}
                disabled={loading}
                className="btn btn-primary w-full max-w-sm text-lg"
            >
                {loading ? "Generating plan..." : "Request new AI plan!"}
            </button>
        </div>
    );
};

export default AiPlanCard;
