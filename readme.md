# 📡 Python News & Content Monitor

A lightweight automation script that monitors news websites for updates. It identifies new content in real-time and maintains a local history to avoid data redundancy.
Here it works with NYTimes and anaylise all the headlines to see what is the most common word used today

## 💡 How it Works
1. **Scans** the target URL for specific headlines or article tags.
2. **Compares** found titles with a local `history.txt` file.
3. **Logs** only the new entries with a timestamp.
4. **Notifies** the user via the console (easily extendable to Telegram/Email).

## 🛠️ Technical Details
- **Architecture:** Local persistent storage (File I/O).
- **Libraries:** `Requests` for network calls, `BeautifulSoup4` for DOM parsing.
- **Robustness:** Includes basic error handling for network timeouts and 404 errors.

## 🚀 Future Improvements
- [ ] Integration with Telegram Bot API for instant mobile alerts.
- [ ] Multi-site monitoring support.
- [ ] SQL Database integration for large-scale history tracking.
- [ ] Web designing with any site 

---
*Demonstrating proficiency in data persistence and automated monitoring.*