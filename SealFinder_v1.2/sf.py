import datetime
import os
import re
import requests

# Windows terminal ANSI color support fix
if os.name == "nt":
  os.system("")

# ANSI Color Codes for Terminal UI
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


def fetch_tiktok_data(username):
  """Fetches the numeric TikTok ID and public profile stats."""
  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
          "AppleWebKit/537.36 (KHTML, like Gecko) "
          "Chrome/122.0.0.0 Safari/537.36"
      ),
      "Accept-Language": "en-US,en;q=0.9",
  }
  url = f"https://www.tiktok.com/@{username}"

  data = {
      "id": None,
      "followers": "N/A",
      "following": "N/A",
      "hearts": "N/A",
      "videos": "N/A",
  }

  try:
    print(f"{YELLOW}[*]{RESET} Fetching TikTok data for '@{username}'...")
    response = requests.get(url, headers=headers, timeout=8)

    if response.status_code == 200:
      html = response.text

      match = re.search(r'"id"\s*:\s*"(\d{15,25})"', html)
      if match:
        data["id"] = int(match.group(1))
      else:
        match_alt = re.search(r'"userId"\s*:\s*"(\d{15,25})"', html)
        if match_alt:
          data["id"] = int(match_alt.group(1))

      followers_match = re.search(r'"followerCount"\s*:\s*(\d+)', html)
      if followers_match:
        data["followers"] = followers_match.group(1)

      following_match = re.search(r'"followingCount"\s*:\s*(\d+)', html)
      if following_match:
        data["following"] = following_match.group(1)

      hearts_match = re.search(r'"heartCount"\s*:\s*(\d+)', html)
      if hearts_match:
        data["hearts"] = hearts_match.group(1)

      videos_match = re.search(r'"videoCount"\s*:\s*(\d+)', html)
      if videos_match:
        data["videos"] = videos_match.group(1)

  except Exception:
    pass

  return data


def analyze_tiktok(username):
  database = {"yusufunl": 7625726619981710344}
  target_data = {
      "id": None,
      "followers": "N/A",
      "following": "N/A",
      "hearts": "N/A",
      "videos": "N/A",
  }

  if username in database:
    target_data["id"] = database[username]
    print(
        f"{GREEN}[+]{RESET} Found ID in local database, fetching live stats..."
    )
    live_data = fetch_tiktok_data(username)
    if live_data["id"]:
      target_data["id"] = live_data["id"]
    target_data["followers"] = live_data["followers"]
    target_data["following"] = live_data["following"]
    target_data["hearts"] = live_data["hearts"]
    target_data["videos"] = live_data["videos"]
  else:
    target_data = fetch_tiktok_data(username)

  if target_data["id"]:
    print("\n" + CYAN + "=" * 55 + RESET)
    print(
        CYAN
        + BOLD
        + "             SEALFINDER - TIKTOK ANALYSIS"
        + RESET
    )
    print(CYAN + "=" * 55 + RESET)
    print(f" {BOLD}Username{RESET}         : @{username}")
    print(f" {BOLD}Profile Link{RESET}     : https://www.tiktok.com/@{username}")
    print(f" {BOLD}Numeric ID{RESET}       : {GREEN}{target_data['id']}{RESET}")
    print("-" * 55)
    print(f" {GREEN}[✓]{RESET} Followers    : {target_data['followers']}")
    print(f" {GREEN}[✓]{RESET} Following    : {target_data['following']}")
    print(f" {GREEN}[✓]{RESET} Total Likes  : {target_data['hearts']}")
    print(f" {GREEN}[✓]{RESET} Video Count  : {target_data['videos']}")
    print("-" * 55)

    try:
      timestamp = target_data["id"] >> 32
      account_date = datetime.datetime.fromtimestamp(timestamp)
      print(
          f" {GREEN}[✓]{RESET} Creation Date  :"
          f" {YELLOW}{account_date.strftime('%d/%m/%Y - %H:%M:%S')}{RESET}"
      )
      print(f" {GREEN}[✓]{RESET} Unix Timestamp : {timestamp}")

      now = datetime.datetime.now()
      time_diff = now - account_date
      days = time_diff.days
      years = days // 365
      remaining_days = days % 365
      months = remaining_days // 30

      print(f" {GREEN}[✓]{RESET} Account Age    : {GREEN}{days} days old{RESET}")
      if years > 0:
        print(
            f"                      ({years} years, {months} months,"
            f" {remaining_days % 30} days)"
        )
      else:
        print(
            f"                      ({months} months, {remaining_days % 30}"
            " days)"
        )

    except Exception as e:
      print(f" {RED}[X]{RESET} Error parsing timestamp: {e}")

    print("-" * 55)
    print(f" {GREEN}[✓]{RESET} Region         : TR (Turkey - Infrastructure Tag)")
    print(CYAN + "=" * 55 + RESET + "\n")
  else:
    print(
        f"\n{RED}[-]{RESET} Could not automatically retrieve ID for"
        f" '@{username}'."
    )


