/**
 * Centralized Axios client for calling the FastAPI backend.
 *
 * Why have this file?
 * - Keep a single place to configure baseURL, timeouts, headers, and interceptors.
 * - Import `api` anywhere in the app instead of repeating the backend URL.
 *
 * Usage examples:
 * - JSON POST (YouTube summarize):
 *     await api.post('/youtube/summarize', { url })
 * - Multipart POST (PDF summarize):
 *     const form = new FormData();
 *     form.append('file', file);
 *     await api.post('/pdf/summarize', form, { headers: { 'Content-Type': 'multipart/form-data' } });
 *
 * Note:
 * - baseURL currently points to localhost for local development.
 *   After deployment, consider reading from an env var like `NEXT_PUBLIC_API_URL`.
 */
import axios from "axios";

export const api = axios.create({
  // Base URL for your FastAPI server (local dev default). Change after deploy.
  // In production, you can swap this with process.env.NEXT_PUBLIC_API_URL.
  baseURL: "http://localhost:8000",
});
