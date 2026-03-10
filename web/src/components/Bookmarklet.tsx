"use client";

import { useState } from 'react';
import { createBookmark, generateAITags } from '@/lib/api';

export function Bookmarklet() {
  const [status, setStatus] = useState<string>('');

  const captureCurrentPage = async () => {
    const url = window.location.href;
    const title = document.title || url;
    setStatus('Generating AI tags…');
    let aiTags: string[] = [];
    try {
      aiTags = await generateAITags(url);
    } catch (e) {
      // fallback to empty tags on error
    }
    setStatus('Saving bookmark…');
    try {
      await createBookmark({ url, title, tags: aiTags });
      setStatus('Bookmark saved!');
    } catch (e: any) {
      setStatus(`Error: ${e.message}`);
    }
    setTimeout(() => setStatus(''), 3000);
  };

  const installBookmarklet = () => {
    const js = `javascript:(function(){
  const url=encodeURIComponent(window.location.href);
  const title=encodeURIComponent(document.title||window.location.href);
  fetch('${window.location.origin}/api/bookmarks',{
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({url:decodeURIComponent(url),title:decodeURIComponent(title)})
  }).then(()=>alert('Bookmark saved!')).catch(()=>alert('Failed to save'));
})();`;
    prompt('Drag this link to your bookmarks bar:', js);
  };

  return (
    <div className="space-x-2">
      <button
        onClick={captureCurrentPage}
        className="rounded bg-green-600 px-4 py-2 text-white hover:bg-green-700"
      >
        Capture This Page
      </button>
      <button
        onClick={installBookmarklet}
        className="rounded bg-gray-600 px-4 py-2 text-white hover:bg-gray-700"
      >
        Install Bookmarklet
      </button>
      {status && <span className="ml-2 text-sm text-gray-700">{status}</span>}
    </div>
  );
}
