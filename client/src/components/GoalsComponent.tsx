import React from "react";
import { motion } from "framer-motion";

const goals = [
  { name: "Heti edzések", current: 3, goal: 5 },
  { name: "Megivott víz (liter)", current: 8, goal: 14 },
  { name: "Kalória cél", current: 1800, goal: 2000 },
];

const GoalsComponent: React.FC = () => {
  return (
    <div className="space-y-6">
      {goals.map((g, i) => {
        const progress = Math.min((g.current / g.goal) * 100, 100);
        return (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.15 }}
            className="bg-base-200/60 dark:bg-base-300/60 rounded-xl p-4 shadow-md border border-base-300 transition-colors duration-300"
          >
            <div className="flex justify-between items-center mb-2">
              <span className="font-medium text-base-content">{g.name}</span>
              <span className="text-sm text-base-content/70">
                {g.current}/{g.goal}
              </span>
            </div>
            <div className="w-full bg-base-300 rounded-full h-3 overflow-hidden">
              <motion.div
                className="h-3 rounded-full bg-gradient-to-r from-pink-500 to-purple-500"
                style={{ width: `${progress}%` }}
                initial={{ width: 0 }}
                animate={{ width: `${progress}%` }}
                transition={{ duration: 1, ease: "easeOut" }}
              />
            </div>
          </motion.div>
        );
      })}
    </div>
  );
};

export default GoalsComponent;
