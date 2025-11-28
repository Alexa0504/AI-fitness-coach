import React, { useEffect, useState } from "react";

interface Tip {
  id: number;
  category: string;
  text: string;
}

const NextGoalsTips: React.FC = () => {
  const [tips, setTips] = useState<Tip[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTips = async () => {
      try {
        const res = await fetch("http://localhost:5000/tips/general/weekly");
        if (!res.ok) throw new Error("Failed to fetch tips.");
        const data: Tip[] = await res.json();
        setTips(data);
      } catch (err: unknown) {
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError("An unknown error occurred.");
        }
      } finally {
        setLoading(false);
      }
    };
    fetchTips();
  }, []);

  if (loading) return <p>Loading tips...</p>;
  if (error) return <p className="text-red-500">{error}</p>;

  return (
    <ul className="space-y-3">
      {tips.map((tip) => (
        <li
          key={tip.id}
          className="flex items-center p-3 bg-gray-50 dark:bg-gray-800/60 rounded-lg"
        >
          <span className="w-3 h-3 mr-3 bg-purple-500 rounded-full flex-shrink-0"></span>
          <span className="font-medium text-gray-900 dark:text-gray-100">
            {tip.text}
          </span>
        </li>
      ))}
    </ul>
  );
};

interface GamificationCardProps {
  performance: number;
  xp: number;
  level: number;
  xpToNext: number;
}

const GamificationCard: React.FC<GamificationCardProps> = ({
  performance,
  xp,
  level,
  xpToNext,
}) => {
  return (
    <div className="flex flex-col space-y-4">
      <div className="p-4 bg-yellow-100 dark:bg-yellow-900/50 border border-yellow-300 dark:border-yellow-700 rounded-xl text-center shadow-lg transition duration-300 hover:shadow-xl">
        <span className="text-5xl" role="img" aria-label="Star">
          ⭐
        </span>
        <p className="text-xl font-bold text-yellow-800 dark:text-yellow-300 mt-2">
          Performance: {performance}%
        </p>
        <p className="text-sm text-gray-600 dark:text-gray-400">
          You have achieved {performance}% of your weekly goals!
        </p>
      </div>

      <div className="p-4 bg-green-100 dark:bg-green-900/50 border border-green-300 dark:border-green-700 rounded-xl text-center shadow-lg transition duration-300 hover:shadow-xl">
        <span className="text-5xl" role="img" aria-label="Trophy">
          🏆
        </span>
        <p className="text-xl font-bold text-green-800 dark:text-green-300 mt-2">
          Total Points: {xp} XP
        </p>
        <p className="text-sm text-gray-600 dark:text-gray-400">
          {xpToNext} XP to reach next level (Level {level + 1})
        </p>
      </div>

      <div
        id="next-goals-tips"
        className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700"
      >
        <h3 className="text-2xl font-bold text-base-content mb-4 border-b border-gray-200 dark:border-gray-700 pb-2">
          Self-Care Checklist
        </h3>
        <NextGoalsTips />
      </div>
    </div>
  );
};

export default GamificationCard;
