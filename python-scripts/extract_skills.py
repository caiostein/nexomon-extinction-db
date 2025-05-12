import os
import json
from collections import OrderedDict

# Paths
DB_PATH = 'python-scripts/assets/nexomon_extinction_database.json'
IMG_DIR = 'database-frontend/src/assets/downloaded_images'
OUTPUT_PATH = 'python-scripts/assets/skill_database.json'

# Load Nexomon database
with open(DB_PATH, encoding='utf-8') as f:
    nexomon_data = json.load(f)

unique_skills = OrderedDict()

def local_image_path(filename):
    if not filename:
        return None
    local_path = os.path.join(IMG_DIR, filename)
    if os.path.isfile(local_path):
        return f"downloaded_images/{filename}"
    return None

def extract_filename_from_url(url):
    if not url:
        return None
    return os.path.basename(url.split('?')[0])

def find_local_image(skill_name, remote_url=None):
    # Try to use the filename from the remote URL if available
    if remote_url:
        img_name = extract_filename_from_url(remote_url)
        local_img = local_image_path(img_name)
        if local_img:
            return local_img
    # Guess from skill name
    guess_name = skill_name.replace(' ', '_') + '_EX_SkillIcon.png'
    local_img = local_image_path(guess_name)
    if local_img:
        return local_img
    return None

def find_local_type_image(type_entry):
    if isinstance(type_entry, dict):
        type_name = type_entry.get('text', '').replace(' Type', '')
    else:
        type_name = str(type_entry).replace(' Type', '')
    if not type_name:
        return None
    img_name = f"{type_name}_Type_Icon.png"
    return local_image_path(img_name)

def find_local_effect_image(effect_entry):
    if not effect_entry or not isinstance(effect_entry, dict):
        return None
    effect_img_url = effect_entry.get('image')
    if effect_img_url and effect_img_url.startswith('http'):
        filename = extract_filename_from_url(effect_img_url)
        local_img = local_image_path(filename)
        if local_img:
            return local_img
    # Try to guess from effect text
    effect_text = effect_entry.get('text', '')
    if effect_text:
        guess_name = effect_text.split('(')[0].strip().replace(' ', '_') + '_Status_Icon.png'
        local_img = local_image_path(guess_name)
        if local_img:
            return local_img
    return None

for nex in nexomon_data:
    skill_tree = nex.get('Skill Tree', [])
    for skill_entry in skill_tree:
        skill = skill_entry.get('Skill')
        if not skill:
            continue
        # Skill can be a dict with 'text' and 'image'
        if isinstance(skill, dict):
            skill_name = skill.get('text')
            skill_img_url = skill.get('image')
        else:
            skill_name = str(skill)
            skill_img_url = None
        if not skill_name:
            continue
        # Find local skill image
        local_img = find_local_image(skill_name, skill_img_url)
        # Find local type image
        type_entry = skill_entry.get('Type', {})
        local_type_img = find_local_type_image(type_entry)
        # Compose type info
        type_info = {
            'text': type_entry.get('text') if isinstance(type_entry, dict) else str(type_entry),
            'image': local_type_img
        } if type_entry else {}
        # Find local effect image (status icon)
        effect_entry = skill_entry.get('Effect')
        local_effect_img = None
        if effect_entry:
            local_effect_img = find_local_effect_image(effect_entry)
        # Compose effect info
        if effect_entry:
            if isinstance(effect_entry, dict):
                effect_info = dict(effect_entry)
                if local_effect_img:
                    effect_info['image'] = local_effect_img
            else:
                effect_info = effect_entry
        else:
            effect_info = "-"
        # Use skill name as unique key
        if skill_name not in unique_skills:
            skill_info = {
                'Name': skill_name,
                'Image': local_img,
                'Type': type_info,
                'Power': skill_entry.get('Power'),
                'Acc': skill_entry.get('Acc'),
                'STA': skill_entry.get('STA'),
                'Speed': skill_entry.get('Speed'),
                'Crit %': skill_entry.get('Crit %'),
                'Effect': effect_info
            }
            unique_skills[skill_name] = skill_info

# Write to skill_database.json
with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(list(unique_skills.values()), f, ensure_ascii=False, indent=2)

print(f"Extracted {len(unique_skills)} unique skills to skill_database.json (using local images)")