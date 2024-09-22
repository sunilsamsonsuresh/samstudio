from api_response import api_response
import re

def get_bounding_box(annotation):
    vertices = annotation['bounding_poly']['vertices']
    return {
        'x_min': min(v['x'] for v in vertices),
        'x_max': max(v['x'] for v in vertices),
        'y_min': min(v['y'] for v in vertices),
        'y_max': max(v['y'] for v in vertices)
    }

def is_below(box1, box2, threshold=5):
    return box1['y_min'] > box2['y_max'] + threshold

def is_right_of(box1, box2, threshold=5):
    return box1['x_min'] > box2['x_max'] + threshold

def is_above(box1, box2, threshold=5):
    return box2['y_max'] < box1['y_min'] - threshold

def extract_name_from_bounding_boxes(text_annotations):
    name_start_box = None
    name_end_box = None
    name_text = []

    for annotation in text_annotations[1:]:
        description = annotation['description']
        box = get_bounding_box(annotation)

        if "NAMEN" in description or "SURNAMES" in description:
            name_start_box = box
        elif "GESCHLECHT" in description or "SEX" in description:
            name_end_box = box
            break

        if name_start_box and is_below(box, name_start_box) and (not name_end_box or is_below(name_end_box, box)):
            name_text.append(description)

    return ' '.join(name_text).strip()

def extract_expiry_date(text_annotations):
    expiry_label_box = None
    for ind, annotation in enumerate(text_annotations[1:]):
        description = annotation['description']
        box = get_bounding_box(annotation)
        if "EXPIRY" in description:
            expiry_label_box = box
            break

    if expiry_label_box:
        candidates = []
        for annotation in text_annotations[ind+1:]:
            box = get_bounding_box(annotation)
            if (is_below(box, expiry_label_box, threshold=2) and 
                re.match(r'\d{1,2}', annotation['description'])):
                candidates.append((box['y_min'], annotation['description']))
        
        if candidates:
            grouped_candidates = {}
            for y, text in candidates:
                key = round(y)
                if key not in grouped_candidates:
                    grouped_candidates[key] = []
                grouped_candidates[key].append(text)
            
            sorted_groups = sorted(grouped_candidates.items())
            expiry_date = ''.join(sorted_groups[0][1]) if sorted_groups else ''
            
            if len(expiry_date) == 8:
                return f"{expiry_date[:2]}.{expiry_date[2:4]}.{expiry_date[4:]}"
    
    return None

def extract_nationality(text_annotations):
    nationality_label_box = None
    for ind, annotation in enumerate(text_annotations[1:]):
        description = annotation['description']
        box = get_bounding_box(annotation)
        if "NATIONALITY" in description:
            nationality_label_box = box
            break

    if nationality_label_box:
        candidates = []
        for annotation in text_annotations[ind+1:]:
            box = get_bounding_box(annotation)
            if (is_below(box, nationality_label_box, threshold=2) and 
                len(annotation['description']) == 3 and
                annotation['description'].isalpha()):
                candidates.append((box['x_min'], box['y_min'], annotation['description']))
        
        if candidates:
            candidates.sort(key=lambda x: (x[1], x[0]))
            return candidates[0][2]
    
    return None

def extract_issue_date(text_annotations):
    issue_label_box = None
    for ind, annotation in enumerate(text_annotations[1:]):
        description = annotation['description']
        box = get_bounding_box(annotation)
        if "ISSUE" in description:
            issue_label_box = box
            break

    if issue_label_box:
        candidates = []
        for annotation in text_annotations[ind+1:]:
            box = get_bounding_box(annotation)
            if (is_below(box, issue_label_box, threshold=2) and 
                re.match(r'\d{1,2}', annotation['description'])):
                candidates.append((box['y_min'], annotation['description']))
        
        if candidates:
            grouped_candidates = {}
            for y, text in candidates:
                key = round(y)
                if key not in grouped_candidates:
                    grouped_candidates[key] = []
                grouped_candidates[key].append(text)
            
            sorted_groups = sorted(grouped_candidates.items())
            issue_date = ''.join(sorted_groups[0][1]) if sorted_groups else ''
            
            if len(issue_date) == 8:
                return f"{issue_date[:2]}.{issue_date[2:4]}.{issue_date[4:]}"
    
    return None

def extract_permit_number(text_annotations):
    namen_box = None
    for ind, annotation in enumerate(text_annotations[1:]):
        if "NAMEN" in annotation['description']:
            namen_box = get_bounding_box(annotation)
            break
    
    if namen_box:
        candidates = []
        for annotation in text_annotations[:ind+1]:
            box = get_bounding_box(annotation)
            if is_above(namen_box, box, threshold=10) and re.match(r'^[A-Z0-9]+$', annotation['description']):
                candidates.append((box['y_min'], annotation['description']))
        
        if candidates:
            candidates.sort(key=lambda x: -x[0])
            return candidates[0][1]
    
    return None

def extract_all_fields(text_annotations):
    return {
        "name": extract_name_from_bounding_boxes(text_annotations),
        "expiry_date": extract_expiry_date(text_annotations),
        "nationality": extract_nationality(text_annotations),
        "issue_date": extract_issue_date(text_annotations),
        "permit_number": extract_permit_number(text_annotations)
    }

extracted_fields = extract_all_fields(api_response)
print("Extracted Fields:", extracted_fields)