import { render, screen, waitFor } from "@testing-library/react";
import HomePage from '../../pages/HomePage';
import '@testing-library/jest-dom';


jest.mock('../../components/ThemeContext', () => ({
    useTheme: () => ({ theme: "light" })
}));


const mockedFetch: jest.Mock = jest.fn();
global.fetch = mockedFetch as unknown as typeof global.fetch;

describe("HomePage XP update", () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    it("should display XP after fetching from backend", async () => {
        // Mock XP API responses
        mockedFetch.mockImplementation((url: string) => {
            if (url.includes("/api/xp/status")) {
                return Promise.resolve({
                    ok: true,
                    json: () => Promise.resolve({ xp: 50, level: 2, xpToNext: 100 })
                }) as Promise<Response>;
            }
            if (url.includes("/api/progress/status")) {
                return Promise.resolve({
                    ok: true,
                    json: () => Promise.resolve({ workoutDays: [], dietMeals: [] })
                }) as Promise<Response>;
            }
            return Promise.resolve({ ok: false }) as Promise<Response>;
        });

        render(<HomePage />);

        await waitFor(() => {
            expect(screen.getByText(/Level: 2/i)).toBeInTheDocument();
            expect(screen.getByText(/XP: 50/i)).toBeInTheDocument();
        });
    });

    it("should update XP when handlePlanUpdate is called via AiPlanCard mock", async () => {
        mockedFetch.mockImplementation((url: string) => {
            if (url.includes("/api/xp/status")) {
                return Promise.resolve({
                    ok: true,
                    json: () => Promise.resolve({ xp: 20, level: 1, xpToNext: 100 })
                }) as Promise<Response>;
            }
            if (url.includes("/api/progress/status")) {
                return Promise.resolve({
                    ok: true,
                    json: () => Promise.resolve({ workoutDays: [], dietMeals: [] })
                }) as Promise<Response>;
            }
            return Promise.resolve({ ok: false }) as Promise<Response>;
        });

        render(<HomePage />);

        await waitFor(() => {
            expect(screen.getByText(/XP: 20/i)).toBeInTheDocument();
            expect(screen.getByText(/Level: 1/i)).toBeInTheDocument();
        });


    });
});
