"""Build the static pages for vuongdinhtrung.github.io into the folder given as argv[1]."""
import sys, os, html, json, datetime

OUT = sys.argv[1]
YEAR = 2026
UPDATED = "October 2026"

# Auto-updated data (written by _src/update.py via GitHub Actions every 3 days)
_DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")
AUTO = json.load(open(_DATA_FILE, encoding="utf-8")) if os.path.exists(_DATA_FILE) else {}
if AUTO.get("checked"):
    UPDATED = datetime.datetime.strptime(AUTO["checked"], "%Y-%m").strftime("%B %Y")

NAV = [("index.html", "about"), ("team.html", "team"), ("publications.html", "publications"),
       ("outreach.html", "outreach"), ("news.html", "news"), ("contact.html", "contact")]

EMAIL = "trung.vd2@vinuni.edu.vn"
LINKS = {
    "scholar": "https://scholar.google.com/citations?user=-c7W-o0AAAAJ",
    "orcid": "https://orcid.org/0000-0001-5032-292X",
    "github": "https://github.com/vdtrung96",
    "linkedin": "https://www.linkedin.com/in/trung-vuong",
    "cv": "https://docs.google.com/document/d/1NEw9mI0M1JVqCwqg6WKjQTHhJ649v-qM/edit?usp=sharing&ouid=101029776121650064169&rtpof=true&sd=true",
    "cmit": "https://cmit.vinuni.edu.vn/",
    "researchmap": "https://researchmap.jp/trung-vuong",
    "cecs": "https://cecs.vinuni.edu.vn/",
    "cei": "https://cei.vinuni.edu.vn/",
    "textiles": "https://www.shinshu-u.ac.jp/faculty/textiles/english/",
    "yuwa": "https://www.yuwa-net.co.jp/",
    "vmr": "http://www.vmr.vn/",
    "eyh": "https://eyhcnc.com/",
}


def page(fname, title, body, desc):
    menu = "\n".join(
        f'      <li><a href="{h}"{" class=\"active\"" if h == fname else ""}>{label}</a></li>'
        for h, label in NAV)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{html.escape(desc)}">
  <meta name="author" content="Vuong Dinh Trung">
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,300;0,400;0,700;1,400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
  <link rel="stylesheet" href="style.css">
</head>
<body>
<header class="banner">
  <nav class="nav">
    <ul class="menu">
{menu}
    </ul>
  </nav>
  <div class="tagline">Fibers &middot; Sensing &middot; AI</div>
</header>
<main class="wrap">
{body}
</main>
<footer class="wrap">
  &copy; {YEAR} Vuong Dinh Trung &middot; VinUniversity &middot; Last updated {UPDATED}
</footer>
</body>
</html>
"""


def icons():
    return f"""<div class="icons">
  <a class="i-cv" href="{html.escape(LINKS['cv'])}" title="Curriculum Vitae" aria-label="Curriculum Vitae"><i class="fa-solid fa-file-lines"></i></a>
  <a class="i-mail" href="mailto:{EMAIL}" title="Email" aria-label="Email"><i class="fa-solid fa-envelope"></i></a>
  <a class="i-gs" href="{LINKS['scholar']}" title="Google Scholar" aria-label="Google Scholar"><i class="fa-solid fa-graduation-cap"></i></a>
  <a class="i-orcid" href="{LINKS['orcid']}" title="ORCID" aria-label="ORCID"><i class="fa-brands fa-orcid"></i></a>
  <a class="i-gh" href="{LINKS['github']}" title="GitHub" aria-label="GitHub"><i class="fa-brands fa-github"></i></a>
  <a class="i-li" href="{LINKS['linkedin']}" title="LinkedIn" aria-label="LinkedIn"><i class="fa-brands fa-linkedin-in"></i></a>
