import React, { useContext } from "react";
import { ThemeContext } from "./ThemeContext";

const ThemeSwitcher: React.FC = () => {
  const { toggleTheme } = useContext(ThemeContext);

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
