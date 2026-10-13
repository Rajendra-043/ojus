SAVE YOUR CAMPUS PHOTO HERE as: campus.jpg

You sent the BIT Durg campus photo in chat (building + palm trees + grass).
I cannot copy chat images to disk, so please save it manually:

  1. Save the photo as  campus.jpg
  2. Put one copy here:  backend/static/core/img/campus.jpg
  3. Put one copy here:  frontend/assets/campus.jpg

The CSS already references it:
  backend:  background-image: ... url("img/campus.jpg")
  frontend: background-image: ... url("assets/campus.jpg")

Until campus.jpg exists you will see a dark gradient fallback.
Recommended size: 1600px+ wide JPG, < 500 KB (compress with TinyJPG).