</div>"""


def rows(items):
    out = ['<div class="cv">']
    for when, what in items:
        out.append(f'  <div class="row"><div class="when">{when}</div><div class="what">{what}</div></div>')
    out.append("</div>")
    return "\n".join(out)


# =====================================================================
# PUBLICATIONS DATA
# =====================================================================
ME = "V.D. Trung"

def doi(d):
    return f'<a class="btn" href="https://doi.org/{d}">DOI</a>'

UNDER_REVIEW = [
    ("Multifunctional AgNW/CNT-Based Textile Sensor for Piezoresistive Sensing, Braille Input Recognition, and Electrothermal Heating",
     "X. Han, J. Natsuki, Y. Sun, W. Zhao, V.D. Trung, L. Cui, T. Natsuki"),
    ("Tunable Gas Sensors for Multi-Gas Recognition: Response Manifolds, Generated Selectivity, and Adaptive Operations",
     "H.H. Hau, V.D. Trung, T. Nguyen-Dang, N.D. Hoa, S.S. Park"),
    ("Innovative Advances in Intelligent Droplet Microfluidics: From Machine Vision-Augmented Quantifications to Autonomous Control",
     "V.D. Trung, H. Nguyen-Duc, W. Zhao, N.T. Ha, P.T. Bui, V.N. Quynh, X. Han, Y. Sun, T.N.H. Lo, T. Nguyen-Dang"),
    ("Skin-Inspired Wearable Tactile-Acoustic Sensor for Multimodal Physiological and Auditory Signal Recognition",
     "W. Zhao, V.D. Trung, T. Nguyen-Dang, J. Natsuki, H. Li, W. Yang, X. Wang, T. Natsuki"),
    ("Spray Coating Conjugated Polyelectrolyte Thin Film for Composite Electrochromic Devices",
     "V.N. Quynh, P.T. Bui, N.T. Ha, L.P. Anh, G.C. Bazan, V.D. Trung, T.N.H. Lo, T. Nguyen-Dang"),
]

# (year, title, authors, journal, vol/pages, doi, extra-html)
PUBLISHED = [
    (2026, "Weaving Intelligence: Multimaterial Thermally Drawn Fibers Toward AI-Enabled Smart Textiles",
     "V.D. Trung, J. Yi, H. Nguyen-Duc, T.N.H. Lo, W. Zhao, C. Dong, F. Sorin, B. Caglar, L. Wei, T. Nguyen-Dang",
     "Adv. Mater.", "<b>38</b>, e73574", "10.1002/adma.73574",
     '<a class="btn flag-feat" href="https://vinuni.edu.vn/breakthrough-research-from-vinuniversity-featured-in-the-worlds-top-materials-science-journal-advanced-materials/">In the news</a>'),
    (2026, "Percolation-Tuned Mesostructured Capacitive Sensor for Physiological Signal Detection and Acoustic Recognition",
     "W. Zhao, V.D. Trung, Y. Zhang, X. Hong, K. Chen, J. Natsuki, L. Cui, T. Natsuki",
     "Chem. Eng. J.", "<b>545</b>, 179945", "10.1016/j.cej.2026.179945", ""),
    (2026, "Skin-Inspired Controllable Microcrack Electronic Skin with High Signal-to-Noise Ratio for High-Fidelity Pulse Wave Monitoring",
     "W. Zhao, V.D. Trung, Y. Zhang, X. Su, X. Hong, L. Cui, X. Liu",
     "Adv. Fiber Mater.", "", "10.1007/s42765-026-00763-6", ""),
    (2026, "Sewn Textile Strain Sensors: Impact of Contact-Regulating Stitch Parameters on Strain Sensing Performance",
     "X. Han, J. Natsuki, Y. Sun, V.D. Trung, T. Natsuki",
     "J. Text. Inst.", "1&ndash;12", "10.1080/00405000.2026.2712796", ""),
    (2026, "From Battery Recycling to Ion-Transport-Triggered Hydrovoltaic Capacitor Employing Graphene Nanosheet Anode Prepared via One-Step Cathodic Plasma Exfoliation",
     "P.-A. Le, V.D. Trung, W. Zhao, T. Nguyen-Dang, X.V. Nguyen, X. Han, J. Natsuki, N.T. Tung, T. Natsuki",
     "Chem. Eng. J.", "<b>529</b>, 172769", "10.1016/j.cej.2026.172769", ""),
    (2025, "Arterial Pulse Dynamics Monitoring via Ultrasensitive Sandwich Soft Electronics",
     "W. Zhao, V.D. Trung, J. Natsuki, J. Tan, W. Yang, T. Natsuki",
     "Adv. Fiber Mater.", "<b>7</b>, 1615&ndash;1631", "10.1007/s42765-025-00575-0", ""),
    (2025, "Hierarchical Synergistic Engineering for Machine Learning-Assisted Gesture Recognition and Integrated Thermal Management",
     "W. Zhao, V.D. Trung, F. Li, Y. Zhang, H. Li, J. Natsuki, J. Tan, W. Yang, T. Natsuki",
     "Adv. Fiber Mater.", "<b>7</b>, 1495&ndash;1513", "10.1007/s42765-025-00565-2", ""),
    (2025, "Empirical Modeling of Seasonal Cooling Performance Based on Test Devices Using Zinc Oxide/Low-Density Polyethylene Passive Cooling Membranes",
     "Y. Zhang, J. Natsuki, C. Weng, V.D. Trung, Y. Wang, L. Cui, T. Natsuki",
     "Polymers", "<b>17</b>, 1420", "10.3390/polym17101420", ""),
    (2025, "Synergistic Interfacial Engineering for Ultrasensitive Bionic Tunable Strain Sensors with Robust Sensing Stability and Integrated Thermal Management",
     "V.D. Trung, W. Zhao, J. Natsuki, J. Tan, W. Yang, T. Natsuki",
     "Chem. Eng. J.", "<b>508</b>, 161056", "10.1016/j.cej.2025.161056", ""),
    (2025, "Iontronic Dual Pressure-Humidity Sensor Based on Poly(Vinyl Alcohol)/Phosphoric Acid/Ni-Al Layered Double Hydroxide Hydrogel@Melamine Sponge for Advanced Wearable Electronics",
     "V.D. Trung, W. Zhao, P.-A. Le, Y. Zhang, Y. Sun, J. Natsuki, J. Tan, W. Yang, T. Natsuki",
     "Mater. Res. Bull.", "<b>186</b>, 113357", "10.1016/j.materresbull.2025.113357", ""),
    (2025, "Textile-Based Interdigitated Electrode Piezoresistive Sensor: Materials, Fabrication and Applications &ndash; A Review",
     "W. Zhao, V.D. Trung, X. Hong, Y. Sun, Y. Zhang, J. Natsuki, J. Tan, W. Yang, T. Natsuki",
     "J. Alloys Compd.", "<b>1014</b>, 178764", "10.1016/j.jallcom.2025.178764", ""),
    (2024, "Hydrovoltaic&ndash;Piezoelectric Hybridized Device for Microdroplet-Pressure Dual Energy Harvesting and Piezo Sensing",
     "V.D. Trung, P.-A. Le, J. Natsuki, W. Zhao, T.V.B. Phung, J. Tan, W. Yang, T. Natsuki",
     "Chem. Eng. J.", "<b>496</b>, 154164", "10.1016/j.cej.2024.154164", ""),
    (2024, "AgNPs/CNTs Modified Nonwoven Fabric for PET-Based Flexible Interdigitated Electrodes in Pressure Sensor Applications",
     "W. Zhao, J. Natsuki, V.D. Trung, H. Li, J. Tan, W. Yang, T. Natsuki",
     "Chem. Eng. J.", "<b>499</b>, 156252", "10.1016/j.cej.2024.156252", ""),
    (2024, "Enhanced Functionalization of Nonwoven Fabric by Spray Coating AgNPs/CNTs Solution Prepared by a One-Step Method",
     "W. Zhao, V.D. Trung, H. Li, J. Natsuki, J. Tan, W. Yang, T. Natsuki",
     "Chem. Eng. J.", "<b>494</b>, 153101", "10.1016/j.cej.2024.153101", ""),
    (2024, "Recent Developments in Droplet-Based Devices",
     "V.D. Trung, P.-A. Le, J. Natsuki, W. Zhao, T.V.B. Phung, T. Natsuki",
     "Mater. Today Chem.", "<b>36</b>, 101943", "10.1016/j.mtchem.2024.101943", ""),
    (2024, "An Aluminum-Air Battery/Hydrocapacitor-Inspired Hybrid Device for Energy Conversion from Micro Water Droplets",
     "V.D. Trung, J. Natsuki, L. Cui, P.-A. Le, T. Natsuki",
     "Chem. Eng. J.", "<b>480</b>, 148125", "10.1016/j.cej.2023.148125", ""),
    (2023, "Compact Electrolytic Hydrocapacitor for Direct Harvesting and Storing Energy from Water Droplet Achieving High Voltage",
     "V.D. Trung, P.-A. Le, J. Natsuki, T. Natsuki",
     "Adv. Mater. Technol.", "<b>8</b>, 2300638", "10.1002/admt.202300638", ""),
    (2023, "Overview of the Thermal Runaway in Lithium-Ion Batteries with Application in Electric Vehicles: Working Principles, Early Warning, and Future Outlooks",
     "P.-A. Le, V.D. Trung, J. Natsuki, T. Natsuki",
     "Energy Fuels", "<b>37</b>, 17052&ndash;17074", "10.1021/acs.energyfuels.3c02548", ""),
    (2023, "The Current Status of Hydrogen Energy: An Overview",
     "P.-A. Le, V.D. Trung, P.L. Nguyen, T.V.B. Phung, J. Natsuki, T. Natsuki",
     "RSC Adv.", "<b>13</b>, 28262&ndash;28287", "10.1039/d3ra05158g",
     '<span class="btn flag-feat" title="Clarivate Essential Science Indicators">Highly Cited Paper (Clarivate)</span>'),
    (2022, "A Moisture-Induced Electric Generator with High Output Voltage for Self-Powered Wearable Electronics",
     "V.D. Trung, S. Chen, H. Xia, T. Natsuki, Q. Ni",
     "ChemNanoMat", "<b>8</b>, e202200395", "10.1002/cnma.202200395",
     '<a class="btn flag-feat" href="top-downloaded.jpg">Top Downloaded Article</a>'),
]
N_PUB = len(PUBLISHED)
N_FIRST = sum(1 for p in PUBLISHED if p[2].startswith(ME))
assert N_PUB == 20 and N_FIRST == 8, (N_PUB, N_FIRST)

# Articles found on ORCID that are not curated above (added automatically)
EXTRA = [w for w in AUTO.get("extra_works", []) if w.get("year")]
N_ART = N_PUB + len(EXTRA)
MET = AUTO.get("metrics") or {}
PEER = AUTO.get("peer_reviews") or 45
MET_SRC = MET.get("source", "Google Scholar")
MET_URL = LINKS["scholar"] if MET_SRC == "Google Scholar" else "https://openalex.org/"


def authors(s):
    return html.escape(s).replace(ME, f"<b>{ME}</b>")


# =====================================================================
# ABOUT (index.html)
# =====================================================================
about = f"""
<section class="intro">
  <div>
    <h1>Vuong Dinh Trung</h1>
    <p class="lead">Postdoctoral Research Fellow &amp; Instructor &middot; VinUniversity, Hanoi</p>
    <p>I go by <b>Trung</b>. I am a postdoctoral research fellow and instructor at the <a href="{LINKS['cmit']}">Center for Materials Innovation and Technology (CMIT)</a>
    and the <a href="{LINKS['cecs']}">College of Engineering and Computer Science</a>, <a href="https://vinuni.edu.vn/">VinUniversity</a>, Vietnam, where I work
    on smart fibers.</p>
    <p>I received my D.Eng. (2025) and M.Eng. (2022) in Smart Materials Science and Technology from
    <a href="https://www.shinshu-u.ac.jp/english/">Shinshu University</a>, Japan, advised by Prof. Toshiaki Natsuki and
    Prof. Qing-Qing Ni, and my B.Eng. in Mechanical Engineering from HCMC University of Technology and Engineering.</p>
    <p>My research is about <b>fibers that sense</b>: multimaterial fibers, textile and skin-inspired wearable sensors,
    droplet microfluidics and hydrovoltaic energy harvesting, and increasingly, pairing these fiber systems with
    machine learning so that a textile can recognize gestures, physiological signals and sound.</p>
    <p>I also bring an industry background, as an external designer for the <a href="https://www.lego.com/en-us/aboutus/lego-group">LEGO Group</a> and three years as a corporate
    leadership trainee at a Japanese molding factory, so I am as comfortable at a CNC machine or a 3D printer as at the lab bench.</p>
    {icons()}
  </div>
  <div class="side">
    <img class="photo" src="profile.jpg" alt="Portrait of Vuong Dinh Trung"
         onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">
    <div class="monogram" aria-hidden="true">VDT</div>
  </div>
