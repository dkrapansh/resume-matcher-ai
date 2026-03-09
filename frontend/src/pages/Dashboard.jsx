import Shell from "../components/Shell";

export default function Dashboard() {
    return (
        <Shell>
            <div className="text-3xl font-semibold">Dashboard</div>
            <p className="mt-2 text-neutral-600">
                Login successful. Next we’ll add resume upload and job description input.
            </p>
        </Shell>
    );
}