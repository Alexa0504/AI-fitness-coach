import React, {useState, useEffect} from "react";
import AuthForm from "../components/AuthForm";
import {useNavigate, useLocation} from "react-router-dom";
import ThemeSwitcher from "../components/ThemeSwitcher";

const LoginPage: React.FC = () => {
    const navigate = useNavigate();
    const location = useLocation();

    const [formData, setFormData] = useState({
        email: "",
        password: "",
    });

    const [error, setError] = useState<string | null>(null);
    const [success, setSuccess] = useState<string | null>(null);

    useEffect(() => {
        if (location.state && (location.state as any).registered) {
            setSuccess("Registration successful! You can now log in.");
        }
    }, [location.state]);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const {name, value} = e.target;
        setFormData((prev) => ({...prev, [name]: value}));
    };

    const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setError(null);
        setSuccess(null);

        try {
            const response = await fetch("http://localhost:5000/api/auth/login", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(formData),
            });

            const data = await response.json();

            if (response.ok) {
                localStorage.setItem("authToken", data.token);
                navigate("/dashboard");
            } else {
                setError(data.message || "User not found or credentials do not match");
            }
        } catch (err) {
            setError("Network error. Please try again.");
            console.error(err);
        }
    };

    const fields = [
        {label: "Email", type: "email", name: "email", value: formData.email, onChange: handleChange},
        {label: "Password", type: "password", name: "password", value: formData.password, onChange: handleChange},
    ];

    return (
        <>
            <ThemeSwitcher/>
            <AuthForm
                title="Welcome Back 👋"
                buttonText="Login"
                onSubmit={handleLogin}
                fields={fields}
                footer={
                    <div className="space-y-2">
                        {success && (
                            <div className="alert alert-success shadow-lg">
                                <div>
                                    <span className="text-white">{success}</span>
                                </div>
                            </div>
                        )}

                        {error && (
                            <div className="alert alert-error shadow-lg">
                                <div>
                                    <span>{error}</span>
                                </div>
                            </div>
                        )}

                        <p className="text-white text-center mt-2">
                            Don’t have an account?{" "}
                            <button
                                onClick={() => navigate("/register")}
                                className="btn btn-outline btn-accent w-full mt-2"
                            >
                                Register
                            </button>
                        </p>
                    </div>
                }
            />
        </>
    );
};

export default LoginPage;