</section>

<section class="stats">
  <div class="stat"><span class="n">{N_ART}</span><span class="l">high-impact journal articles</span></div>
  <div class="stat"><span class="n">{MET.get("citations", "&ndash;")}</span><span class="l">citations</span></div>
  <div class="stat"><span class="n">{MET.get("h_index", "&ndash;")}</span><span class="l">h-index</span></div>
  <div class="stat"><span class="n">4</span><span class="l">grants contributed to (Co-PI / member) &middot; total USD 457K</span></div>
  <div class="stat"><span class="n">1</span><span class="l">patent</span></div>
  <div class="stat"><span class="n">{PEER}</span><span class="l">peer reviews for leading journals</span></div>
</section>

<h2>Research Interests</h2>
<div class="grid2">
  <div class="card ri"><img src="ri-fibers.svg" alt="Illustration of a multifunctional fiber and its cross-section" loading="lazy"><div class="cb"><h4>Smart fibers</h4>
    <p>Multifunctional fibers that integrate electrodes, semiconductors and microchannels along their length, for distributed sensing, fiber transistors and lab-on-fiber photonics.</p></div></div>
  <div class="card ri"><img src="ri-wearable.svg" alt="Illustration of a textile sensor band on the wrist reading a pulse wave" loading="lazy"><div class="cb"><h4>Textile &amp; skin-inspired wearable sensors</h4>
    <p>Piezoresistive, capacitive and iontronic sensors on fabrics, nonwovens and sponges for pulse-wave, strain, pressure and humidity monitoring.</p></div></div>
  <div class="card ri"><img src="ri-ai.svg" alt="Illustration of a sensing textile feeding a neural network" loading="lazy"><div class="cb"><h4>AI-enabled smart textiles</h4>
    <p>Machine learning for gesture, physiological-signal and acoustic recognition, and AI-assisted design of fiber devices.</p></div></div>
  <div class="card ri"><img src="ri-droplet.svg" alt="Illustration of droplet microfluidics and droplet energy harvesting" loading="lazy"><div class="cb"><h4>Droplet microfluidics &amp; hydrovoltaic energy</h4>
    <p>Harvesting and storing energy from water droplets and moisture; intelligent droplet microfluidics with machine-vision control.</p></div></div>
