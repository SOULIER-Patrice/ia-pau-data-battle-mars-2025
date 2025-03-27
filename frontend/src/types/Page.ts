import type { Message } from "./Message";

export type Page = {
    id: string;
    title: string;
    book_id: string;
    history: Array<Message>;
    created_at: string;
    qa_id: string;
    category: string;
    question: string;
    options: Array<string>;
    answer: string;
    justification: string;
    isVerified: boolean;
};