import React from "react";
import AuthForm from "../components/AuthForm";
import { Link, useNavigate } from "react-router-dom";

const LoginPage: React.FC = () => {
  const navigate = useNavigate();

  const handleLogin = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    // TODO: connect to Flask API later
    console.log("Login submitted");
  };

  return (
    <AuthForm
      title="Welcome Back 👋"
      buttonText="Login"
      onSubmit={handleLogin}
      fields={[
        { label: "Email", type: "email", name: "email" },
        { label: "Password", type: "password", name: "password" },
      ]}
      footer={
        <div className="space-y-2">
          <p className="text-white">
            Don’t have an account?{" "}
            <Link to="/register" className="link link-info">
              Register here
            </Link>
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
  );
};

export default LoginPage;