</div>

<h2>Education</h2>
{rows([
    ("2022 &ndash; 2025", '<b>D.Eng.</b> in Smart Materials Science and Technology<span class="sub">Shinshu University, Japan &middot; Advisor: Prof. Toshiaki Natsuki</span>'),
    ("2020 &ndash; 2022", '<b>M.Eng.</b> in Smart Materials Science and Technology<span class="sub">Shinshu University, Japan &middot; Advisor: Prof. Qing-Qing Ni</span>'),
    ("2014 &ndash; 2018", '<b>B.Eng.</b> in Mechanical Engineering<span class="sub">HCMC University of Technology and Engineering, Vietnam</span>'),
])}

<h2>Positions</h2>
{rows([
    ("2025 &ndash;", '<b>Postdoctoral Research Fellow &amp; Instructor</b><span class="sub"><a href="https://cecs.vinuni.edu.vn/">College of Engineering &amp; Computer Science</a> and <a href="https://cmit.vinuni.edu.vn/">CMIT</a>, VinUniversity, Vietnam</span>'),
    ("2026 &ndash;", '<b>Technical Advisor</b><span class="sub"><a href="https://eyhcnc.com/">EYH Industrial Joint Stock Company</a> and <a href="https://www.facebook.com/profile.php?id=61585326377855">Basement LAB</a>, Vietnam</span>'),
    ("2022 &ndash; 2025", '<b>Research Assistant</b><span class="sub"><a href="https://www.shinshu-u.ac.jp/faculty/textiles/english/">Faculty of Textile Science and Technology</a>, Shinshu University, Japan</span>'),
    ("2024", '<b>Contract Researcher</b><span class="sub"><a href="https://cei.vinuni.edu.vn/">Center for Environmental Intelligence</a>, VinUniversity, Vietnam</span>'),
    ("2019 &ndash; 2022", '<b>Corporate Leadership Trainee</b><span class="sub"><a href="https://www.yuwa-net.co.jp/">Yuwa Co., Ltd.</a>, Head Office Molding Factory, Japan</span>'),
    ("2018 &ndash; 2019", '<b>External Designer</b><span class="sub"><a href="https://www.lego.com/en-us/aboutus/lego-group">LEGO Group</a> (via <a href="http://www.vmr.vn/">VMR Co., Ltd.</a>), Vietnam</span>'),
])}

<h2>Grants &amp; Projects</h2>
{rows([
    ("2026 &ndash; 2027", '<b>Co-PI:</b> Microsphere Lasers Enabled by Microdroplet Microfluidic Devices Fabricated via Thermally Drawn Fibers<span class="sub">CMIT Grant Program AY25-26 (VINUNI.2526.CMIT.06), VinUniversity &middot; USD 20,000</span>'),
    ("2026 &ndash; 2029", '<b>Senior Member:</b> Developing Lab-on-Fiber Photonic Devices Based on Integration of High-Quality Microlasers with Multistructured Fibers<span class="sub">Vingroup Innovation Foundation (VINIF.2026.DA003) &middot; USD 115,000</span>'),
    ("2026 &ndash; 2028", '<b>Member:</b> Metal Electrode Integration Methods in Smart Fiber Structures for Organic Semiconductor Devices and Energy Storage<span class="sub">NAFOSTED (103.02-2025.81) &middot; USD 72,000</span>'),
    ("2023 &ndash; 2027", '<b>Member:</b> AI for Materials Discovery<span class="sub">ENVISION Flagship Grant (VUNI.CEI.FS_0007), VinUniversity &middot; USD 250,000</span>'),
])}

<h2>Teaching</h2>
{rows([
    ("Fall 2026", '<b>MECE3070 &ndash; Mechanics of Engineering Materials</b>, Teaching Assistant<span class="sub">VinUniversity</span>'),
    ("Summer 2026", '<b>Scientific Research Talent Camp: Smart Sensing Materials</b>, Instructor<span class="sub">Vingroup Innovation Foundation (VinIF)</span>'),
    ("Summer 2026", '<b>UROP1010 &ndash; Undergraduate Research Opportunities Program 1</b>, Teaching Assistant<span class="sub">VinUniversity</span>'),
    ("Spring 2026", '<b>MECE4120 &ndash; Sensors and Actuators</b>, Teaching Assistant<span class="sub">VinUniversity</span>'),
])}

<h2>Skills</h2>
{rows([
    ("Characterization", "XRD, Raman, XPS, SEM, TEM, FTIR, BET, tensile testing; electrochemical and electrical measurements (V&ndash;I&ndash;R, CV, LSV, EIS, GCD)"),
    ("Design &amp; code", "SolidWorks, Siemens NX, AutoCAD, COMSOL, Python, Arduino IDE, Origin, ChemDraw"),
    ("Manufacturing", "Semi-automated and CNC machining, 3D printing (additive manufacturing), thermal drawing"),
    ("Languages", "Vietnamese, English, Japanese"),
])}

<p class="small" style="margin-top:28px">Full publication list on the <a href="publications.html">publications</a> page &middot;
service and editorial work on the <a href="outreach.html">outreach</a> page.</p>
"""

# =====================================================================
# TEAM
# =====================================================================
def person(initials, name, aff, meta, tags, cls="", photo=None):
    t = "".join(f'<span class="tag">{x}</span>' for x in tags)
    m = f'\n      <p class="meta">{meta}</p>' if meta else ""
    av = (f'<img class="avatar" src="{photo}" alt="{name}">' if photo
          else f'<div class="avatar {cls}">{initials}</div>')
    return f"""  <div class="person">
    {av}
    <div>
      <h4>{name}</h4>
      <div class="aff">{aff}</div>
      <div>{t}</div>{m}
    </div>
  </div>"""

team = f"""
<h1>Team</h1>
<p class="lead">I do not run a lab yet. Below are the colleagues I work with most closely, with whom I have grown shared
ideas into research with real impact, followed by my collaborators.</p>

