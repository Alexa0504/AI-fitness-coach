import React from "react";
import { motion } from "framer-motion";

interface TaskbarProps {
  progress: number;
}

const Taskbar: React.FC<TaskbarProps> = ({ progress }) => {
  return (
    <div className="w-full bg-base-300 rounded-full h-4 overflow-hidden mt-2">
      <motion.div
        className="h-4 rounded-full bg-gradient-to-r from-pink-500 to-purple-500"
        style={{ width: `${progress}%` }}
        animate={{ width: `${progress}%` }}
        transition={{ duration: 0.6, ease: "easeOut" }}
      />
    </div>
  );
};

export default Taskbar;
