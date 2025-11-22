"use client";

import { useState } from "react";
import { api } from "@/lib/api";
import { supabase } from "@/lib/supabaseClient";


async function callBackend(formData: FormData) {
  const { data: { session } } = await supabase.auth.getSession();

  const res = await api.post("/pdf/summarize", formData, {
    headers: {
      Authorization: `Bearer ${session?.access_token}`,
    },
  });

  return res.data;
}


export default function PDFPage() {
  // Selected PDF file
  const [file, setFile] = useState<File | null>(null);
  // Spinner / disabled state while request is in-flight
  const [loading, setLoading] = useState(false);
  // Holds the generated summary returned by the backend
  const [result, setResult] = useState("");
  // Holds any error message encountered during upload/summarization
  const [error, setError] = useState<string | null>(null);

  const handleUpload = async () => {
    if (!file) return;
    // Basic MIME type check (helpful but not foolproof if browser mislabels)
    if (file.type !== "application/pdf") {
      setError("Please select a PDF file.");
      return;
    }
    setError(null);
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);
    try {
      // Axios automatically sets the correct multipart boundary; explicit header optional.
      const res = await api.post("/pdf/summarize", formData);
      setResult(res.data.summary);
    } catch (err: any) {
      // Derive a human-friendly message from Axios error shape.
      const msg = err?.response?.data?.detail || err?.message || "Upload failed";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-10">
      <h1 className="text-3xl font-semibold mb-4">PDF Summarizer</h1>

      <input
        type="file"
        accept="application/pdf"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
        className="mb-4"
      />

      <button
        onClick={handleUpload}
        disabled={!file || loading}
        className="px-5 py-2 bg-blue-600 text-white rounded-lg disabled:opacity-50"
      >
        {loading ? "Summarizing..." : "Summarize"}
      </button>

      {loading && <p className="mt-4 text-sm text-gray-600">Processing…</p>}

      {error && (
        <p className="mt-4 text-sm text-red-600">{error}</p>
      )}

      {result && (
        <div className="mt-6 whitespace-pre-wrap bg-gray-100 p-4 rounded">
          {result}
        </div>
      )}
    </div>
  );
}