<h2>Close colleagues</h2>
<div class="people">
{person("WZ", "Weili Zhao", "State Key Laboratory of Bio-based Fiber Materials, Zhejiang Sci-Tech University, China &middot; formerly Shinshu University, Japan",
        "Textile pressure and strain sensors, electronic skin, pulse-wave monitoring.", ["13 joint papers"], photo="weili-zhao.jpg")}
{person("TL", "Tien Nu Hoang Lo", "Center for Materials Innovation and Technology and College of Engineering and Computer Science, VinUniversity, Vietnam",
        "Multimaterial fibers, droplet microfluidics, organic electronics.", ["1 joint paper"], "warm")}
{person("YZ", "Yinjia Zhang", "College of Textiles and Apparel, Quanzhou Normal University, China &middot; formerly Shinshu University, Japan",
        "Passive radiative-cooling membranes and wearable sensors.", ["6 joint papers"], "alt")}
{person("YS", "Yanyan Sun", "School of Textile and Garment, Anhui Polytechnic University, China &middot; formerly a student at Shinshu University, Japan",
        "Textile and sewn strain sensors.", ["3 joint papers"], "alt")}
{person("XH", "Xiaoyu Han", "College of Textiles and Apparel, Quanzhou Normal University, China &middot; formerly a student at Shinshu University, Japan",
        "Sewn textile sensors, Braille input recognition, electrothermal heating.", ["2 joint papers"])}
{person("NH", "Nam-Tien Ha", "IntOr Lab, VinUniversity, Vietnam",
        "Fiber-based wearable textile biosensors.", ["1 joint presentation"], "warm")}
{person("SC", "Si Chen", "Key Laboratory of Clothing Materials of Universities in Fujian, Quanzhou Normal University, China &middot; formerly Shinshu University, Japan",
        "Moisture-induced electric generators for self-powered wearables.", ["1 joint paper"])}
{person("VN", "Van Nhat Nguyen", "Department of Materials Science and Engineering, National Tsing Hua University, Taiwan",
        "", [], "alt")}
</div>

