import {render, screen, waitFor} from "@testing-library/react";
import HomePage from "../../pages/HomePage";
import "@testing-library/jest-dom";
import {MemoryRouter} from "react-router-dom";

// ------------------------------------------------------------------
// 1. MOCK KOMPONENSEK
// ------------------------------------------------------------------


jest.mock("../../components/ThemeSwitcher", () => {
    return function DummyThemeSwitcher() {
        return <div data-testid="theme-switcher-mock">Theme Switcher</div>;
    };
});


jest.mock("../../components/GoalsComponent", () => {
    return function DummyGoalsComponent() {
        return <div data-testid="goals-mock">Goals Component</div>;
    };
});


jest.mock("../../components/StatComponent", () => {
    return function DummyStatComponent(props: { level: number; xp: number }) {
        return (
            <div data-testid="stat-mock">
                <p>Level: {props.level}</p>
                <p>XP: {props.xp}</p>
            </div>
        );
    };
});


const mockedFetch = jest.fn();
global.fetch = mockedFetch;


const createFetchResponse = (data: unknown) => {
    return {
        ok: true,
        json: async () => data
    } as Response;
};

describe("HomePage XP update", () => {
    beforeEach(() => {

        jest.clearAllMocks();


        Object.defineProperty(window, 'localStorage', {
            value: {
                getItem: jest.fn(() => "fake-token"),
                setItem: jest.fn(),
                removeItem: jest.fn(),
                clear: jest.fn(),
            },
            writable: true
        });
    });

    it("should display XP after fetching from backend", async () => {

        const responseData = {
            xp: 50,
            level: 2,
            xpToNext: 100,
            longGoals: [],
            tips: []
        };


        mockedFetch.mockResolvedValue(createFetchResponse(responseData));

        render(
            <MemoryRouter>
                <HomePage/>
            </MemoryRouter>
        );


        await waitFor(() => {
            expect(screen.getByText(/Level: 2/i)).toBeInTheDocument();
            expect(screen.getByText(/XP: 50/i)).toBeInTheDocument();
        });
    });

    it("should update XP when handlePlanUpdate is called", async () => {

        const responseData = {
            xp: 20,
            level: 1,
            xpToNext: 100,
            longGoals: [],
            tips: []
        };

        mockedFetch.mockResolvedValue(createFetchResponse(responseData));

        render(
            <MemoryRouter>
                <HomePage/>
            </MemoryRouter>
        );

        await waitFor(() => {
            expect(screen.getByText(/XP: 20/i)).toBeInTheDocument();
            expect(screen.getByText(/Level: 1/i)).toBeInTheDocument();
        });
    });
});