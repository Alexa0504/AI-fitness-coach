import React, { useContext } from "react";
import { ThemeContext } from "./ThemeContext";

const ThemeSwitcher: React.FC = () => {
  const { toggleTheme } = useContext(ThemeContext);

  return (
    <button
      onClick={toggleTheme}
      className="btn btn-sm btn-outline btn-accent"
    >
      Theme
    </button>
  );
};

export default ThemeSwitcher;
