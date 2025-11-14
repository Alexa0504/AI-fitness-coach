import { motion } from "framer-motion";

const Taskbar = ({ progress }: { progress: number }) => {
  return (
    <div className="w-full bg-base-300 rounded-full h-4 overflow-hidden">
      <motion.div
        className="h-4 bg-gradient-to-r from-pink-500 to-purple-500 rounded-full"
        animate={{ width: `${progress}%` }}
        transition={{ duration: 0.5 }}
      />
    </div>
  );
};

export default Taskbar;
