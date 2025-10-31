import React from "react";
import AuthForm from "../components/AuthForm";
import { Link } from "react-router-dom";

const LoginPage: React.FC = () => {
  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: connect to Flask API later
    console.log("Login submitted");
  };

  return (
    <div>
      <AuthForm
        title="Welcome Back 👋"
        buttonText="Login"
        onSubmit={handleLogin}
        fields={[
          { label: "Email", type: "email", name: "email" },
          { label: "Password", type: "password", name: "password" },
        ]}
      />
      <p className="text-center mt-4">
        Don’t have an account?{" "}
        <Link to="/register" className="link link-primary">
          Register
        </Link>
      </p>
    </div>
  );
};

export default LoginPage;
