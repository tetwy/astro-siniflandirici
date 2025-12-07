import cv2
import numpy as np
import os
import json
import math

def preprocess_image(img_color):
    img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.medianBlur(img_gray, 5)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    img_clahe = clahe.apply(img_blur)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (35, 35))
    img_tophat = cv2.morphologyEx(img_clahe, cv2.MORPH_TOPHAT, kernel)
    return img_tophat, img_gray, img_color

def detect_and_extract_features(img_processed, img_gray, img_color):
    _, img_thresh = cv2.threshold(img_processed, 15, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(img_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    all_object_features = []
    valid_contours = []
    img_debug = img_color.copy()

    for i, cnt in enumerate(contours):
        area = cv2.contourArea(cnt)
        if area < 5: continue

        valid_contours.append(cnt)
        features = {}
        features['object_id'] = len(valid_contours) - 1
        
        x, y, w, h = cv2.boundingRect(cnt)
        features['bounding_box'] = {'x': x, 'y': y, 'w': w, 'h': h}
        
        M = cv2.moments(cnt)
        if M["m00"] == 0: cX, cY = x + w//2, y + h//2
        else: cX, cY = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])
        features['center'] = {'x': cX, 'y': cY}
        
        mask = np.zeros(img_gray.shape, dtype="uint8")
        cv2.drawContours(mask, [cnt], -1, 255, -1)

        features['area'] = area
        perimeter = cv2.arcLength(cnt, True)
        features['perimeter'] = perimeter
        features['circularity'] = (4 * math.pi * area) / (perimeter**2) if perimeter > 0 else 0
        features['aspect_ratio'] = float(w) / h if h > 0 else 0

        hull = cv2.convexHull(cnt)
        hull_area = cv2.contourArea(hull)
        features['solidity'] = area / hull_area if hull_area > 0 else 0
            
        if len(cnt) >= 5:
            ellipse = cv2.fitEllipse(cnt)
            (major_axis, minor_axis) = ellipse[1]
            a, b = max(major_axis, minor_axis), min(major_axis, minor_axis)
            features['eccentricity'] = math.sqrt(1 - (b**2 / a**2)) if a > 0 else 0
        else:
            features['eccentricity'] = 0

        mean_val, std_dev = cv2.meanStdDev(img_gray, mask=mask)
        features['mean_intensity_gray'] = mean_val[0][0]
        features['std_dev_intensity_gray'] = std_dev[0][0]
        _, max_val, _, _ = cv2.minMaxLoc(img_gray, mask=mask)
        features['peak_intensity_gray'] = max_val

        mean_bgr = cv2.mean(img_color, mask=mask)
        features['mean_b'] = mean_bgr[0]
        features['mean_g'] = mean_bgr[1]
        features['mean_r'] = mean_bgr[2]

        all_object_features.append(features)
        
        cv2.drawContours(img_debug, [cnt], -1, (0, 255, 0), 1)
        cv2.putText(img_debug, str(features['object_id']), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    return all_object_features, img_debug, valid_contours

def main():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    INPUT_DIR = os.path.join(BASE_DIR, "assets")
    OUTPUT_ROOT = os.path.join(BASE_DIR, "outputs")
    OUTPUT_FEATURES_DIR = os.path.join(OUTPUT_ROOT, "features")
    OUTPUT_DEBUG_DIR = os.path.join(OUTPUT_ROOT, "debug_images")

    os.makedirs(OUTPUT_FEATURES_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DEBUG_DIR, exist_ok=True)

    print(f"Görüntüler taranıyor: {INPUT_DIR}")
    
    supported_extensions = ('.jpg', '.jpeg', '.png', '.tif', '.tiff')
    new_files = 0
    skipped_files = 0

    for root, dirs, files in os.walk(INPUT_DIR):
        if "outputs" in root: continue
            
        for filename in files:
            if filename.lower().endswith(supported_extensions):
                image_path = os.path.join(root, filename)
                relative_path = os.path.relpath(image_path, INPUT_DIR)
                base_name = os.path.splitext(relative_path)[0].replace(os.path.sep, '_')
                
                json_path = os.path.join(OUTPUT_FEATURES_DIR, f"{base_name}_features.json")
                
                if os.path.exists(json_path):
                    skipped_files += 1
                    continue 

                print(f"--- İşleniyor: {relative_path} ---")
                new_files += 1
                
                img_color = cv2.imread(image_path)
                if img_color is None: continue

                img_processed, img_gray, img_color_original = preprocess_image(img_color)
                features, debug_img, _ = detect_and_extract_features(img_processed, img_gray, img_color_original)
                
                def convert(obj):
                    if isinstance(obj, (np.integer, int)): return int(obj)
                    if isinstance(obj, (np.floating, float)): return float(obj)
                    if isinstance(obj, np.ndarray): return obj.tolist()
                    if isinstance(obj, dict): return {k: convert(v) for k, v in obj.items()}
                    if isinstance(obj, list): return [convert(i) for i in obj]
                    return obj

                with open(json_path, 'w') as f:
                    json.dump(convert(features), f, indent=4)
                
                cv2.imwrite(os.path.join(OUTPUT_DEBUG_DIR, f"{base_name}_debug.jpg"), debug_img)

    print(f"\nBitti. Atlanan: {skipped_files}, Yeni İşlenen: {new_files}")

if __name__ == "__main__":
    main()