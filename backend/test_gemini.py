import os
from dotenv import load_dotenv
import google.generativeai as genai

# 1. Load .env and get the key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise SystemExit("❌ GEMINI_API_KEY missing in .env file.")

# 2. Configure the SDK
try:
    genai.configure(api_key=API_KEY)
    print("✅ Gemini configured successfully.")
except Exception as e:
    raise SystemExit(f"❌ Failed to configure Gemini: {e}")

# 3. Create model instance (latest Gemini 2.5)
model_name = "gemini-2.5-flash"
model = genai.GenerativeModel(model_name)
print(f"Using model: {model_name}")

# 4. Simple test prompt
prompt = "Write one short motivational line for a student portfolio project."

try:
    response = model.generate_content(prompt)
    print("\n✅ Response received successfully!")
    print("----------------------------------")
    print(response.text.strip())
    print("----------------------------------")
except Exception as e:
    print(f"\n❌ Gemini generation failed: {type(e).__name__}: {e}")



# # test_gemini_robust.py
# import os
# from dotenv import load_dotenv

# load_dotenv()
# API_KEY = os.getenv("GEMINI_API_KEY")
# if not API_KEY:
#     raise SystemExit("Set GEMINI_API_KEY in .env before running this test.")

# import google.generativeai as genai
# import traceback
# print("SDK module:", genai.__name__, "version (if exposed):", getattr(genai, "__version__", "unknown"))

# # configure
# try:
#     genai.configure(api_key=API_KEY)
#     print("Configured genai with provided API key.")
# except Exception as e:
#     print("Failed to configure genai:", type(e).__name__, e)
#     raise

# model_name = "gemini-2.5-flash"
# prompt = "Write one short, encouraging sentence about this project."

# # helper to safely extract text from varied response shapes
# def extract_text(resp):
#     # common shapes
#     try:
#         if resp is None:
#             return None
#         # resp.text
#         if hasattr(resp, "text") and isinstance(resp.text, str):
#             return resp.text
#         # resp.output_text or resp.output
#         if isinstance(resp, dict):
#             # nested structures
#             if "output" in resp:
#                 out = resp["output"]
#                 if isinstance(out, list) and out and isinstance(out[0], dict):
#                     # try to find text
#                     first = out[0]
#                     # many variants:
#                     for k in ("content", "text", "output_text", "message"):
#                         if k in first:
#                             v = first[k]
#                             if isinstance(v, str):
#                                 return v
#                             # if list, join texts
#                             if isinstance(v, list):
#                                 # look for dicts with 'text' or 'plain_text'
#                                 texts = []
#                                 for item in v:
#                                     if isinstance(item, dict):
#                                         for tk in ("text", "plain_text", "content"):
#                                             if tk in item and isinstance(item[tk], str):
#                                                 texts.append(item[tk])
#                                 if texts:
#                                     return "\n".join(texts)
#             # top-level 'text' key
#             if "text" in resp and isinstance(resp["text"], str):
#                 return resp["text"]
#         # for objects with 'choices' like older chat completions
#         if hasattr(resp, "choices") and isinstance(resp.choices, (list, tuple)) and resp.choices:
#             c = resp.choices[0]
#             # this may have .message.content or .text
#             if hasattr(c, "message") and isinstance(c.message, dict):
#                 return c.message.get("content") or c.message.get("text")
#             if hasattr(c, "text"):
#                 return c.text
#             if isinstance(c, dict):
#                 # dict choice
#                 if "message" in c and isinstance(c["message"], dict):
#                     return c["message"].get("content") or c["message"].get("text")
#                 if "text" in c:
#                     return c["text"]
#     except Exception:
#         pass
#     # last resort: repr
#     return repr(resp)

# attempts = []

# # Attempt 1: genai.generate_text (some versions)
# try:
#     print("\nAttempt 1: genai.generate_text(...)")
#     resp = genai.generate_text(model=model_name, prompt=prompt, temperature=0.2, max_output_tokens=200)
#     text = extract_text(resp)
#     print("SUCCESS (generate_text). Output:\n", text)
#     raise SystemExit(0)
# except Exception as e:
#     print("Attempt 1 failed:", type(e).__name__, str(e))
#     attempts.append(("generate_text", traceback.format_exc()))

# # Attempt 2: genai.models.generate(...) (newer SDK pattern)
# try:
#     print("\nAttempt 2: genai.models.generate(...)")
#     # some SDK versions expect genai.models.generate or genai.models.generate_text
#     if hasattr(genai, "models") and hasattr(genai.models, "generate"):
#         resp = genai.models.generate(model=model_name, prompt=prompt, temperature=0.2, max_output_tokens=200)
#         text = extract_text(resp)
#         print("SUCCESS (models.generate). Output:\n", text)
#         raise SystemExit(0)
#     else:
#         raise AttributeError("genai.models.generate not found")
# except Exception as e:
#     print("Attempt 2 failed:", type(e).__name__, str(e))
#     attempts.append(("models.generate", traceback.format_exc()))

# # Attempt 3: genai.chat.completions.create(...) (chat-style)
# try:
#     print("\nAttempt 3: genai.chat.completions.create(...)")
#     if hasattr(genai, "chat") and hasattr(genai.chat, "completions") and hasattr(genai.chat.completions, "create"):
#         resp = genai.chat.completions.create(
#             model=model_name,
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.2,
#             max_output_tokens=200
#         )
#         text = extract_text(resp)
#         print("SUCCESS (chat.completions.create). Output:\n", text)
#         raise SystemExit(0)
#     else:
#         raise AttributeError("genai.chat.completions.create not available")
# except Exception as e:
#     print("Attempt 3 failed:", type(e).__name__, str(e))
#     attempts.append(("chat.completions.create", traceback.format_exc()))

# # Attempt 4: genai.create(...) (older or different)
# try:
#     print("\nAttempt 4: genai.create(...)")
#     if hasattr(genai, "create"):
#         resp = genai.create(model=model_name, prompt=prompt, temperature=0.2, max_output_tokens=200)
#         text = extract_text(resp)
#         print("SUCCESS (create). Output:\n", text)
#         raise SystemExit(0)
#     else:
#         raise AttributeError("genai.create not available")
# except Exception as e:
#     print("Attempt 4 failed:", type(e).__name__, str(e))
#     attempts.append(("create", traceback.format_exc()))

# # If we get here, nothing worked. Print diagnostics.
# print("\nAll attempts failed. Diagnostics summary:")
# for name, tb in attempts:
#     print("\n--- Attempt:", name, "---")
#     print(tb)

# print("\nSuggestion:")
# print("1) Ensure 'google-generativeai' is upgraded: pip install --upgrade google-generativeai")
# print("2) Check the package version: pip show google-generativeai")
# print("3) Paste the above tracebacks if you want me to adapt a precise call pattern for your installed SDK.")
