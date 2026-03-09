import { Link, NavLink } from "react-router-dom";

const navItem = ({ isActive }) =>
    `px-3 py-2 rounded-xl text-sm font-medium transition ${isActive
        ? "bg-black text-white"
        : "text-neutral-700 hover:bg-neutral-100"
    }`;

export default function Shell({ children }) {
    return (
        <div className="min-h-screen bg-neutral-50 text-neutral-900">
            <header className="sticky top-0 z-10 border-b bg-white/70 backdrop-blur">
                <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
                    <Link to="/dashboard" className="font-semibold tracking-tight">
                        Resume Matcher
                    </Link>

                    <nav className="flex items-center gap-2">
                        <NavLink to="/dashboard" className={navItem}>
                            Dashboard
                        </NavLink>
                        <NavLink to="/reports" className={navItem}>
                            Reports
                        </NavLink>
                    </nav>
                </div>
            </header>

            <main className="mx-auto max-w-6xl px-4 py-10">{children}</main>
        </div>
    );
}