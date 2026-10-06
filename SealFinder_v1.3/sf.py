import datetime
import json
import os
import re
from curl_cffi import requests

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
  """Fetches TikTok data using curl_cffi with improved privacy and region detection."""
  url = f"https://www.tiktok.com/@{username}"

  data = {
      "id": None,
      "followers": "N/A",
      "following": "N/A",
      "hearts": "N/A",
      "videos": "N/A",
      "nickname": "N/A",
      "region": "Global / Not Specified",
      "is_private": False,
      "is_verified": False,
  }

  try:
    print(
        f"{YELLOW}[*]{RESET} Bypassing Cloudflare & fetching TikTok data for"
        f" '@{username}'..."
    )

    response = requests.get(url, impersonate="chrome", timeout=10)

    if response.status_code == 200:
      html = response.text

      # JSON Rehydration extraction for extra details
      json_data = None
      match_univ = re.search(
          r'',
          html,
      )
      if match_univ:
        try:
          json_data = json.loads(match_univ.group(1))
        except Exception:
          pass

      if not json_data:
        match_sigi = re.search(
            r'',
            html,
        )
        if match_sigi:
          try:
            json_data = json.loads(match_sigi.group(1))
          except Exception:
            pass

      if json_data:
        try:
          scope = json_data.get("__DEFAULT_SCOPE__", {})
          user_detail = scope.get("webapp.user-detail", {})
          user_info = (
              user_detail.get("userInfo", {}).get("user", {})
              if user_detail
              else {}
          )
          stats_info = (
              user_detail.get("userInfo", {}).get("stats", {})
              if user_detail
              else {}
          )

          if not user_info:
            sigi_users = json_data.get("UserModule", {}).get("users", {})
            if sigi_users:
              uid_key = list(sigi_users.keys())[0]
              user_info = sigi_users[uid_key]
            sigi_stats = json_data.get("UserModule", {}).get("stats", {})
            if sigi_stats:
              uid_key = list(sigi_stats.keys())[0]
              stats_info = sigi_stats[uid_key]

          if user_info:
            data["nickname"] = (
                user_info.get("nickname")
                or user_info.get("nickName")
                or user_info.get("name")
                or "N/A"
            )
            data["is_private"] = (
                user_info.get("secret", False)
                or user_info.get("privateAccount", False)
                or user_info.get("isPrivate", False)
            )
            data["is_verified"] = user_info.get("verified", False)
            data["region"] = (
                user_info.get("region")
                or user_info.get("country")
                or "Global / Not Specified"
            )

          if stats_info:
            data["followers"] = str(
                stats_info.get("followerCount", "N/A")
            )
            data["following"] = str(
                stats_info.get("followingCount", "N/A")
            )
            data["hearts"] = str(
                stats_info.get(
                    "heartCount", stats_info.get("diggCount", "N/A")
                )
            )
            data["videos"] = str(
                stats_info.get("videoCount", "N/A")
            )
        except Exception:
          pass

      # Regex fallbacks if JSON fails or misses fields
      if not data["is_private"]:
        if (
            re.search(r'"secret"\s*:\s*true', html, re.IGNORECASE)
            or re.search(r'"privateAccount"\s*:\s*true', html, re.IGNORECASE)
            or re.search(r'"isPrivate"\s*:\s*true', html, re.IGNORECASE)
        ):
          data["is_private"] = True

      if data["nickname"] == "N/A":
        nick_match = re.search(r'"nickname"\s*:\s*"([^"]+)"', html)
        if nick_match:
          data["nickname"] = nick_match.group(1)

      if data["region"] == "Global / Not Specified":
        reg_match = re.search(r'"region"\s*:\s*"([^"]+)"', html)
        if reg_match:
          data["region"] = reg_match.group(1)

      match = re.search(r'"id"\s*:\s*"(\d{15,25})"', html)
      if match:
        data["id"] = int(match.group(1))
      else:
        match_alt = re.search(r'"userId"\s*:\s*"(\d{15,25})"', html)
        if match_alt:
          data["id"] = int(match_alt.group(1))

      if data["followers"] == "N/A":
        f_match = re.search(r'"followerCount"\s*:\s*(\d+)', html)
        if f_match:
          data["followers"] = f_match.group(1)

      if data["following"] == "N/A":
        fg_match = re.search(r'"followingCount"\s*:\s*(\d+)', html)
        if fg_match:
          data["following"] = fg_match.group(1)

      if data["hearts"] == "N/A":
        h_match = re.search(r'"heartCount"\s*:\s*(\d+)', html)
        if h_match:
          data["hearts"] = h_match.group(1)

      if data["videos"] == "N/A":
        v_match = re.search(r'"videoCount"\s*:\s*(\d+)', html)
        if v_match:
          data["videos"] = v_match.group(1)
    else:
      print(
          f" {RED}[-]{RESET} Cloudflare Blocked or HTTP Status:"
          f" {response.status_code}"
      )

  except Exception as e:
    print(f" {RED}[X]{RESET} Connection/Bypass Error: {e}")

  return data


def analyze_tiktok(username):
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
    print(f" {GREEN}[✓]{RESET} Nickname     : {target_data['nickname']}")
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
    print(
        f" {GREEN}[✓]{RESET} Private Account: "
        f"{'Yes' if target_data['is_private'] else 'No'}"
    )
    print(
        f" {GREEN}[✓]{RESET} Verified (Tick): "
        f"{'Yes' if target_data['is_verified'] else 'No'}"
    )
    print(
        f" {GREEN}[✓]{RESET} Region         :"
        f" {str(target_data['region']).upper()}"
    )
    print(CYAN + "=" * 55 + RESET + "\n")
  else:
    print(
        f"\n{RED}[-]{RESET} Could not automatically retrieve ID for"
        f" '@{username}'."
    )


def scan_global_footprint(username):
  """Scans global platforms for the given username using curl_cffi."""
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
      response = requests.get(url, impersonate="chrome", timeout=5)
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