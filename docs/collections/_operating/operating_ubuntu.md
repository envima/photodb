---
title: Running on Ubuntu
---

Execute `audio.sh` (located in the PhotoDB / AudioDB root directory) from the console to start the application:

```bash
./audio.sh
```

The web application can now be opened in a browser.

For local instances with default port 8080 go to:  
```text
http://127.0.0.1:8080/
```

If you configured an external server go to the corresponding address.

---

Stop the application by pressing key **crtl-c** or by closing the terminal.

**NOTE**: For images to appear in PhotoApp, corresponding metadata files need to exist. Go to [Tasks](/photodb/usage/tasks.html) to learn how to create metadata files using the **photo_create_yaml** task!
