#!/usr/bin/env python3
"""
One-time script to generate comprehensive star name catalog using AI.
This script prompts the AI to provide all common naming conventions
(Bayer, Flamsteed, Traditional) for the 27 Nakshatra primary stars.

Usage:
    python scripts/generate_star_catalog.py

Output:
    star_catalog_ai_generated.json - AI-generated catalog (requires validation)
"""
import sys
import os
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.ai_engine import ai_engine

# List of 27 Nakshatras with known primary stars (for reference)
NAKSHATRAS = [
    ("Ashwini", "Hamal", "Alpha Arietis"),
    ("Bharani", "41 Arietis", "41 Arietis"),
    ("Krittika", "Alcyone", "Eta Tauri"),
    ("Rohini", "Aldebaran", "Alpha Tauri"),
    ("Mrigashira", "Meissa", "Lambda Orionis"),
    ("Ardra", "Betelgeuse", "Alpha Orionis"),
    ("Punarvasu", "Pollux", "Beta Geminorum"),
    ("Pushya", "Delta Cancri", "Delta Cancri"),
    ("Ashlesha", "Alphard", "Alpha Hydrae"),
    ("Magha", "Regulus", "Alpha Leonis"),
    ("Purva Phalguni", "Zosma", "Delta Leonis"),
    ("Uttara Phalguni", "Denebola", "Beta Leonis"),
    ("Hasta", "Algorab", "Delta Corvi"),
    ("Chitra", "Spica", "Alpha Virginis"),
    ("Swati", "Arcturus", "Alpha Bootis"),
    ("Vishakha", "Zubenelgenubi", "Alpha Librae"),
    ("Anuradha", "Dschubba", "Delta Scorpii"),
    ("Jyeshtha", "Antares", "Alpha Scorpii"),
    ("Mula", "Shaula", "Lambda Scorpii"),
    ("Purva Ashadha", "Kaus Media", "Delta Sagittarii"),
    ("Uttara Ashadha", "Nunki", "Sigma Sagittarii"),
    ("Shravana", "Altair", "Alpha Aquilae"),
    ("Dhanishta", "Sualocin", "Alpha Delphini"),
    ("Shatabhisha", "Sadachbia", "Lambda Aquarii"),
    ("Purva Bhadrapada", "Markab", "Alpha Pegasi"),
    ("Uttara Bhadrapada", "Algenib", "Gamma Pegasi"),
    ("Revati", "Zeta Piscium", "Zeta Piscium"),
]

def generate_catalog():
    """Generate comprehensive star name catalog using AI."""
    
    print("🌟 Generating star name catalog using AI...")
    print("=" * 60)
    
    nakshatra_list = [n[0] for n in NAKSHATRAS]
    
    prompt = f"""
You are an astronomical database expert. For each of the 27 Nakshatras (Hindu lunar mansions), 
provide ALL common names for the primary star (Yogathara).

For each Nakshatra, list:
1. Bayer designation (e.g., "Alpha Tauri")
2. Flamsteed number (if exists, e.g., "87 Tauri")
3. Traditional Western name (e.g., "Aldebaran")
4. Sanskrit name (same as Nakshatra name)
5. Any other common aliases (Greek letter notation, catalog numbers)

Format as JSON with this EXACT structure:
{{
    "Ashwini": {{
        "bayer": "Alpha Arietis",
        "flamsteed": "13 Arietis",
        "traditional": "Hamal",
        "sanskrit": "Ashwini",
        "aliases": ["α Ari", "HR 617"]
    }},
    "Bharani": {{
        "bayer": "41 Arietis",
        "flamsteed": "41 Arietis",
        "traditional": "41 Arietis",
        "sanskrit": "Bharani",
        "aliases": []
    }},
    ... (continue for all 27)
}}

Nakshatras to process (in order):
{nakshatra_list}

CRITICAL RULES:
1. Return ONLY valid JSON. No markdown code blocks, no explanations.
2. Use null if a naming convention doesn't exist for a star.
3. Be accurate - cross-reference with astronomical databases.
4. Include Greek letter notation in aliases (e.g., "α Ari", "β Leo").
"""
    
    try:
        print("📡 Calling AI engine...")
        response = ai_engine.engine.generate_insight(prompt, context_instructions="Return only JSON")
        
        # Clean response (remove markdown if AI added it)
        clean_response = response.strip()
        if clean_response.startswith('```'):
            # Extract JSON from markdown code block
            lines = clean_response.split('\n')
            clean_response = '\n'.join(lines[1:-1])
        
        # Validate JSON
        try:
            catalog = json.loads(clean_response)
            print(f"✅ Successfully parsed JSON with {len(catalog)} entries")
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            print("Raw response:")
            print(clean_response)
            return
        
        # Save to file
        output_file = 'star_catalog_ai_generated.json'
        with open(output_file, 'w') as f:
            json.dump(catalog, f, indent=2)
        
        print(f"✅ Star catalog generated: {output_file}")
        print("=" * 60)
        print("⚠️  IMPORTANT: Manually review and validate before using!")
        print("   Cross-reference with: http://simbad.u-strasbg.fr/simbad/")
        print("")
        print("📊 Summary:")
        print(f"   Total Nakshatras: {len(catalog)}")
        
        # Count total aliases
        total_aliases = sum(
            len([catalog[n].get('bayer'), catalog[n].get('flamsteed'), 
                 catalog[n].get('traditional'), catalog[n].get('sanskrit')] + 
                catalog[n].get('aliases', [])) 
            for n in catalog
        )
        print(f"   Total name variants: ~{total_aliases}")
        
    except Exception as e:
        print(f"❌ Error generating catalog: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    generate_catalog()
