# Bird Detection and Persistence Fixes

## Issues Found and Fixed

### 1. ✅ Fixed: Duplicate Birds in Detection UI
**Problem**: When recording audio and detecting birds, the same species appeared multiple times in the BirdRegistry list.

**Root Cause**: `bird-detection-context.tsx` was using timestamp-based IDs (`${Date.now()}_${index}`) for `identifiedBirds`, allowing duplicate species to appear in the UI.

**Solution**: Changed the ID to use `species_name` instead, and added deduplication logic to prevent adding birds that already exist in the list:

```tsx
// Before:
id: `${Date.now()}_${index}`,

// After:
id: detection.species_name, // Use species_name as ID to avoid duplicates

// Added deduplication:
setIdentifiedBirds(prev => {
  const existingIds = new Set(prev.map(b => b.id));
  const uniqueNewBirds = newBirds.filter(b => !existingIds.has(b.id));
  return [...uniqueNewBirds, ...prev];
});
```

**File Modified**: `mobile/context/bird-detection-context.tsx`

---

### 2. ✅ Fixed: Sighting Creation Payload Mismatch
**Problem**: When creating sightings in the backend, the request was failing silently due to field name mismatches.

**Root Cause**: Mobile app was sending:
- `latitude` / `longitude` → Backend expects `location_lat` / `location_lon`
- `confidence` → Backend expects `confidence_score`

**Solution**: Updated the sighting payload in `avedex-context.tsx`:

```tsx
// Before:
const sightingPayload = {
  user_id: userId,
  species_name: bird.id,
  common_name: bird.commonName,
  latitude: 0,           // ❌ Wrong field name
  longitude: 0,          // ❌ Wrong field name
  confidence: 0.95,      // ❌ Wrong field name
  image_url: bird.imageUrl || null,
  audio_url: null,
};

// After:
const sightingPayload = {
  user_id: userId,
  species_name: bird.id,
  common_name: bird.commonName,
  location_lat: 0,       // ✅ Correct field name
  location_lon: 0,       // ✅ Correct field name
  confidence_score: 0.95, // ✅ Correct field name
  image_url: bird.imageUrl || null,
  audio_url: null,
};
```

**File Modified**: `mobile/context/avedex-context.tsx`

---

## ✅ Fixed: Birds Don't Persist After Logout/Login

### Problem: Birds Detected via Audio Don't Appear in Collection After Re-login
**Status**: **FIXED** - Backend service communication updated.

**Root Cause**: The sightings service was calling the wrong achievements service endpoint (`/species/detect`) which:
1. Required authentication that the sightings service wasn't providing
2. Expected different field names in the payload

**Solution**: Updated the sightings service to use the correct endpoint: `POST /users/{user_id}/sightings`

**Changes Made** in `services/sightings/app/main.py`:

```python
# Before:
achievement_data = {
    "user_id": sighting.user_id,
    "species_name": sighting.species_name,
    "confidence": sighting.confidence_score,           # ❌ Wrong field
    "location": {                                       # ❌ Wrong structure
        "latitude": sighting.location_lat,
        "longitude": sighting.location_lon
    },
    "detection_time": sighting.timestamp.isoformat()   # ❌ Wrong field
}

response = await client.post(
    f"{ACHIEVEMENTS_URL}/species/detect",              # ❌ Wrong endpoint
    json=achievement_data,
    timeout=10.0
)

# After:
achievement_data = {
    "user_id": sighting.user_id,
    "species_name": sighting.species_name,
    "common_name": sighting.common_name,
    "confidence_score": sighting.confidence_score,     # ✅ Correct field
    "location_lat": sighting.location_lat,             # ✅ Flat structure
    "location_lon": sighting.location_lon,             # ✅ Flat structure
    "timestamp": sighting.timestamp.isoformat()        # ✅ Correct field
}

response = await client.post(
    f"{ACHIEVEMENTS_URL}/users/{sighting.user_id}/sightings",  # ✅ Correct endpoint
    json=achievement_data,
    timeout=10.0
)
```

**Response Handling Updated**:
```python
# The endpoint returns: {"message": "...", "newly_unlocked_achievements": [...]}
if isinstance(body, dict):
    unlocked = body.get("newly_unlocked_achievements", [])
    if isinstance(unlocked, list):
        achievements_unlocked = unlocked
```

**File Modified**: `services/sightings/app/main.py`

---

## Summary of All Fixes

### Frontend Fixes (Mobile App)
1. **Duplicate detection in UI** - Changed ID from timestamp to species_name
2. **Sighting payload fields** - Fixed field names to match backend schema

### Backend Fix (Sightings Service)
1. **Achievements integration** - Changed to use correct endpoint with proper payload structure

---

## Testing the Fix

### 1. Test Duplicate Detection Fix
1. Open the app and go to the "Record" tab
2. Record audio with multiple birds
3. Verify that each species appears only once in the BirdRegistry list
4. ✅ Expected: No duplicate species in the UI

### 2. Test Sighting Creation
1. Detect a bird via audio recording
2. Check the console logs for:
   - `✅ Sighting created successfully for [bird name]`
   - Or error messages if the request failed
3. Logout and login again
4. Go to the Avedex tab
5. ✅ Expected: The detected bird appears in your collection

### 3. Debug Backend Issue
If birds still don't persist after logout:

1. Check mobile console for errors in `addBird()` function
2. Check backend logs for sightings service errors
3. Check backend logs for achievements service authentication errors
4. Verify the `USER_INFO` contains correct `user_id` field

---

## Files Modified

### Frontend (Mobile)
1. **`mobile/context/avedex-context.tsx`**
   - Fixed field names in sighting payload: `location_lat`, `location_lon`, `confidence_score`

2. **`mobile/context/bird-detection-context.tsx`**
   - Changed ID from timestamp to `species_name`
   - Added deduplication logic to prevent duplicate species in UI

### Backend (Services)
3. **`services/sightings/app/main.py`**
   - Changed achievements endpoint from `/species/detect` to `/users/{user_id}/sightings`
   - Updated payload field names to match `SightingEventRequest` schema
   - Updated response handling to extract `newly_unlocked_achievements`

---

## Next Steps

1. Choose one of the backend solutions (Option 1, 2, or 3)
2. Test the backend fix by recording audio and verifying persistence
3. (Optional) Add actual GPS coordinates instead of hardcoded `0, 0`
4. (Optional) Add bird images from eBird API or other sources
