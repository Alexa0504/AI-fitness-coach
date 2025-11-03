import React from 'react';

const AiPlanCard: React.FC = () => {
    const handleGenerateNewPlan = () => {
        alert("Új terv generálása...");
    };

    return (
        <div className="space-y-6">
            {/* Változtatás: text-base-content/80 a text-gray-700 dark:text-gray-300 helyett */}
            <div className="text-base-content/80 transition-colors duration-300">
                <p className="mb-4 border-gray-200 dark:border-gray-700 pb-2 transition-colors duration-300">
                    Jelenleg nem elérhető edzés- vagy étrendterv. Kérlek, generálj egy újat a gomb segítségével.
                </p>
                <p className="text-sm italic border-gray-200 dark:border-gray-700 pb-2 transition-colors duration-300">
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