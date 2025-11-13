import React, { useEffect }  from "react";
import {useNavigate} from "react-router-dom";
import ThemeSwitcher from "../components/ThemeSwitcher";
import {useTheme} from "../components/ThemeContext";
import AiPlanCard from "../components/AIPlanComponent";
import GamificationCard from "../components/StatComponent";
import GoalsCard from "../components/GoalsComponent";
import {motion} from "framer-motion";

const HeaderBar: React.FC = () => {
    const navigate = useNavigate();

    const handleLogout = async () => {
        const token = localStorage.getItem("authToken");
        if (!token) {
            navigate("/login");
            return;
        }

        try {
            const res = await fetch("http://localhost:5000/api/auth/logout", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            });

            if (res.ok) {
                localStorage.removeItem("authToken");
                localStorage.removeItem("user");
                navigate("/login");
            } else {
                console.error("Logout failed:", await res.text());
            }
        } catch (err) {
            console.error("Error logging out:", err);
        }
    };

    return (
        <header
            className="sticky top-0 z-20 w-full bg-base-100/70 dark:bg-base-300/50 backdrop-blur-lg shadow-md border-b border-base-300 transition-colors duration-300">
            <div className="max-w-7xl mx-auto flex flex-wrap justify-between items-center px-4 sm:px-6 py-3 gap-3">
                <h1 className="text-xl sm:text-2xl font-extrabold bg-gradient-to-r from-purple-500 to-pink-400 bg-clip-text text-transparent drop-shadow-md dark:from-purple-300 dark:to-pink-200 transition-colors duration-300">
                    AI Fitness Coach
                </h1>

                 <div className="flex items-center gap-2 sm:gap-4">
          {/*  Profile button added */}
          <button
            onClick={() => navigate("/profile")}
            className="px-3 sm:px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg font-semibold shadow-md hover:shadow-indigo-400/30 transition-all duration-200 text-sm sm:text-base"
          >
            Profile
          </button>

          <div className="flex items-center justify-center">
            <ThemeSwitcher />
          </div>

          <button
            onClick={handleLogout}
            className="px-3 sm:px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg font-semibold shadow-md hover:shadow-indigo-400/30 transition-all duration-200 text-sm sm:text-base"
          >
            Logout
          </button>
        </div>
            </div>
        </header>
    );
};

const DashboardSection: React.FC<{ title: string; children: React.ReactNode }> = ({
                                                                                      title,
                                                                                      children,
                                                                                  }) => (
    <motion.section
        initial={{opacity: 0, y: 25}}
        animate={{opacity: 1, y: 0}}
        transition={{duration: 0.6, ease: "easeOut"}}
        className="p-6 rounded-2xl shadow-2xl border border-base-300
               bg-base-100/90 dark:bg-base-200/80
               backdrop-blur-md hover:shadow-[0_0_25px_rgba(255,255,255,0.15)]
               transition-all duration-300"
    >
        <h2 className="text-2xl font-bold text-base-content mb-4 border-b border-base-300 pb-2 transition-colors duration-300">
            {title}
        </h2>
        <div className="text-base-content transition-colors duration-300">
            {children}
        </div>
    </motion.section>
);

const Footer: React.FC = () => (
    <footer className="py-6 text-center text-sm text-white/80 dark:text-gray-400 mt-10 transition-colors duration-300">
        © {new Date().getFullYear()} AI Planner. All rights reserved.
    </footer>
);

const HomePage: React.FC = () => {
    const {theme} = useTheme();
    const navigate = useNavigate();

    
    useEffect(() => {
    const checkProfileCompletion = async () => {
      const token = localStorage.getItem("authToken");

      
      if (!token) {
        navigate("/login");
        return;
      }

      try {
        
        const res = await fetch("http://localhost:5000/api/users/profile", {
          headers: { Authorization: `Bearer ${token}` },
        });
        const data = await res.json();

        
        if (!data.gender || !data.height_cm || !data.weight_kg) {
          navigate("/profile");
        }
      } catch (error) {
        console.error("Error checking profile:", error);
        navigate("/login"); 
      }
    };

    checkProfileCompletion();
  }, [navigate]);
    return (
        <div className={`relative min-h-screen ${theme} transition-colors duration-500`}>
            <div
                className="absolute inset-0 bg-gradient-to-br from-purple-600 via-pink-500 to-blue-500 dark:from-gray-900 dark:via-gray-800 dark:to-black transition-colors duration-500"/>
            <div
                className="absolute inset-0 bg-black/10 dark:bg-black/50 backdrop-blur-[1px] transition-colors duration-500"/>
            <div className="relative z-10">
                <HeaderBar/>

                <main className="max-w-7xl mx-auto px-6 py-10">
                    <motion.h1
                        initial={{opacity: 0, y: -20}}
                        animate={{opacity: 1, y: 0}}
                        transition={{duration: 0.7}}
                        className="text-4xl font-extrabold text-white dark:text-gray-100 mb-10 text-center sm:text-left drop-shadow-[0_3px_5px_rgba(0,0,0,0.3)] transition-colors duration-500"
                    >
                        Dashboard
                    </motion.h1>

                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                        <div className="lg:col-span-2 space-y-8">
                            <DashboardSection title="Your Goals and Progress">
                                <GoalsCard/>
                            </DashboardSection>
                            <DashboardSection title="AI Workout and Diet Plan">
                                <AiPlanCard/>
                            </DashboardSection>
                        </div>

                        <aside className="lg:col-span-1 space-y-8">
                            <DashboardSection title="Statistics and Score">
                                <GamificationCard/>
                            </DashboardSection>
                        </aside>
                    </div>
                </main>

                <Footer/>
            </div>
        </div>
    );
};

export default HomePage;
