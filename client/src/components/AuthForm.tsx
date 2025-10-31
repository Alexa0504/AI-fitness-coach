import React from "react";

interface AuthFormProps {
  title: string;
  buttonText: string;
  onSubmit: (e: React.FormEvent) => void;
  fields: { label: string; type: string; name: string }[];
}

const AuthForm: React.FC<AuthFormProps> = ({ title, buttonText, onSubmit, fields }) => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-base-200">
      <div className="card w-full max-w-md shadow-2xl bg-base-100">
        <div className="card-body">
          <h2 className="text-center text-2xl font-bold mb-4">{title}</h2>
          <form onSubmit={onSubmit}>
            {fields.map((field) => (
              <div className="form-control mb-3" key={field.name}>
                <label className="label">
                  <span className="label-text">{field.label}</span>
                </label>
                <input
                  type={field.type}
                  name={field.name}
                  placeholder={field.label}
                  className="input input-bordered w-full"
                  required
                />
              </div>
            ))}
            <div className="form-control mt-6">
              <button className="btn btn-primary w-full" type="submit">
                {buttonText}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default AuthForm;
