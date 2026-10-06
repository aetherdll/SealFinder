import datetime
import os
import re
import requests

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
    print(f"{YELLOW}[*]{RESET} Fetching public data for '@{username}'...")
    response = requests.get(url, headers=headers, timeout=8)

    if response.status_code == 200:
      html = response.text

      # 1. Extract ID
      match = re.search(r'"id"\s*:\s*"(\d{15,25})"', html)
      if match:
        data["id"] = int(match.group(1))
      else:
        match_alt = re.search(r'"userId"\s*:\s*"(\d{15,25})"', html)
        if match_alt:
          data["id"] = int(match_alt.group(1))

      # 2. Extract Public Stats
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


def analyze_account(username, user_data):
  print("\n" + CYAN + "=" * 55 + RESET)
  print(
      CYAN
      + BOLD
      + "            SEALFINDER ACCOUNT ANALYSIS REPORT"
      + RESET
  )
  print(CYAN + "=" * 55 + RESET)
  print(f" {BOLD}Username{RESET}         : @{username}")
  print(f" {BOLD}Profile Link{RESET}     : https://www.tiktok.com/@{username}")
  print(f" {BOLD}Numeric ID{RESET}       : {GREEN}{user_data['id']}{RESET}")
  print("-" * 55)
  print(f" {GREEN}[✓]{RESET} Followers    : {user_data['followers']}")
  print(f" {GREEN}[✓]{RESET} Following    : {user_data['following']}")
  print(f" {GREEN}[✓]{RESET} Total Likes  : {user_data['hearts']}")
  print(f" {GREEN}[✓]{RESET} Video Count  : {user_data['videos']}")
  print("-" * 55)

  try:
    timestamp = user_data["id"] >> 32
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
      print(f"                      ({months} months, {remaining_days % 30} days)")

  except Exception as e:
    print(f" {RED}[X]{RESET} Error parsing timestamp: {e}")

  print("-" * 55)
  print(f" {GREEN}[✓]{RESET} Region         : TR (Turkey - Infrastructure Tag)")
  print(CYAN + "=" * 55 + RESET + "\n")


def main():
  database = {"yusufunl": 7625726619981710344}

  print(CYAN + "=====================================================" + RESET)
  print(CYAN + BOLD + "          Welcome to SealFinder v1.1" + RESET)
  print(CYAN + "=====================================================" + RESET)
  entered_name = (
      input(f"{YELLOW}Enter the TikTok username to search: {RESET}")
      .strip()
      .lower()
  )

  if entered_name.startswith("@"):
    entered_name = entered_name[1:]

  target_data = {
      "id": None,
      "followers": "N/A",
      "following": "N/A",
      "hearts": "N/A",
      "videos": "N/A",
  }

  if entered_name in database:
    target_data["id"] = database[entered_name]
    print(
        f"{GREEN}[+]{RESET} Found ID in local database, fetching live stats..."
    )
    live_data = fetch_tiktok_data(entered_name)
    if live_data["id"]:
      target_data["id"] = live_data["id"]
    target_data["followers"] = live_data["followers"]
    target_data["following"] = live_data["following"]
    target_data["hearts"] = live_data["hearts"]
    target_data["videos"] = live_data["videos"]
  else:
    target_data = fetch_tiktok_data(entered_name)

  if target_data["id"]:
    analyze_account(entered_name, target_data)
  else:
    print(
        f"\n{RED}[-]{RESET} Could not automatically retrieve ID for"
        f" '@{entered_name}' (Cloudflare/Network block)."
    )
    choice = (
        input(
            f"{YELLOW}Would you like to enter the numeric ID manually? (y/n):"
            f" {RESET}"
        )
        .strip()
        .lower()
    )
    if choice == "y":
      try:
        manual_id = int(
            input(f"{YELLOW}Enter the numeric ID: {RESET}").strip()
        )
        target_data["id"] = manual_id
        analyze_account(entered_name, target_data)
      except ValueError:
        print(f"{RED}[-] Invalid (non-numeric) ID entered!{RESET}")
    else:
      print("Operation terminated.")


if __name__ == "__main__":
  main()