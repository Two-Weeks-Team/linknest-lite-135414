type BookmarkPayload = {
  url: string;
  title: string;
  tags?: string[];
};

type BookmarkResponse = {
  id: string;
  url: string;
  title: string;
  tags: string[];
  created_at: string;
};

type SearchResult = BookmarkResponse[];

type GeneratedTags = { generated_tags: string[] };

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || '/api';

export async function createBookmark(payload: BookmarkPayload): Promise<BookmarkResponse> {
  const res = await fetch(`${API_BASE_URL}/bookmarks`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.message ?? 'Failed to create bookmark');
  }
  return res.json();
}

export async function searchBookmarks(query: string): Promise<SearchResult> {
  const res = await fetch(`${API_BASE_URL}/bookmarks?search=${encodeURIComponent(query)}`);
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.message ?? 'Search failed');
  }
  return res.json();
}

export async function generateAITags(url: string): Promise<string[]> {
  const res = await fetch(`${API_BASE_URL}/ai/generate-tags`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.message ?? 'AI tag generation failed');
  }
  const data: GeneratedTags = await res.json();
  return data.generated_tags;
}
