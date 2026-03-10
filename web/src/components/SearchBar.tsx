"use client";

import { useState, FormEvent } from 'react';
import { searchBookmarks } from '@/lib/api';

type Bookmark = {
  id: string;
  url: string;
  title: string;
  tags: string[];
  created_at: string;
};

export function SearchBar() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<Bookmark[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const data = await searchBookmarks(query);
      setResults(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          placeholder="Search bookmarks..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="flex-1 rounded border px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          disabled={loading}
          className="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Searching...' : 'Search'}
        </button>
      </form>
      {error && <p className="text-red-600">{error}</p>}
      <ul className="list-disc pl-5 space-y-2">
        {results.map((bm) => (
          <li key={bm.id} className="border-b pb-2">
            <a href={bm.url} target="_blank" rel="noopener noreferrer" className="font-medium text-blue-600 hover:underline">
              {bm.title}
            </a>
            {bm.tags.length > 0 && (
              <p className="text-sm text-gray-600">Tags: {bm.tags.join(', ')}</p>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
