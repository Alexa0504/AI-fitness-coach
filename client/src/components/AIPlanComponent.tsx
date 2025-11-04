import React, {useState} from "react";

const AiPlanCard: React.FC = () => {
    const [plan, setPlan] = useState<any | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleGenerateNewPlan = async () => {
        setLoading(true);
        setError(null);

        const token = localStorage.getItem("authToken");
        if (!token) {
            setError("Kérlek, jelentkezz be új terv generálásához.");
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
                body: JSON.stringify({plan_type: "workout"}),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || "Hiba történt a terv generálása során.");
            }

            // Ha a content JSON string, akkor parsoljuk
            const parsedContent =
                typeof data.plan.content === "string"
                    ? JSON.parse(data.plan.content)
                    : data.plan.content;

            setPlan(parsedContent);
        } catch (err: any) {
            console.error(err);
            setError(err.message || "Hiba történt a szerverrel való kommunikáció során.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="space-y-6">
            {error && (
                <div className="p-3 rounded-lg bg-red-500/20 text-red-300 border border-red-500/40">
                    {error}
                </div>
            )}

            {plan ? (
                <div
                    className="bg-base-200/70 p-4 rounded-xl border border-base-300 shadow-md text-base-content space-y-4">
                    <h3 className="text-xl font-bold">{plan.plan_name}</h3>
                    <p className="text-sm opacity-80">
                        Időtartam: {plan.duration_days} nap
                    </p>

                    <ul className="space-y-2">
                        {plan.exercises?.map((ex: any, index: number) => (
                            <li
                                key={index}
                                className="p-2 rounded-lg bg-base-300/60 border border-base-300"
                            >
                                <span className="font-semibold">{ex.name}</span> – {ex.sets}x{ex.reps}
                            </li>
                        ))}
                    </ul>
                </div>
            ) : (
                <div className="text-base-content/80 transition-colors duration-300">
                    <p className="mb-4">
                        Jelenleg nem elérhető edzés- vagy étrendterv. Kérlek, generálj egy újat a gomb
                        segítségével.
                    </p>
                    <p className="text-sm italic">
                        Itt fognak megjelenni a részletes, napokra bontott adatok, miután az AI elkészítette
                        a személyre szabott terved.
                    </p>
                </div>
            )}

            <button
                onClick={handleGenerateNewPlan}
                disabled={loading}
                className="btn btn-primary w-full max-w-sm text-lg"
            >
                {loading ? "Terv generálása..." : "Kérj új AI tervet!"}
            </button>
        </div>
    );
};

export default AiPlanCard;
