// Утилита для установки cookie с типизацией
export function setCookie(name: string, value: string, hours: number): void {
    const date = new Date();
    date.setTime(date.getTime() + hours * 60 * 60 * 1000);
    document.cookie = `${name}=${value}; path=/; expires=${date.toUTCString()}; SameSite=None; Secure`;
}
