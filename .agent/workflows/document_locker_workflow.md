---
description: Test the Citizen Document Locker functionality (Upload, View, Download, Delete)
---

# Citizen Document Locker Workflow

This workflow validates the "Digital Document Locker" feature, ensuring users can securely store, retrieve, and manage their documents.

## 1. Access the Locker
1. Login as a **Citizen**.
2. Navigate to **Dashboard** -> **Document Locker** (in the user dropdown or "Express Portal" cards).
3. URL: `/citizen/locker/`

## 2. Upload a Document
1. Click the **"Upload Document"** button (top right or empty state).
2. **Fill the form**:
   - **Document Label**: Enter a name (e.g., "Aadhaar Card").
   - **Category**: Select a type (e.g., "Identity Proof").
   - **Select File**: Choose a PDF or Image file (JPG, PNG) from your device.
3. Click **"Start Upload"**.
4. **Verify**:
   - A success message "Document permanently added..." appears.
   - The new document card appears in the grid.
   - The "Documents Stored" count increases.

## 3. View Document
1. Locate the document card.
2. Click the **"View"** button.
3. **Verify**:
   - The file opens in a new browser tab.
   - The URL path starts with `/media/locker/...`.

## 4. Download Document
1. Locate the document card.
2. Click the **"Save"** button.
3. **Verify**:
   - The file downloads to your local machine instead of opening.

## 5. Delete Document
1. Locate the document card.
2. Click the **"Delete"** button.
3. Confirm the browser popup ("Are you sure...?").
4. **Verify**:
   - A success message "Document removed..." appears.
   - The document card is removed from the grid.
   - The file is physically deleted from the server (check `media/locker/` folder if checking backend).

## Troubleshooting "Not Found" Errors
If you see a 404 "Not Found" error when viewing files:
- **Local Dev**: Ensure `DEBUG = True` in `settings.py`.
- **Production (Render)**: Django does not serve media files in production by default. 
  - **Fix**: We have enabled a fallback media serving pattern in `urls.py` to handle this for demo purposes.
  - **Note**: Files uploaded on one Render instance may be lost if the instance restarts (ephemeral storage), leading to 404s for old records. Re-upload the file to fix.
