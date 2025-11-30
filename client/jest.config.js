export default {
    preset: 'ts-jest/presets/js-with-ts-esm',
    testEnvironment: 'jest-environment-jsdom',
    setupFilesAfterEnv: ['<rootDir>/src/setupTests.ts'],
    moduleNameMapper: {
        '\\.(css|scss)$': 'identity-obj-proxy'
    },
    transform: {
        '^.+\\.tsx?$': ['ts-jest', { useESM: true , tsconfig: './tsconfig.jest.json', }]
    },
    extensionsToTreatAsEsm: ['.ts', '.tsx'],
};
