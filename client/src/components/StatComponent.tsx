import React from 'react';

const GamificationCard: React.FC = () => {
    return (
        <div className="flex flex-col space-y-4">
            <div className="p-4 bg-yellow-100 dark:bg-yellow-900/50 border border-yellow-300 dark:border-yellow-700 rounded-xl text-center shadow-lg transition duration-300 hover:shadow-xl">
                <span className="text-5xl" role="img" aria-label="Star">⭐</span>
                <p className="text-xl font-bold text-yellow-800 dark:text-yellow-300 mt-2">
                    Teljesítmény: 85%
                </p>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                    A heti céljaid 85%-át teljesítetted!
                </p>
            </div>
            <div className="p-4 bg-green-100 dark:bg-green-900/50 border border-green-300 dark:border-green-700 rounded-xl text-center shadow-lg transition duration-300 hover:shadow-xl">
                <span className="text-5xl" role="img" aria-label="Trophy">🏆</span>
                <p className="text-xl font-bold text-green-800 dark:text-green-300 mt-2">
                    Összesített pontszám: 1250 XP
                </p>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                    Még 750 XP a "Haladó Szint" eléréséig!
                </p>
            </div>

            <div className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                    Következő Célok
                </h3>
                <ul className="space-y-3 text-gray-700 dark:text-gray-300">
                    <li className="flex items-center p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                        <span className="w-3 h-3 mr-3 bg-purple-500 rounded-full flex-shrink-0"></span>
                        <span className="font-medium">Futás:</span> Teljesíts 10 km-t (0/1)
                    </li>
                    <li className="flex items-center p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                        <span className="w-3 h-3 mr-3 bg-purple-500 rounded-full flex-shrink-0"></span>
                        <span className="font-medium">Vízfogyasztás:</span> Igyál 2L vizet (3/7 nap)
                    </li>
                    <li className="flex items-center p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
                        <span className="w-3 h-3 mr-3 bg-purple-500 rounded-full flex-shrink-0"></span>
                        <span className="font-medium">Pihenés:</span> Aludj 8 órát (6/7 nap)
                    </li>
                </ul>
            </div>
        </div>
    );
};

export default GamificationCard;
