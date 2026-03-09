import { useState } from "react";
import { useNavigate } from "react-router-dom";
import client from "../api/client";

export default function Login() {
    const navigate = useNavigate();

    const [form, setForm] = useState({
        email: "",
        password: "",
    });

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    function handleChange(e) {
        setForm((prev) => ({
            ...prev,
            [e.target.name]: e.target.value,
        }));
    }

    async function handleSubmit(e) {
        e.preventDefault();
        setError("");
        setLoading(true);

        try {
            const response = await client.post("/auth/login", form);

            const token = response.data.access_token;
            localStorage.setItem("token", token);

            navigate("/dashboard");
        } catch (err) {
            setError(
                err?.response?.data?.detail || "Login failed. Please try again."
            );
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="min-h-screen bg-neutral-50 text-neutral-900">
            <div className="mx-auto flex min-h-screen max-w-6xl items-center justify-center px-4">
                <div className="w-full max-w-md rounded-3xl border border-neutral-200 bg-white p-8 shadow-sm">
                    <div className="mb-8">
                        <h1 className="text-3xl font-semibold tracking-tight">
                            Resume Matcher
                        </h1>
                        <p className="mt-2 text-sm text-neutral-500">
                            Sign in to continue to your dashboard.
                        </p>
                    </div>

                    <form onSubmit={handleSubmit} className="space-y-5">
                        <div>
                            <label className="mb-2 block text-sm font-medium text-neutral-700">
                                Email
                            </label>
                            <input
                                type="email"
                                name="email"
                                value={form.email}
                                onChange={handleChange}
                                placeholder="you@example.com"
                                className="w-full rounded-2xl border border-neutral-300 px-4 py-3 outline-none transition focus:border-neutral-500"
                                required
                            />
                        </div>

                        <div>
                            <label className="mb-2 block text-sm font-medium text-neutral-700">
                                Password
                            </label>
                            <input
                                type="password"
                                name="password"
                                value={form.password}
                                onChange={handleChange}
                                placeholder="Enter your password"
                                className="w-full rounded-2xl border border-neutral-300 px-4 py-3 outline-none transition focus:border-neutral-500"
                                required
                            />
                        </div>

                        {error ? (
                            <div className="rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-600">
                                {error}
                            </div>
                        ) : null}

                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full rounded-2xl bg-black px-4 py-3 text-sm font-medium text-white transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-60"
                        >
                            {loading ? "Signing in..." : "Sign In"}
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
}