@@COLLAB@@
"""

# =====================================================================
# COLLABORATORS
# =====================================================================
FLAGS = {
 "vn": '<svg class="flag" viewBox="0 0 30 20" aria-hidden="true"><rect width="30" height="20" fill="#da251d"/><polygon points="15,4 16.5,8.5 21.2,8.5 17.4,11.3 18.8,15.8 15,13 11.2,15.8 12.6,11.3 8.8,8.5 13.5,8.5" fill="#ffff00"/></svg>',
 "jp": '<svg class="flag" viewBox="0 0 30 20" aria-hidden="true"><rect width="30" height="20" fill="#fff" stroke="#ccc"/><circle cx="15" cy="10" r="6" fill="#bc002d"/></svg>',
 "cn": '<svg class="flag" viewBox="0 0 30 20" aria-hidden="true"><rect width="30" height="20" fill="#de2910"/><polygon points="6,3 7.2,6.6 11,6.6 7.9,8.8 9.1,12.4 6,10.2 2.9,12.4 4.1,8.8 1,6.6 4.8,6.6" fill="#ffde00"/></svg>',
 "sg": '<svg class="flag" viewBox="0 0 30 20" aria-hidden="true"><rect width="30" height="10" fill="#ef3340"/><rect y="10" width="30" height="10" fill="#fff"/><circle cx="7" cy="5" r="3.2" fill="#fff"/><circle cx="8.2" cy="5" r="3" fill="#ef3340"/></svg>',
}

def collab(initials, name, aff, tags, cls="", title="", roles=""):
    head = f'<b class="ttl">{title}</b><br>' if title else ""
    return person(initials, name, head + aff, roles, tags, cls)

def joint(n, kind="paper"):
    return f"{n} joint {kind}{'s' if n > 1 else ''}"

def country(code, label, cards):
    return f'<h3 class="country">{FLAGS[code]} {label}</h3>\n<div class="people">\n' + "\n".join(cards) + "\n</div>"

BUCT = "College of Mechanical and Electrical Engineering, Beijing University of Chemical Technology"
collaborators = '\n<h2 id="collaborators">Collaborators</h2>\n\n' + "\n\n".join([
    country("vn", "Vietnam", [
        collab("TN", "Tung Nguyen-Dang", "College of Engineering and Computer Science, VinUniversity",
               ["Postdoctoral supervisor", joint(2)], "warm", title="Assistant Professor",
               roles="Director of Career and Industry Relations; Head of IntOr Lab."),
        collab("TD", "Ta Van Duong", "Department of Optical Equipment, Faculty of Weapons, Le Quy Don Technical University (Military Technical Academy), Hanoi",
               ["Lab-on-Fiber project, VINIF"], "warm", title="Associate Professor",
               roles="Senior Lieutenant Colonel, Vietnam People&rsquo;s Army."),
    ]),
    country("jp", "Japan", [
        collab("TN", "Toshiaki Natsuki", "Shinshu University",
               ["D.Eng. advisor", joint(18)], title="Professor",
               roles="Head of the Division of Textile Production and Manufacturing Technology, Institute for Fiber Engineering and Science (IFES); Professor in the Faculty of Textile Science and Technology, Division of Machinery and Robotics."),
        collab("JN", "Jun Natsuki", "Institute for Fiber Engineering and Science (IFES), Shinshu University",
               [joint(17)], title="Specially Appointed Professor"),
        collab("QN", "Qing-Qing Ni", "Zhejiang Sci-Tech University, China &middot; Shinshu University, Japan",
               ["M.Eng. advisor", joint(1)], title="Distinguished Professor; Professor Emeritus, Shinshu University",
               roles="Deputy Director of the Zhejiang Provincial Innovation Center of Advanced Textile Technology; former Head of the Department of Mechanical and Robotics Engineering, Shinshu University."),
        collab("HX", "Hong Xia", "Shinshu University",
               [joint(1)], title="Researcher"),
    ]),
    country("cn", "China", [
        collab("WY", "Weimin Yang", BUCT,
               [joint(8)], "alt", title="Distinguished Professor",
               roles="Dean of the College of Mechanical and Electrical Engineering; Chair of the Expert Committee of the China Plastics Processing Industry Association; Chair of the Injection Molding Division of the Society of Plastics Engineers; Deputy Director of the National Engineering Laboratory for Tire Design and Manufacturing."),
        collab("JT", "Jing Tan", BUCT,
               [joint(8)], "alt", title="Professor",
               roles="Secretary of the Mechanical Engineering and Automation Party Branch."),
        collab("HL", "Haoyi Li", BUCT,
               [joint(3)], "alt", title="Associate Professor",
               roles="Deputy Director of the Department of Mechanical Engineering."),
        collab("XL", "Xiangyang Liu", "Xiamen University &middot; Quanzhou Normal University",
               [joint(1)], "alt", title="Nanqiang Distinguished Professor",
               roles="Ministry of Education Changjiang Scholar Chair Professor; National Overseas High-Level Talent Specially Appointed Professor."),
        collab("LC", "Lina Cui", "College of Textiles and Apparel, Quanzhou Normal University",
               [joint(4)], "alt", title="Professor",
               roles="Vice Dean; Chair of the College Professors&rsquo; Committee; Deputy Secretary-General of the Fujian Textile Engineering Society."),
        collab("XH", "Xinghua Hong", "State Key Laboratory of Bio-based Fiber Materials, Zhejiang Sci-Tech University",
               [joint(3)], "alt"),
        collab("HW", "Hao Wang", "Department of Textile and Garment, Anhui Vocational and Technical College, Hefei",
               [], "alt"),
        collab("FL", "Fang Li", "Zhongyuan University of Technology, Zhengzhou",
               [joint(1)], "alt"),
        collab("KC", "Kun Chen", "Zhejiang Sci-Tech University, Hangzhou",
               [joint(1)], "alt"),
        collab("XS", "Xiuping Su", "College of Textile, Apparel and Art Design, Shaoxing Institute of Technology",
               [joint(1)], "alt"),
        collab("YW", "Yiwen Wang", "College of Textile and Clothing, Xinjiang University",
               [joint(1)], "alt"),
    ]),
]) + "\n"
team = team.replace("@@COLLAB@@", collaborators)

# =====================================================================
# PUBLICATIONS
# =====================================================================
def pub_list(items, start):
    out = [f'<ol class="pubs" style="--start:{start}">']
    for it in items:
        out.append(it)
    out.append("</ol>")
    return "\n".join(out)

ur_items = [f'<li><span class="pt">{html.escape(t)}</span><span class="pa">{authors(a)}</span><span class="pv"><i>Under review</i> (2026)</span></li>'
            for t, a in UNDER_REVIEW]

# Journal metrics from the latest editions available in the submission year:
# doi -> (submitted year, JCR IF, JCR year, Scopus CiteScore highest-percentile "top %", CiteScore year)
METRICS = {
 "10.1002/adma.73574":               (2026, "29.1", 2025, 1, 2025),
 "10.1016/j.cej.2026.179945":        (2026, "12.5", 2025, 4, 2025),
 "10.1007/s42765-026-00763-6":       (2026, "22.6", 2025, 1, 2025),
 "10.1080/00405000.2026.2712796":    (2026, "1.6", 2025, 25, 2025),
 "10.1016/j.cej.2026.172769":        (2025, "13.2", 2024, 3, 2024),
 "10.1007/s42765-025-00575-0":       (2025, "21.3", 2024, 2, 2024),
 "10.1007/s42765-025-00565-2":       (2025, "21.3", 2024, 2, 2024),
 "10.3390/polym17101420":            (2025, "4.9", 2024, 15, 2024),
 "10.1016/j.cej.2025.161056":        (2025, "13.2", 2024, 3, 2024),
 "10.1016/j.materresbull.2025.113357": (2024, "5.3", 2023, 8, 2023),
 "10.1016/j.jallcom.2025.178764":    (2024, "5.8", 2023, 6, 2023),
 "10.1016/j.cej.2024.154164":        (2024, "13.3", 2023, 2, 2023),
 "10.1016/j.cej.2024.156252":        (2024, "13.3", 2023, 2, 2023),
 "10.1016/j.cej.2024.153101":        (2024, "13.3", 2023, 2, 2023),
 "10.1016/j.mtchem.2024.101943":     (2023, "7.3", 2022, 17, 2022),
 "10.1016/j.cej.2023.148125":        (2023, "15.1", 2022, 1, 2022),
 "10.1002/admt.202300638":           (2023, "6.8", 2022, 5, 2022),
 "10.1021/acs.energyfuels.3c02548":  (2023, "5.3", 2022, 16, 2022),
 "10.1039/d3ra05158g":               (2023, "3.9", 2022, 22, 2022),
 "10.1002/cnma.202200395":           (2022, "3.82", 2021, 21, 2021),
}
assert set(METRICS) == {p[5] for p in PUBLISHED}

def metric_line(d):
    sub, jif, jy, top, cy = METRICS[d]
    return (f'<span class="metrics"><span class="metric if" title="Journal Impact Factor, JCR {jy}">IF {jif}</span>'
            f'<span class="metric sc" title="Scopus CiteScore {cy}, highest category percentile">Top {top}% Scopus</span>'
            f'<span class="mnote">{jy} metrics &middot; submitted {sub}</span></span>')

TOPDL = ('<figure class="cert"><a href="top-downloaded.jpg"><img src="top-downloaded.jpg" alt="Wiley Top Downloaded Article certificate for ChemNanoMat"></a>'
         '<figcaption>Wiley Top Downloaded Article, <i>ChemNanoMat</i> (published in 2022)</figcaption></figure>')

def extra_item(w):
    vol = f", <b>{html.escape(str(w['volume']))}</b>" if w.get("volume") else ""
    pg = f", {html.escape(str(w['pages']))}" if w.get("pages") else ""
    au = f'<span class="pa">{authors(w["authors"])}</span>' if w.get("authors") else ""
    return (f'<li><span class="pt">{html.escape(w["title"])}</span>{au}'
            f'<span class="pv"><i>{html.escape(w.get("journal") or "")}</i>{vol}{pg} ({w["year"]}). {doi(w["doi"])}</span></li>')

years = sorted({p[0] for p in PUBLISHED} | {w["year"] for w in EXTRA}, reverse=True)
pub_sections = []
counter = 0
for y in years:
    items = [extra_item(w) for w in EXTRA if w["year"] == y]
    for (yy, t, a, j, vp, d, extra) in PUBLISHED:
        if yy != y:
            continue
        vp_s = f", {vp}" if vp else ""
        cert = TOPDL if d == "10.1002/cnma.202200395" else ""
        items.append(f'<li><span class="pt">{t}</span><span class="pa">{authors(a)}</span>'
                     f'<span class="pv"><i>{j}</i>{vp_s} ({yy}). {doi(d)}{extra}</span>{metric_line(d)}{cert}</li>')
    pub_sections.append(f"<h3>{y}</h3>\n" + pub_list(items, counter))
    counter += len(items)

publications = f"""
<h1>Publications</h1>

