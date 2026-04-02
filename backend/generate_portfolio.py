# generate_portfolio.py
import json, os

def build_portfolio_html(portfolio):
    user = portfolio.get("user", {})
    projects = portfolio.get("projects", [])
    education = portfolio.get("education", [])
    skills = portfolio.get("skills", [])
    experience = portfolio.get("experience", [])

    name = user.get("name", "Your Name")
    tagline = user.get("portfolio_tagline", "Building Ideas into Reality")
    email = user.get("email", "example@example.com")
    bio = user.get("short_bio", "A passionate developer exploring innovation and technology.")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{name} | Portfolio</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    body {{ font-family: 'Inter', sans-serif; }}
    html {{ scroll-behavior: smooth; }}
  </style>
</head>

<body class="bg-gray-50 text-gray-800">
  <!-- Navbar -->
  <nav class="bg-white shadow sticky top-0 z-50">
    <div class="max-w-6xl mx-auto px-4 py-3 flex justify-between items-center">
      <h1 class="text-xl font-bold text-blue-600">{name}</h1>
      <div class="space-x-6 hidden md:block">
        <a href="#about" class="hover:text-blue-500">About</a>
        <a href="#projects" class="hover:text-blue-500">Projects</a>
        <a href="#experience" class="hover:text-blue-500">Experience</a>
        <a href="#education" class="hover:text-blue-500">Education</a>
        <a href="#skills" class="hover:text-blue-500">Skills</a>
        <a href="#contact" class="hover:text-blue-500">Contact</a>
      </div>
    </div>
  </nav>

  <!-- Hero Section -->
  <section class="bg-gradient-to-r from-blue-600 to-indigo-600 text-white py-24 text-center">
    <h1 class="text-5xl font-bold mb-4">{name}</h1>
    <p class="text-xl mb-6">{tagline}</p>
    <a href="#contact" class="bg-white text-blue-700 font-semibold px-6 py-2 rounded shadow hover:bg-gray-100">Contact Me</a>
  </section>

  <!-- About Section -->
  <section id="about" class="max-w-5xl mx-auto px-4 py-16">
    <h2 class="text-3xl font-semibold text-blue-600 mb-6">About</h2>
    <p class="text-lg leading-relaxed">{bio}</p>
  </section>

  <!-- Projects Section -->
  <section id="projects" class="bg-white py-16">
    <div class="max-w-6xl mx-auto px-4">
      <h2 class="text-3xl font-semibold text-blue-600 mb-10 text-center">Projects</h2>
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {''.join(f'''
        <div class="bg-gray-50 rounded-xl shadow hover:shadow-md transition p-6">
          <h3 class="text-xl font-bold text-blue-700 mb-2">{p.get('project_title')}</h3>
          <p class="text-gray-600 text-sm mb-3">{p.get('short_summary')}</p>
          <a href="{p.get('project_link', '#')}" class="text-blue-500 font-semibold hover:underline">View Project →</a>
        </div>
        ''' for p in projects)}
      </div>
    </div>
  </section>

  <!-- Experience Section -->
  <section id="experience" class="max-w-6xl mx-auto px-4 py-16">
    <h2 class="text-3xl font-semibold text-blue-600 mb-10 text-center">Experience</h2>
    <div class="space-y-6">
      {''.join(f'''
      <div class="bg-white p-6 rounded-xl shadow hover:shadow-md transition">
        <h3 class="text-xl font-bold text-gray-800">{exp.get('role')}</h3>
        <p class="text-sm text-gray-500">{exp.get('organization')} ({exp.get('duration')})</p>
        <p class="mt-3 text-gray-700">{exp.get('description')}</p>
      </div>
      ''' for exp in experience)}
    </div>
  </section>

  <!-- Education Section -->
  <section id="education" class="bg-gray-50 py-16">
    <div class="max-w-6xl mx-auto px-4">
      <h2 class="text-3xl font-semibold text-blue-600 mb-10 text-center">Education</h2>
      <div class="grid md:grid-cols-2 gap-6">
        {''.join(f'''
        <div class="bg-white p-6 rounded-xl shadow hover:shadow-md transition">
          <h3 class="text-xl font-bold text-gray-800">{edu.get('degree')}</h3>
          <p class="text-gray-600">{edu.get('institution')}</p>
          <p class="text-sm text-gray-500 mt-1">{edu.get('duration')}</p>
        </div>
        ''' for edu in education)}
      </div>
    </div>
  </section>

  <!-- Skills Section -->
  <section id="skills" class="max-w-6xl mx-auto px-4 py-16">
    <h2 class="text-3xl font-semibold text-blue-600 mb-10 text-center">Skills</h2>
    <div class="flex flex-wrap justify-center gap-3">
      {''.join(f'<span class="bg-blue-100 text-blue-700 px-4 py-2 rounded-full text-sm font-medium">{s.get("skill_name")}</span>' for s in skills)}
    </div>
  </section>

  <!-- Contact Section -->
  <section id="contact" class="bg-blue-600 text-white py-16 text-center">
    <h2 class="text-3xl font-semibold mb-6">Get in Touch</h2>
    <p class="mb-4 text-lg">I'd love to connect and collaborate!</p>
    <a href="mailto:{email}" class="bg-white text-blue-700 px-6 py-2 rounded font-semibold hover:bg-gray-100">📩 {email}</a>
  </section>

  <footer class="bg-gray-900 text-gray-300 text-center py-6">
    <p>© {name} — Built with ❤️ using Python & Tailwind CSS</p>
  </footer>

</body>
</html>"""
    return html


if __name__ == "__main__":
    input_path = "outputs/portfolio.json"
    output_dir = "outputs/portfolio_site"
    os.makedirs(output_dir, exist_ok=True)

    with open(input_path, "r", encoding="utf-8") as f:
        portfolio_data = json.load(f)

    html_content = build_portfolio_html(portfolio_data)

    output_path = os.path.join(output_dir, "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ Modern portfolio website generated at: {output_path}")
