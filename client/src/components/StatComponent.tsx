import React from "react";

const GamificationCard: React.FC = () => {
  return (
    <div className="flex flex-col space-y-4">
      <div
        className="p-4 bg-yellow-100 dark:bg-yellow-900/50 border border-yellow-300
                 dark:border-yellow-700 rounded-xl text-center shadow-lg transition duration-300 hover:shadow-xl"
      >
        <span className="text-5xl" role="img" aria-label="Star">
          ⭐
        </span>
        <p className="text-xl font-bold text-yellow-800 dark:text-yellow-300 mt-2">
          Performance: 85%
        </p>
        <p className="text-sm text-gray-600 dark:text-gray-400">
          You have achieved 85% of your weekly goals!
        </p>
      </div>

      <div className="p-4 bg-green-100 dark:bg-green-900/50 border border-green-300 dark:border-green-700 rounded-xl text-center shadow-lg transition duration-300 hover:shadow-xl">
        <span className="text-5xl" role="img" aria-label="Trophy">
          🏆
        </span>
        <p className="text-xl font-bold text-green-800 dark:text-green-300 mt-2">
          Total Points: 1250 XP
        </p>
        <p className="text-sm text-gray-600 dark:text-gray-400">
          750 XP to reach "Advanced Level"!
        </p>
      </div>

      <div className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
        <h3
          className="text-2xl font-bold text-base-content mb-4 border-b border-gray-200
                 dark:border-gray-700 pb-2 transition-colors duration-300"
        >
          Next Goals
        </h3>
        <ul className="space-y-3">
          <li
            className="flex items-center p-3 bg-gray-50 dark:bg-gray-800/60 rounded-lg 
                    transition-colors duration-300"
          >
            <span className="w-3 h-3 mr-3 bg-purple-500 rounded-full flex-shrink-0"></span>
            <span className="font-medium text-gray-900 dark:text-gray-100">
              Running:
            </span>
            <span className="ml-1 text-gray-800 dark:text-gray-200">
              Complete 10 km (0/1)
            </span>
          </li>

          <li className="flex items-center p-3 bg-gray-50 dark:bg-gray-800/60 rounded-lg transition-colors duration-300">
            <span className="w-3 h-3 mr-3 bg-purple-500 rounded-full flex-shrink-0"></span>
            <span className="font-medium text-gray-900 dark:text-gray-100">
              Water Intake:
            </span>
            <span className="ml-1 text-gray-800 dark:text-gray-200">
              Drink 2L water (3/7 days)
            </span>
          </li>

          <li className="flex items-center p-3 bg-gray-50 dark:bg-gray-800/60 rounded-lg transition-colors duration-300">
            <span className="w-3 h-3 mr-3 bg-purple-500 rounded-full flex-shrink-0"></span>
            <span className="font-medium text-gray-900 dark:text-gray-100">
              Rest:
            </span>
            <span className="ml-1 text-gray-800 dark:text-gray-200">
              Sleep 8 hours (6/7 days)
            </span>
          </li>
        </ul>
      </div>
    </div>
  );
};

export default GamificationCard;
