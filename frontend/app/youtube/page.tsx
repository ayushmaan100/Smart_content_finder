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



export default function YouTubePage() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState("");

  const handleSummarize = async () => {
    setLoading(true);
    const res = await api.post("/youtube/summarize", { url });
    setResult(res.data.summary);
    setLoading(false);
  };

  return (
    <div className="p-10">
      <h1 className="text-3xl font-semibold mb-4">YouTube Summarizer</h1>

      <input
        type="text"
        placeholder="Paste YouTube URL"
        className="border p-2 w-1/2"
        onChange={(e) => setUrl(e.target.value)}
      />

      <button
        onClick={handleSummarize}
        className="px-5 py-2 bg-purple-600 text-white rounded-lg ml-3"
      >
        Summarize
      </button>

      {loading && <p className="mt-4">Processing…</p>}

      {result && (
        <div className="mt-6 whitespace-pre-wrap bg-gray-100 p-4 rounded">
          {result}
        </div>
      )}
    </div>
  );
}