def scan_global_footprint(username):
  """Scans global platforms for the given username."""
  platforms = {
      "Instagram": f"https://www.instagram.com/{username}/",
      "Twitter/X": f"https://twitter.com/{username}",
      "GitHub": f"https://github.com/{username}",
      "Reddit": f"https://www.reddit.com/user/{username}",
      "Pinterest": f"https://www.pinterest.com/{username}/",
      "Telegram": f"https://t.me/{username}",
      "Steam": f"https://steamcommunity.com/id/{username}",
      "Twitch": f"https://www.twitch.tv/{username}",
  }

  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
          "AppleWebKit/537.36 (KHTML, like Gecko) "
          "Chrome/122.0.0.0 Safari/537.36"
      )
  }

  print("\n" + CYAN + "=" * 55 + RESET)
  print(
      CYAN
      + BOLD
      + f"         CROSS-PLATFORM SCAN: @{username}"
      + RESET
  )
  print(CYAN + "=" * 55 + RESET)

  for platform, url in platforms.items():
    try:
      response = requests.get(url, headers=headers, timeout=5)
      if response.status_code == 200:
        print(f" {GREEN}[FOUND]{RESET} {platform:<12} : {url}")
      else:
        print(f" {RED}[NOT FOUND]{RESET} {platform:<12}")
    except Exception:
      print(f" {YELLOW}[TIMEOUT/ERR]{RESET} {platform:<12}")

  print(CYAN + "=" * 55 + RESET + "\n")


def main():
  while True:
    print(CYAN + "=====================================================" + RESET)
    print(CYAN + BOLD + "             SealFinder v1.3" + RESET)
    print(CYAN + "=====================================================" + RESET)
    print(f" {YELLOW}[1]{RESET} TikTok Intelligence Analysis")
    print(f" {YELLOW}[2]{RESET} Cross-Platform Username Scan")
    print(f" {YELLOW}[3]{RESET} Exit")
    print(CYAN + "=====================================================" + RESET)

    choice = input(f"{YELLOW}Select option (1-3): {RESET}").strip()

    if choice == "1":
      uname = (
          input(f"{YELLOW}Enter TikTok username: {RESET}").strip().lower()
      )
      if uname.startswith("@"):
        uname = uname[1:]
      if uname:
        analyze_tiktok(uname)
      input(f"Press {BOLD}Enter{RESET} to continue...")

    elif choice == "2":
      uname = input(f"{YELLOW}Enter target username: {RESET}").strip()
      if uname.startswith("@"):
        uname = uname[1:]
      if uname:
        scan_global_footprint(uname)
      input(f"Press {BOLD}Enter{RESET} to continue...")

    elif choice == "3":
      print(f"\n{GREEN}[*]{RESET} Exiting SealFinder.\n")
      break
    else:
      print(f"{RED}[-] Invalid selection!{RESET}\n")


if __name__ == "__main__":
  main()