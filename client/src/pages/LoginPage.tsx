import React, { useState } from "react";
import AuthForm from "../components/AuthForm";
import { Link, useNavigate } from "react-router-dom";
import ThemeSwitcher from "../components/ThemeSwitcher";

const LoginPage: React.FC = () => {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleLogin = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log("Login submitted", formData);
    // TODO: connect to Flask API
  };

  const fields = [
    { label: "Email", type: "email", name: "email", value: formData.email, onChange: handleChange },
    { label: "Password", type: "password", name: "password", value: formData.password, onChange: handleChange },
  ];

  return (
    <>
      <ThemeSwitcher />
      <AuthForm
        title="Welcome Back 👋"
        buttonText="Login"
        onSubmit={handleLogin}
        fields={fields}
        footer={
          <div className="space-y-2">
            <p className="text-white text-center">
              Don’t have an account?{" "}
            </p>
            <button
              onClick={() => navigate("/register")}
              className="btn btn-outline btn-accent w-full mt-2"
            >
              Register
            </button>
          </div>
        }
      />
    </>
  );
};

export default LoginPage;
