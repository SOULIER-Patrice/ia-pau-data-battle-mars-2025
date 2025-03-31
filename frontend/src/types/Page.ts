import type { Message } from "./Message";

export type Page = {
    id: string;
    title: string;
    book_id: string;
    history: Message[];
    created_at: string;
    qa_id: string;
    categories: string[];
    question: string;
    options: string[];
    answer: string;
    justification: string;
    isVerified: boolean;
};