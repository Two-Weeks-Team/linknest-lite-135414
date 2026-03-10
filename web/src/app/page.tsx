"use client";

import { SearchBar } from '@/components/SearchBar';
import { Bookmarklet } from '@/components/Bookmarklet';
import { TagInput } from '@/components/TagInput';

export default function HomePage() {
  return (
    <main className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">LinkNest Lite</h1>
      <p className="mb-6">Simple bookmark saver with instant search – no login, just fast access.</p>
      <section className="mb-8">
        <h2 className="text-xl font-semibold mb-2">One‑Click Capture</h2>
        <Bookmarklet />
        <TagInput />
      </section>
      <section>
        <h2 className="text-xl font-semibold mb-2">Search Bookmarks</h2>
        <SearchBar />
      </section>
    </main>
  );
}
