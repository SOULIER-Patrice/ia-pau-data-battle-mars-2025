export type QA = {
    id: string;
    type: string;
    categories: string[];
    question: string;
    answer: string;
    is_verified: boolean;
    options?: string[];
    justification?: string;
};