const [flashcards, setFlashcards] = useState<string | null>(null);
const [mcqs, setMcqs] = useState<string | null>(null);

async function fetchFlashcards() {
  const { data: { session } } = await supabase.auth.getSession();

  const res = await api.get(`/summary/${params.id}/flashcards`, {
    headers: { Authorization: `Bearer ${session?.access_token}` }
  });

  setFlashcards(res.data.flashcards);
}

async function fetchMCQs() {
  const { data: { session } } = await supabase.auth.getSession();

  const res = await api.get(`/summary/${params.id}/mcqs`, {
    headers: { Authorization: `Bearer ${session?.access_token}` }
  });

  setMcqs(res.data.mcqs);
}

<div className="mt-4 flex gap-4">
  <button
    onClick={fetchFlashcards}
    className="px-4 py-2 bg-blue-600 text-white rounded"
  >
    Generate Flashcards
  </button>

  <button
    onClick={fetchMCQs}
    className="px-4 py-2 bg-green-600 text-white rounded"
  >
    Generate MCQs
  </button>
</div>

{flashcards && (
  <div className="mt-6 p-4 bg-gray-100 rounded whitespace-pre-wrap">
    <h2 className="text-xl font-bold mb-2">Flashcards</h2>
    {flashcards}
  </div>
)}

{mcqs && (
  <div className="mt-6 p-4 bg-gray-100 rounded whitespace-pre-wrap">
    <h2 className="text-xl font-bold mb-2">MCQs</h2>
    {mcqs}
  </div>
)}
