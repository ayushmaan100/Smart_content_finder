"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { supabase } from "@/lib/supabaseClient";

type Summary = {
  id: string;
  title: string;
  source_type: string;
  created_at: string;
};

export default function DashboardPage() {
  const [summaries, setSummaries] = useState<Summary[]>([]);

  useEffect(() => {
    (async () => {
      const { data: { session } } = await supabase.auth.getSession();
      const res = await api.get("/summary/list", {
        headers: { Authorization: `Bearer ${session?.access_token}` },
      });
      setSummaries(res.data);
    })();
  }, []);

  return (
    <div className="p-8">
      <h1 className="text-2xl font-semibold mb-4">Your Summaries</h1>
      <ul className="space-y-2">
        {summaries.map((s) => (
          <li key={s.id} className="border p-3 rounded">
            <a href={`/summary/${s.id}`} className="font-medium">
              {s.title} ({s.source_type})
            </a>
            <div className="text-sm text-gray-500">
              {new Date(s.created_at).toLocaleString()}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
