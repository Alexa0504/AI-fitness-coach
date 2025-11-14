// src/utils/calculatePlanProgress.ts
export const calculatePlanProgress = (plan: any, type: "workout" | "diet") => {
  if (!plan) return 0;

  if (type === "workout") {
    const total = plan.days?.length || 0;
    const done = plan.days?.filter((d: any) => d?.completed)?.length || 0;
    return total ? Math.round((done / total) * 100) : 0;
  }

  if (type === "diet") {
    const meals = plan.meals || [];
    const all = meals.flatMap((m: any) => [
      m?.breakfast_consumed,
      m?.lunch_consumed,
      m?.dinner_consumed,
    ]);
    const done = all.filter(Boolean).length;
    return all.length ? Math.round((done / all.length) * 100) : 0;
  }

  return 0;
};
