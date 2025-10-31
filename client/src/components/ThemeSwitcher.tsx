import React, { useEffect, useState } from "react";

const themes = ["light", "dark"] as const;

const ThemeSwitcher: React.FC = () => {
  const [themeIndex, setThemeIndex] = useState(0);

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", themes[themeIndex]);
  }, [themeIndex]);

  const toggleTheme = () => {
    setThemeIndex((prev) => (prev + 1) % themes.length);
  };

  return (
    <button
      onClick={toggleTheme}
      className="btn btn-sm btn-outline btn-accent absolute top-4 right-4 z-50"
    >
      Theme
    </button>
  );
};

export default ThemeSwitcher;
