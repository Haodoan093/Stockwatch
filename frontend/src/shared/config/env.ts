/** Địa chỉ gốc của API. Rỗng = cùng origin (dev: proxy của Vite). */
export const API_BASE_URL: string = (import.meta.env.VITE_API_BASE_URL as string | undefined) ?? "";
