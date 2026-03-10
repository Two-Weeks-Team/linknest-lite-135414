"use client";

import { useState, FormEvent } from 'react';
import { createBookmark } from '@/lib/api';

export function TagInput() {
  const [url, setUrl] = useState('');
  const [title, setTitle] = useState('');
  const [tags, setTags] = useState('');
  const [status, setStatus] = useState<string>('');

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setStatus('Saving…');
    const tagArray = tags
      .split(',')
      .map((t) => t.trim())
      .filter(Boolean);
    try {
      await createBookmark({ url, title, tags: tagArray });
      setStatus('Saved!');
      setUrl('');
      setTitle('');
      setTags('');
    } catch (err: any) {
      setStatus(`Error: ${err.message}`);
    }
    setTimeout(() => setStatus(''), 3000);
  };

  return (
    <form onSubmit={handleSubmit} className="mt-4 space-y-2 max-w-lg">
      <div>
        <label className="block text-sm font-medium">URL</label>
        <input
          type="url"
          required
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="w-full rounded border px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      <div>
        <label className="block text-sm font-medium">Title</label>
        <input
          type="text"
          required
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full rounded border px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      <div>
        <label className="block text-sm font-medium">Tags (comma separated)</label>
        <input
          type="text"
          value={tags}
          onChange={(e) => setTags(e.target.value)}
          placeholder="e.g., research, ai"
          className="w-full rounded border px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      <button
        type="submit"
        className="rounded bg-indigo-600 px-4 py-2 text-white hover:bg-indigo-700"
      >
        Save Bookmark
      </button>
      {status && <p className="mt-2 text-sm text-gray-700">{status}</p>}
    </form>
  );
}
