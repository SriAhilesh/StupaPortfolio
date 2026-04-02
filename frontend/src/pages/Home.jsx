import React, { useState } from "react";
import axios from "axios";


export default function Home() {
  const [notionToken, setNotionToken] = useState("");
  const [pageUrl, setPageUrl] = useState("");
  const [style, setStyle] = useState("academic");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [portfolioPath, setPortfolioPath] = useState("");
  const [previewLink, setPreviewLink] = useState("");
  const [zipUrl, setZipUrl] = useState("");

  const API_BASE = "http://127.0.0.1:8000";

  const handleGenerate = async () => {
      if (!notionToken || !pageUrl) {
        setMessage("⚠️ Please fill in all fields before proceeding.");
        return;
      }

      setLoading(true);
      setMessage("⏳ Fetching Notion data & generating your portfolio...");

      try {
        // Step 1: Fetch data from Notion
        const fetchResponse = await axios.post(`${API_BASE}/fetch-data/`, {
          notion_token: notionToken,
          page_url: pageUrl,
        });

        console.log("Fetch response:", fetchResponse.data);

        // Step 2: Generate portfolio using fetched data
        const generateResponse = await axios.post(`${API_BASE}/generate_portfolio?style=${style}`);

        console.log("Generate response:", generateResponse.data);

        const { message, path, preview_url, zip_url } = generateResponse.data;

        setMessage(message);
        setPortfolioPath(path);
        setPreviewLink(`${API_BASE}${preview_url}`);
        setZipUrl(`${API_BASE}${zip_url}`);
      } catch (err) {
        console.error("Error:", err);
        setMessage(`❌ Error: ${err.response?.data?.detail || err.message}`);
      } finally {
        setLoading(false);
      }
    };


  return (
    <div className="relative flex flex-col items-center justify-center min-h-screen px-6 py-10 overflow-hidden bg-black">
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        {/* Gradient Orbs */}
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl animate-pulse" style={{animationDelay: '1s'}}></div>
        <div className="absolute top-1/2 left-1/2 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl animate-pulse" style={{animationDelay: '2s'}}></div>
        
        {/* Floating Particles */}
        {[...Array(20)].map((_, i) => (
          <div
            key={i}
            className="absolute w-1 h-1 bg-blue-400/40 rounded-full"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
              animation: `float ${5 + Math.random() * 10}s linear infinite`,
              animationDelay: `${Math.random() * 5}s`
            }}
          ></div>
        ))}
      </div>

      {/* Grid Pattern */}
      <div className="absolute inset-0 bg-[linear-gradient(rgba(59,130,246,0.05)_1px,transparent_1px),linear-gradient(90deg,rgba(59,130,246,0.05)_1px,transparent_1px)] bg-[size:50px_50px] [mask-image:radial-gradient(ellipse_80%_50%_at_50%_50%,black,transparent)]"></div>

      <style jsx>{`
        @keyframes float {
          0%, 100% {
            transform: translateY(0) translateX(0);
            opacity: 0;
          }
          10% {
            opacity: 1;
          }
          90% {
            opacity: 1;
          }
          100% {
            transform: translateY(-100vh) translateX(${Math.random() * 100 - 50}px);
            opacity: 0;
          }
        }
      `}</style>

      {/* Main Content */}
      <div className="relative z-10 flex flex-col items-center justify-center w-full">
        {/* Header */}
        <div className="text-center mb-10">
          <h1 className="text-5xl md:text-6xl font-black mb-4 bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500 bg-clip-text text-transparent animate-gradient">
            STuPA Portfolio Generator
          </h1>
          <p className="text-gray-400 text-lg">
            Create your professional portfolio directly from your Notion page
          </p>
          <div className="flex justify-center gap-2 mt-4">
            <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
            <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
            <div className="w-2 h-2 bg-pink-500 rounded-full animate-bounce" style={{animationDelay: '0.4s'}}></div>
          </div>

          {/* ✅ New Portfolio Template Button */}
          {/* ✅ Enhanced Portfolio Template Button */}
          <div className="mt-10">
            <a
              href="https://tide-cell-82a.notion.site/STuPA-Portfolio-Data-698267856f734c55b0f82bb97f8a5062"
              target="_blank"
              rel="noopener noreferrer"
              className="relative inline-flex items-center justify-center px-8 py-3 rounded-xl font-bold text-lg text-white overflow-hidden group"
            >
              {/* Animated Gradient Border */}
              <span className="absolute inset-0 w-full h-full bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 rounded-xl blur-md opacity-70 group-hover:opacity-100 transition duration-500 animate-pulse"></span>

              {/* Inner Glow Layer */}
              <span className="absolute inset-[2px] bg-gray-900 rounded-xl z-0"></span>

              {/* Button Content */}
              <span className="relative z-10 flex items-center gap-2">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth="1.8"
                  stroke="currentColor"
                  className="w-6 h-6 text-blue-400 animate-bounce-slow"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-3-3v6m-7.5-3a9 9 0 1118 0 9 9 0 01-18 0z" />
                </svg>
                Duplicate Portfolio Template
              </span>

              {/* Animated Glow Underlay */}
              <span className="absolute -inset-1 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 opacity-0 group-hover:opacity-40 blur-2xl transition-all duration-700 rounded-xl"></span>
            </a>
          </div>

        </div>

        {/* Form Card */}
        <div className="w-full max-w-xl bg-gray-900/40 backdrop-blur-xl p-8 rounded-3xl border border-gray-700/50 shadow-2xl relative overflow-hidden group">
          {/* Card Glow Effect */}
          <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 via-purple-500/10 to-pink-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          
          {/* Border Animation */}
          <div className="absolute inset-0 rounded-3xl bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 opacity-20 blur-xl group-hover:opacity-40 transition-opacity duration-500"></div>

          <div className="relative z-10">
            {/* Token Input */}
            <div className="mb-6">
              <label className="block mb-2 text-gray-300 font-medium flex items-center gap-2">
                <span className="text-xl">🔑</span> Notion Integration Token
              </label>
              <div className="relative">
                <input
                  type="password"
                  value={notionToken}
                  onChange={(e) => setNotionToken(e.target.value)}
                  placeholder="secret_xxxxxxxxxxxxxx"
                  className="w-full p-4 rounded-xl bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 outline-none transition-all duration-300 text-white placeholder-gray-500"
                />
                <div className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-500">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </div>
              </div>
            </div>

            {/* URL Input */}
            <div className="mb-6">
              <label className="block mb-2 text-gray-300 font-medium flex items-center gap-2">
                <span className="text-xl">🔗</span> Notion Page URL
              </label>
              <div className="relative">
                <input
                  type="text"
                  value={pageUrl}
                  onChange={(e) => setPageUrl(e.target.value)}
                  placeholder="https://www.notion.so/your-page-link"
                  className="w-full p-4 rounded-xl bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 focus:border-purple-500 focus:ring-2 focus:ring-purple-500/20 outline-none transition-all duration-300 text-white placeholder-gray-500"
                />
                <div className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-500">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                  </svg>
                </div>
              </div>
            </div>

            {/* Style Selection */}
            <div className="mb-6">
              <label className="block mb-2 text-gray-300 font-medium flex items-center gap-2">
                <span className="text-xl">🎨</span> Portfolio Type
              </label>
              <div className="relative">
                <select
                  value={style}
                  onChange={(e) => setStyle(e.target.value)}
                  className="w-full p-4 rounded-xl bg-gray-800/50 backdrop-blur-sm border border-gray-700/50 focus:border-pink-500 focus:ring-2 focus:ring-pink-500/20 outline-none transition-all duration-300 text-white appearance-none cursor-pointer"
                >
                  <option value="academic">Academic</option>
                  <option value="industry">Industry</option>
                </select>
                <div className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-500 pointer-events-none">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </div>
              </div>
            </div>

            {/* Generate Button */}
            <button
              onClick={handleGenerate}
              disabled={loading}
              className={`w-full p-4 rounded-xl font-bold text-lg transition-all duration-300 relative overflow-hidden group/btn ${
                loading
                  ? "bg-gray-700 text-gray-400 cursor-not-allowed"
                  : "bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 hover:shadow-lg hover:shadow-purple-500/50 hover:scale-[1.02] active:scale-[0.98]"
              }`}
            >
              {!loading && (
                <div className="absolute inset-0 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 opacity-0 group-hover/btn:opacity-100 transition-opacity duration-300"></div>
              )}
              <span className="relative z-10 flex items-center justify-center gap-2">
                {loading ? (
                  <>
                    <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Generating...
                  </>
                ) : (
                  <>
                    Generate Portfolio
                    <span className="text-2xl">🚀</span>
                  </>
                )}
              </span>
            </button>

            {/* Message Box */}
            {message && (
              <div className={`mt-6 p-4 rounded-xl text-center backdrop-blur-sm border transition-all duration-500 animate-in slide-in-from-bottom-4 ${
                message.includes("❌") 
                  ? "bg-red-500/10 border-red-500/30 text-red-400"
                  : message.includes("⚠️")
                  ? "bg-yellow-500/10 border-yellow-500/30 text-yellow-400"
                  : message.includes("⏳")
                  ? "bg-blue-500/10 border-blue-500/30 text-blue-400"
                  : "bg-green-500/10 border-green-500/30 text-green-400"
              }`}>
                {message}
              </div>
            )}

            {/* Preview Section */}
            {portfolioPath && !loading && (
              <div className="mt-8 bg-gradient-to-br from-gray-900/60 to-gray-800/40 backdrop-blur-sm p-6 rounded-2xl border border-gray-700/50 shadow-xl animate-in slide-in-from-bottom-4">
                <div className="text-center mb-6">
                  <div className="inline-flex items-center justify-center w-16 h-16 bg-green-500/20 rounded-full mb-4">
                    <span className="text-3xl">✅</span>
                  </div>
                  <h3 className="text-green-400 text-xl font-bold mb-2">
                    Portfolio Generated Successfully!
                  </h3>
                  <p className="text-gray-400 text-sm">
                    Style: <span className="text-transparent bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text font-semibold">{style.toUpperCase()}</span>
                  </p>
                </div>

                <div className="flex flex-col sm:flex-row justify-center gap-4">
                  {/* Preview Portfolio */}
                  <a
                    href={previewLink}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex-1 px-6 py-3 rounded-xl font-semibold bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 hover:scale-105 active:scale-95 transition-all text-white shadow-lg hover:shadow-blue-500/50 flex items-center justify-center gap-2"
                  >
                    <span className="text-xl">🌐</span>
                    Preview Portfolio
                  </a>

                  {/* Download ZIP */}
                  <a
                    href={zipUrl}
                    className="flex-1 px-6 py-3 rounded-xl font-semibold bg-gradient-to-r from-purple-500 to-pink-600 hover:from-purple-600 hover:to-pink-700 hover:scale-105 active:scale-95 transition-all text-white shadow-lg hover:shadow-pink-500/50 flex items-center justify-center gap-2"
                  >
                    <span className="text-xl">⬇️</span>
                    Download ZIP
                  </a>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-8 text-gray-500 text-sm">
          <p>Powered by Notion API & Modern Web Technologies</p>
        </div>
      </div>
    </div>
  );
}