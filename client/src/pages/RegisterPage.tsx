import React, { useState } from "react";
import AuthForm from "../components/AuthForm";
import { Link } from "react-router-dom";

const RegisterPage: React.FC = () => {
  const [error, setError] = useState("");

  const handleRegister = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const form = e.currentTarget;
    const password = (form.elements.namedItem("password") as HTMLInputElement).value;
    const confirm = (form.elements.namedItem("confirmPassword") as HTMLInputElement).value;

    if (password !== confirm) {
      setError("Passwords do not match!");
      return;
    }

    setError("");
    console.log("Register submitted");
  };

  return (
    <AuthForm
      title="Create Your Account"
      buttonText="Register"
      onSubmit={handleRegister}
      fields={[
        { label: "Username", type: "text", name: "username" },
        { label: "Email", type: "email", name: "email" },
        { label: "Password", type: "password", name: "password" },
        { label: "Confirm Password", type: "password", name: "confirmPassword" },
      ]}
      footer={
        <div>
          {error && <p className="text-error font-semibold mb-3">{error}</p>}
          <p className="text-white">
            Already have an account?{" "}
            <Link to="/login" className="link link-info">
              Login
            </Link>
          </p>
        </div>
      }
    />
  );
};

export default RegisterPage;