<h2>Journal articles</h2>
<p class="small">IF: Journal Impact Factor (Clarivate JCR). Top %: Scopus CiteScore highest category percentile. Both from the latest editions available in the year each manuscript was submitted.</p>
{''.join(pub_sections)}

<h2>Book chapter</h2>
<ol class="pubs"><li><span class="pt">Artificial Intelligence in Thermally Drawn Multimaterial Fibers: From Distributed Sensing to Neuromorphic Smart Textiles</span>
<span class="pa"><b>V.D. Trung</b>, T. Nguyen-Dang</span><span class="pv">In <i>Applied Intelligence</i>, IntechOpen (ISSN 2633-1403).</span></li></ol>

<h2>Patent</h2>
<ol class="pubs">
<li><span class="pt">Aircraft Protective Frame (<i lang="vi">Khung bảo vệ thiết bị bay</i>)</span><span class="pa">L.D. Dung, N.T. Phong, N.D. Hieu, <b>V.D. Trung</b>, N.D. Tung, A. Hajjar</span>
<span class="pv">Vietnamese Industrial Design Application No. 3-2026-00893, filed 20 Apr 2026, published 15 Jul 2026 (Publication No. 58035). Applicant: VinUniversity. <a class="btn" href="https://wipopublish.ipvietnam.gov.vn/wopublish-search/public/designs?lang=en&amp;query=%223-2026-00893%22">IP Viet Nam record</a></span></li>
</ol>

<h2>Conference presentations</h2>
{rows([
    ("2026", '<b>From Battery Waste to Self-Charging Energy Storage: A Sustainable Hydrovoltaic Capacitor Based on Plasma-Exfoliated Graphene Nanosheets</b><span class="sub"><b>V.D. Trung</b>, L.N.H. Tien &middot; Vietnam Association of Catalysis and Adsorption (VNACA XIII), Hue, Vietnam</span>'),
    ("2026", '<b>Fiber-Based Wearable Textile Biosensors for Early Diagnostic Applications</b><span class="sub">H.N. Tien, L.N.H. Tien, <b>V.D. Trung</b>, N.D. Tung &middot; 3rd International Conference on Microbiology and One Health, Quy Nhon, Vietnam</span>'),
    ("2026", '<b>A Skin-Inspired Electronic Skin with Tunable MXene Microcracks and High Signal-to-Noise Ratio for High-Fidelity Arterial Pulse Monitoring</b><span class="sub">W. Zhao, <b>V.D. Trung</b> &middot; 3rd International Conference on Microbiology and One Health, Quy Nhon, Vietnam</span>'),
    ("2023", '<b>Al-Air Battery-Inspired Hydrocapacitor for Energy Conversion from Micro Water Droplets Achieving High Output</b><span class="sub"><b>V.D. Trung</b>, J. Natsuki, P.-A. Le, T. Natsuki &middot; 4th International Workshop on Advanced Materials and Devices, Thai Nguyen, Vietnam</span>'),
])}
"""

# =====================================================================
# OUTREACH
# =====================================================================
outreach = f"""
<h1>Outreach &amp; Service</h1>
<p class="lead">Editorial work, peer review, events and course development.</p>

<h2>Editorial &amp; peer review</h2>
{rows([
    ("Guest Editor", '<b>MDPI <i>Polymers</i></b>, Special Issue &ldquo;Advanced Polymer Materials for Electronics and Smart Devices&rdquo;'),
    ("Reviewer", '<span class="sub" style="margin-bottom:6px">Journals listed on <a href="' + LINKS['orcid'] + '">ORCID</a></span><div class="jchips"><span class="jchip"><i>ACS Applied Polymer Materials</i></span><span class="jchip"><i>Advanced Functional Materials</i></span><span class="jchip"><i>Advanced Materials Technologies</i></span><span class="jchip"><i>Applied Physics A</i></span><span class="jchip"><i>Carbon</i></span><span class="jchip"><i>Chemical Engineering Journal</i></span><span class="jchip"><i>Composites Part B: Engineering</i></span><span class="jchip"><i>iScience</i></span><span class="jchip"><i>Journal of Alloys and Compounds</i></span><span class="jchip"><i>Journal of Hazardous Materials Advances</i></span><span class="jchip"><i>Micromachines</i></span><span class="jchip"><i>Nano Energy</i></span><span class="jchip"><i>Nanomaterials</i></span><span class="jchip"><i>RSC Advances</i></span><span class="jchip"><i>Sensors</i></span><span class="jchip"><i>Soft Science</i></span></div>'),
])}

<h2>Service &amp; events</h2>
{rows([
    ("2026", '<b>ICMIT 2026</b>, VinUniversity: Organizer, Session Chair (<i>Biomaterials &amp; Nanotechnology</i>) and Poster Judge'),
    ("2026", '<b>Scientific Research Talent Camp: Smart Sensing Materials</b>, Vingroup Innovation Foundation: Instructor'),
    ("2024", '<b>2nd Viet Nam Symposium on Scientific Computation and Modeling</b>, VinUniversity: On-site Assistant'),
    ("2024", '<b>MOU between CEI (VinUniversity) and IFES (Shinshu University)</b>: Liaison'),
])}

<h2>Curriculum development</h2>
{rows([
    ("2026", '<b>Soft Materials and Flexible Electronics</b><span class="sub">MSc in Materials Science, VinUniversity &middot; Course Developer</span>'),
    ("2026", '<b>Organic Semiconductors</b><span class="sub">MSc in Materials Science, VinUniversity &middot; Course Developer</span>'),
])}

