export function extractTextInParentheses(text: string | null): string {
    if (!text) {
        return ''; // Или любое другое значение по умолчанию, если text равен null
    }
    const match = text.match(/\((.*?)\)/);
    return match ? match[1] : '';
}