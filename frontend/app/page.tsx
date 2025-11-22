"use client";


export default function Home() {
  return (
    <div className="h-screen flex flex-col items-center justify-center">
      <h1 className="text-4xl font-bold mb-6">
        Smart Content Finder
      </h1>

      <div className="flex gap-6">
        <a
          href="/pdf"
          className="px-6 py-3 bg-blue-600 text-white rounded-lg"
        >
          Summarize PDF
        </a>

        <a
          href="/youtube"
          className="px-6 py-3 bg-purple-600 text-white rounded-lg"
        >
          Summarize YouTube Video
        </a>
      </div>
    </div>
  );
}
