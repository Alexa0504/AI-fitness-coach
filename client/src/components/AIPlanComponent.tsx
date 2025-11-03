import React from 'react';

const AiPlanCard: React.FC = () => {
    const handleGenerateNewPlan = () => {
        alert("Új terv generálása...");
    };

    return (
        <div className="space-y-6">
            <div className="text-gray-700 dark:text-gray-300">
                <p className="mb-4">
                    Jelenleg nem elérhető edzés- vagy étrendterv. Kérlek, generálj egy újat a gomb segítségével.
                </p>
                <p className="text-sm italic">
                    Itt fognak megjelenni a részletes, napokra bontott adatok, miután az AI elkészítette a személyre szabott terved.
                </p>
            </div>

            <button
                onClick={handleGenerateNewPlan}
                className="btn btn-primary w-full max-w-sm text-lg"
            >
                Kérj új AI tervet!
            </button>
        </div>
    );
};

export default AiPlanCard;
