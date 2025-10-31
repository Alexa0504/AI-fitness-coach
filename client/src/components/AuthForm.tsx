import React from "react";

interface AuthFormProps {
  title: string;
  buttonText: string;
  onSubmit: (e: React.FormEvent<HTMLFormElement>) => void;
  fields: { label: string; type: string; name: string }[];
  footer?: React.ReactNode;
}

const AuthForm: React.FC<AuthFormProps> = ({ title, buttonText, onSubmit, fields, footer }) => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 p-4">
      <div
        className="card w-full max-w-md bg-base-100/60 backdrop-blur-xl shadow-2xl border border-white/20 p-10"
        style={{ borderRadius: "1.5rem" }}
      >
        <div className="card-body animate-fade-in">
          <h2 className="text-center text-3xl font-extrabold mb-6 text-white drop-shadow-md">
            {title}
          </h2>
          <form onSubmit={onSubmit}>
            {fields.map((field) => (
              <div className="form-control mb-4" key={field.name}>
                <label className="label">
                  <span className="label-text text-white/90">{field.label}</span>
                </label>
                <input
                  type={field.type}
                  name={field.name}
                  placeholder={field.label}
                  className="input input-bordered w-full bg-white/80 focus:bg-white text-black"
                  required
                />
              </div>
            ))}
            <div className="form-control mt-6">
              <button className="btn btn-primary w-full text-lg">{buttonText}</button>
            </div>
          </form>
          {footer && <div className="mt-6 text-center">{footer}</div>}
        </div>
      </div>
    </div>
  );
};

export default AuthForm;
