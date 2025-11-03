import React from "react";

interface Field {
  label: string;
  type: string;
  name: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  error?: string;
}

interface AuthFormProps {
  title: string;
  buttonText: string;
  onSubmit: (e: React.FormEvent<HTMLFormElement>) => void;
  fields: Field[];
  footer?: React.ReactNode;
}

const AuthForm: React.FC<AuthFormProps> = ({ title, buttonText, onSubmit, fields, footer }) => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 p-4 relative">
      <div className="card w-full max-w-md bg-base-100/60 backdrop-blur-xl shadow-2xl border border-white/20 p-10" style={{ borderRadius: "1.5rem" }}>
        <div className="card-body animate-fade-in">
          <h2 className="text-center text-3xl font-extrabold mb-6 text-white drop-shadow-md">{title}</h2>

          <form onSubmit={onSubmit}>
            {fields.map((field) => (
              <div className="form-control mb-5" key={field.name}>
                <label className="label mb-2">
                  <span className="label-text text-white/90">{field.label}</span>
                </label>
                <input
                  type={field.type}
                  name={field.name}
                  placeholder={field.label}
                  className="input input-bordered w-full bg-base-200 text-base-content placeholder-base-content/50 focus:bg-base-100"
                  value={field.value}
                  onChange={field.onChange}
                  required
                />
                {field.error && <p className="text-error mt-1">{field.error}</p>}
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
