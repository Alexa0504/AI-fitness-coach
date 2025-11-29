import "@testing-library/jest-dom";
import { Buffer } from "buffer";


class MyTextEncoder {
    encode(str: string) {
        return new Uint8Array([...Buffer.from(str)]);
    }
}

class MyTextDecoder {
    decode(buffer: Uint8Array) {
        return Buffer.from(buffer).toString();
    }
}

(global as any).TextEncoder = MyTextEncoder;
(global as any).TextDecoder = MyTextDecoder;
