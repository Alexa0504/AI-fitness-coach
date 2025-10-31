import React from "react";
import AuthForm from "../components/AuthForm";
import { Link } from "react-router-dom";

const RegisterPage: React.FC = () => {
  const handleRegister = (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: connect to Flask API later
    console.log("Register submitted");
  };

  return (
    <div>
      <AuthForm
        title="Create Your Account ✨"
        buttonText="Register"
        onSubmit={handleRegister}
        fields={[
          { label: "Username", type: "text", name: "username" },
          { label: "Email", type: "email", name: "email" },
          { label: "Password", type: "password", name: "password" },
          { label: "Confirm Password", type: "password", name: "confirmPassword" },
        ]}
      />
      <p className="text-center mt-4">
        Already have an account?{" "}
        <Link to="/login" className="link link-primary">
          Login
        </Link>
      </p>
    </div>
  );
};

export default RegisterPage;