<h2>Professional memberships</h2>
{rows([
    ("2026 &ndash;", 'Member, Institute of Electrical and Electronics Engineers (IEEE)'),
    ("2026 &ndash;", 'Member, Vietnam Physical Society (VPS)'),
])}
"""

# =====================================================================
# NEWS
# =====================================================================
news = f"""
<h1>In the news</h1>
<p class="lead">Media coverage of our research and activities.</p>
{rows([
    ("Sep 2026", '<a href="https://cmit.vinuni.edu.vn/%f0%9f%8c%9f-paper-published-in-advanced-fiber-materials-springer-nature-%f0%9f%8c%9f/"><b>Paper published in <i>Advanced Fiber Materials</i> (Springer Nature)</b></a><span class="sub">CMIT, VinUniversity &middot; on our skin-inspired electronic skin with controllable microcracks for high-fidelity pulse-wave monitoring</span>'),
    ("Sep 2026", '<a href="https://www.youtube.com/watch?v=8tj56NpUAaE"><b>VTV2 S-Tech #74: Multifunctional Fibers with Thermal Drawing Process</b></a><span class="sub">VTV2 television feature (in Vietnamese) &middot; YouTube</span>'),
    ("Jun 2026", '<a href="https://vinuni.edu.vn/icmit-2026-over-100-leading-materials-scientists-convene-at-vinuniversity/"><b>ICMIT 2026: Over 100 leading materials scientists convene at VinUniversity</b></a><span class="sub">VinUniversity News &middot; the conference I helped organize and where I chaired the Biomaterials &amp; Nanotechnology session</span>'),
    ("Jun 2026", '<a href="https://vinuni.edu.vn/breakthrough-research-from-vinuniversity-featured-in-the-worlds-top-materials-science-journal-advanced-materials/"><b>Breakthrough research from VinUniversity featured in the world&rsquo;s top materials science journal <i>Advanced Materials</i></b></a><span class="sub">VinUniversity News &middot; on our review of smart fibers for AI-integrated textiles</span>'),
])}
"""

# =====================================================================
# CONTACT
# =====================================================================
contact = f"""
<h1>Contact</h1>
<p class="lead">I am happy to hear from potential collaborators and students.</p>

<h2>Collaboration</h2>
<p>I welcome collaboration with partners in academia and industry on <b>smart materials</b>, <b>functional polymers and fibers</b>,
<b>wearable sensors and electronics</b>, <b>AI for materials and sensing</b>, and <b>energy harvesting</b>.
On the engineering side, I am also open to projects in <b>mechanical design</b>, <b>CNC machining</b> and <b>3D printing</b>,
from prototypes to small-batch production.</p>
<p>Students interested in smart materials, 3D printing or wearable electronics are welcome to get in touch.</p>

<h2>Industry services</h2>
<p>I serve as Technical Advisor to two engineering companies in Ho Chi Minh City and can act as a technical bridge between you and these companies in the areas below.
You may contact them directly by email or reach out to me first.</p>

<h3><a href="https://eyhcnc.com/">EYH Industrial</a></h3>
<ul class="svc">
  <li>Precision CNC machining of custom parts, jigs and fixtures, from prototypes to small batches</li>
  <li>Procurement of laboratory and manufacturing equipment</li>
  <li>Import and export of chemicals and machinery</li>
</ul>
<p><i class="fa-solid fa-envelope"></i> <a href="mailto:sales@eyhcnc.com">sales@eyhcnc.com</a></p>

<h3><a href="https://www.facebook.com/profile.php?id=61585326377855">Basement LAB</a></h3>
<ul class="svc">
  <li>On-demand 3D printing of prototypes, functional parts and custom models</li>
  <li>Custom 3D design and modeling from your ideas, sketches or drawings</li>
  <li>3D scanning of physical objects for reverse engineering and replication</li>
  <li>Showroom of high-quality 3D-printed models</li>
  <li>Distribution of 3D printers and standard printing filaments</li>
</ul>
<p><i class="fa-solid fa-envelope"></i> <a href="mailto:basementlabvn@gmail.com">basementlabvn@gmail.com</a></p>

<h2>Get in touch</h2>
{rows([
    ("Email", f'<a href="mailto:{EMAIL}">{EMAIL}</a>'),
    ("Address", 'Integrated Organic Materials, Devices, Systems Lab<br>College of Engineering and Computer Science, Building H, VinUniversity<br>Gia Lam, Hanoi, Vietnam'),
])}
<iframe class="map" loading="lazy" title="VinUniversity on Google Maps"
  src="https://www.google.com/maps?q=VinUniversity,+Gia+Lam,+Hanoi&output=embed"></iframe>
"""

PAGES = [
    ("index.html", "Vuong Dinh Trung", about,
     "Vuong Dinh Trung, postdoctoral research fellow and instructor at VinUniversity: smart fibers, wearable sensors and AI-enabled textiles."),
    ("team.html", "Team · Vuong Dinh Trung", team, "Close colleagues and collaborators of Vuong Dinh Trung."),
    ("publications.html", "Publications · Vuong Dinh Trung", publications, "Publications, patents and presentations of Vuong Dinh Trung."),
    ("outreach.html", "Outreach · Vuong Dinh Trung", outreach, "Editorial work, peer review, service and outreach of Vuong Dinh Trung."),
    ("news.html", "News · Vuong Dinh Trung", news, "Media coverage of Vuong Dinh Trung's research."),
    ("contact.html", "Contact · Vuong Dinh Trung", contact, "How to contact Vuong Dinh Trung."),
]
for fname, title, body, desc in PAGES:
    with open(os.path.join(OUT, fname), "w") as f:
        f.write(page(fname, title, body, desc))
    print("wrote", fname)

# favicon: small fiber-node monogram
with open(os.path.join(OUT, "favicon.svg"), "w") as f:
    f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#063542"/>'
            '<path d="M14 18 C30 18 30 46 50 46" fill="none" stroke="#5fe3ee" stroke-width="5" stroke-linecap="round"/>'
            '<circle cx="50" cy="46" r="6" fill="#fff"/><circle cx="14" cy="18" r="6" fill="#ffb35c"/></svg>')
print("wrote favicon.svg")

with open(os.path.join(OUT, "collaborators.html"), "w") as f:
    f.write('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Collaborators · Vuong Dinh Trung</title>'
            '<meta http-equiv="refresh" content="0; url=team.html#collaborators"><link rel="canonical" href="team.html#collaborators"></head>'
            '<body><p>Moved to <a href="team.html#collaborators">team</a>.</p></body></html>')
print("wrote collaborators.html (redirect)")

# sitemap.xml + robots.txt for search engines
SITE_URL = "https://vuongdinhtrung.github.io/"
with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for fname, *_ in PAGES:
        loc = SITE_URL if fname == "index.html" else SITE_URL + fname
        f.write(f"  <url><loc>{loc}</loc></url>\n")
    f.write("</urlset>\n")
with open(os.path.join(OUT, "robots.txt"), "w") as f:
    f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}sitemap.xml\n")
print("wrote sitemap.xml, robots.txt")
