import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qualilearn_backend.settings')
django.setup()

from core.models import LearningCategory, LearningTopic

SYLLABUS = {
    "MATHEMATICS": [
        "Algebra", "Indices and Logarithms", "Surds", "Linear Equations & Inequalities", 
        "Quadratic Equations", "Simultaneous Equations", "Variation (Direct, Inverse, Joint)", 
        "Sequence and Series (AP & GP)", "Geometry & Trigonometry", "Angles and Triangles", 
        "Circle Theorems", "Mensuration (2D & 3D shapes)", "Trigonometric Ratios", 
        "Trigonometric Identities", "Bearings & Elevation", "Calculus & Functions", 
        "Functions and Graphs", "Limits (basic)", "Differentiation", 
        "Applications of Differentiation", "Integration (basic)", "Statistics & Probability", 
        "Mean, Median, Mode", "Range & Variance", "Probability", "Data Representation"
    ],
    "PHYSICS": [
        "Mechanics", "Motion (Speed, Velocity, Acceleration)", "Newton’s Laws of Motion", 
        "Work, Energy & Power", "Momentum & Collisions", "Simple Harmonic Motion", 
        "Heat & Thermodynamics", "Temperature & Heat", "Gas Laws", "Thermal Expansion", 
        "Heat Transfer", "Waves & Optics", "Wave Properties", "Sound Waves", 
        "Light (Reflection & Refraction)", "Lenses & Optical Instruments", 
        "Electricity & Magnetism", "Electrostatics", "Current Electricity", "Circuits", 
        "Electromagnetism", "Magnetic Fields", "Modern Physics", "Atomic Structure", 
        "Radioactivity", "Nuclear Energy"
    ],
    "CHEMISTRY": [
        "Physical Chemistry", "Atomic Structure", "Periodic Table", "Chemical Bonding", 
        "States of Matter", "Gas Laws", "Thermochemistry", "Chemical Equilibrium", 
        "Organic Chemistry", "Hydrocarbons (Alkanes, Alkenes, Alkynes)", "Functional Groups", 
        "Isomerism", "Crude Oil & Petrochemicals", "Polymers", "Inorganic Chemistry", 
        "Acids, Bases & Salts", "Metals & Non-metals", "Extraction of Metals", 
        "Water & Air", "Quantitative Chemistry", "Mole Concept", "Stoichiometry", 
        "Volumetric Analysis"
    ],
    "BIOLOGY": [
        "Cell Biology", "Cell Structure & Function", "Cell Division (Mitosis & Meiosis)", 
        "Tissues", "Genetics & Evolution", "Mendelian Genetics", "Variation", "Evolution", 
        "Ecology", "Ecosystem", "Food Chains & Webs", "Nutrient Cycles", "Conservation", 
        "Human & Plant Biology", "Digestive System", "Respiratory System", 
        "Circulatory System", "Nervous System", "Reproduction", "Microbiology", 
        "Microorganisms", "Diseases & Immunity"
    ],
    "ENGLISH": [
        "Grammar", "Parts of Speech", "Tenses", "Concord (Subject-Verb Agreement)", 
        "Active & Passive Voice", "Direct & Indirect Speech", "Comprehension & Vocabulary", 
        "Reading Comprehension", "Lexis & Structure", "Synonyms & Antonyms", "Idioms", 
        "Writing", "Essay Writing (Narrative, Descriptive, Argumentative)", 
        "Letter Writing (Formal & Informal)", "Report Writing", "Oral English (WAEC Focus)", 
        "Vowel & Consonant Sounds", "Stress & Intonation", "Minimal Pairs"
    ],
    "LITERATURE": [
        "Drama", "Poetry", "Prose", "Literary Devices", "Themes & Character Analysis"
    ]
}

ICONS = {
    "MATHEMATICS": "bi-calculator",
    "PHYSICS": "bi-lightning-charge",
    "CHEMISTRY": "bi-flask",
    "BIOLOGY": "bi-dna",
    "ENGLISH": "bi-translate",
    "LITERATURE": "bi-book"
}

def seed():
    print("Seeding syllabus...")
    for cat_name, topics in SYLLABUS.items():
        category, created = LearningCategory.objects.get_or_create(
            name=cat_name.title(),
            defaults={'icon_class': ICONS.get(cat_name, 'bi-book')}
        )
        if created:
            print(f"Created category: {cat_name}")
        
        for i, topic_name in enumerate(topics):
            topic, t_created = LearningTopic.objects.get_or_create(
                category=category,
                name=topic_name,
                defaults={'order': i}
            )
            if t_created:
                print(f"  Added topic: {topic_name}")

if __name__ == "__main__":
    seed()
