import React, { useState, useEffect } from "react";
import AuthForm from "../components/AuthForm";
import { Link, useNavigate } from "react-router-dom";
import ThemeSwitcher from "../components/ThemeSwitcher";

const RegisterPage: React.FC = () => {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const [confirmError, setConfirmError] = useState("");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!formData.confirmPassword) {
      setConfirmError("");
    } else if (formData.password !== formData.confirmPassword) {
      setConfirmError("Passwords do not match!");
    } else {
      setConfirmError("");
    }
  }, [formData.password, formData.confirmPassword]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleRegister = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (confirmError) return;
    setError(null);

    try {
      const response = await fetch("http://localhost:5000/api/auth/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: formData.username,
          email: formData.email,
          password: formData.password,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        console.log("Register response:", data);

        localStorage.setItem("authToken", data.token);

        navigate("/dashboard");
      } else {
        setError(data.message || "Registration failed");
      }
    } catch (err) {
      setError("Network error. Please try again.");
      console.error(err);
    }
  };

  const fields = [
    { label: "Username", type: "text", name: "username", value: formData.username, onChange: handleChange },
    { label: "Email", type: "email", name: "email", value: formData.email, onChange: handleChange },
    { label: "Password", type: "password", name: "password", value: formData.password, onChange: handleChange },
    {
      label: "Confirm Password",
      type: "password",
      name: "confirmPassword",
      value: formData.confirmPassword,
      onChange: handleChange,
      error: confirmError,
    },
  ];

  return (
    <>
      <ThemeSwitcher />
      <AuthForm
        title="Create Your Account"
        buttonText="Register"
        onSubmit={handleRegister}
        fields={fields}
        footer={
          <p className="text-white text-center mt-2">
            Already have an account?{" "}
            <Link to="/login" className="link link-info">
              Login
            </Link>
          </p>
        }
      />
    </>
  );
};

export default RegisterPage;
