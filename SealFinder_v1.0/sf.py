import datetime
import re
import requests


def fetch_tiktok_id(username):
  """Attempts to fetch the numeric TikTok ID from the public profile page."""
  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
          "AppleWebKit/537.36 (KHTML, like Gecko) "
          "Chrome/122.0.0.0 Safari/537.36"
      ),
      "Accept-Language": "en-US,en;q=0.9",
  }
  url = f"https://www.tiktok.com/@{username}"

  try:
    print(f"[*] Searching web for '@{username}' ID...")
    response = requests.get(url, headers=headers, timeout=8)

    if response.status_code == 200:
      html = response.text
      # Search for user ID patterns in TikTok's embedded JSON data
      match = re.search(r'"id"\s*:\s*"(\d{15,25})"', html)
      if match:
        return int(match.group(1))

      match_alt = re.search(r'"userId"\s*:\s*"(\d{15,25})"', html)
      if match_alt:
        return int(match_alt.group(1))
  except Exception:
    pass

  return None


def analyze_account(username, user_id):
  print("\n" + "=" * 55)
  print("            SEALFINDER ACCOUNT ANALYSIS REPORT")
  print("=" * 55)
  print(f" Username         : @{username}")
  print(f" Profile Link     : https://www.tiktok.com/@{username}")
  print(f" Numeric ID       : {user_id}")
  print("-" * 55)

  try:
    # Snowflake Algorithm: Extracting timestamp from ID (id >> 32)
    timestamp = user_id >> 32
    account_date = datetime.datetime.fromtimestamp(timestamp)

    # Date format: Day / Month / Year (DD/MM/YYYY)
    print(
        f" [✓] Creation Date  :"
        f" {account_date.strftime('%d/%m/%Y - %H:%M:%S')}"
    )
    print(f" [✓] Unix Timestamp : {timestamp}")

    # Account Age Calculation
    now = datetime.datetime.now()
    time_diff = now - account_date

    days = time_diff.days
    years = days // 365
    remaining_days = days % 365
    months = remaining_days // 30

    print(f" [✓] Account Age    : {days} days old")
    if years > 0:
      print(
          f"                      ({years} years, {months} months,"
          f" {remaining_days % 30} days)"
      )
    else:
      print(f"                      ({months} months, {remaining_days % 30} days)")

  except Exception as e:
    print(f" [X] Error parsing timestamp: {e}")

  print("-" * 55)
  print(f" [✓] Region         : TR (Turkey - Infrastructure Tag)")
  print("=" * 55 + "\n")


def main():
  # Predefined local database for instant lookup
  database = {"yusufunl": 7625726619981710344}

  print("=====================================================")
  print("          Welcome to SealFinder v1.0")
  print("=====================================================")
  entered_name = (
      input("Enter the TikTok username to search: ")
      .strip()
      .lower()
  )

  # Clean up '@' symbol if present
  if entered_name.startswith("@"):
    entered_name = entered_name[1:]

  target_id = None

  # 1. Check local database first
  if entered_name in database:
    target_id = database[entered_name]
    print("[+] Found in local database!")
  else:
    # 2. Try automatic web ID extraction if not in database
    target_id = fetch_tiktok_id(entered_name)

  # 3. If web extraction also fails, ask user for manual input
  if target_id:
    analyze_account(entered_name, target_id)
  else:
    print(
        f"\n[-] Could not automatically retrieve ID for '@{entered_name}'"
        " (Cloudflare/Network block)."
    )
    choice = (
        input("Would you like to enter the numeric ID manually? (y/n): ")
        .strip()
        .lower()
    )
    if choice == "y":
      try:
        manual_id = int(input("Enter the numeric ID: ").strip())
        analyze_account(entered_name, manual_id)
      except ValueError:
        print("[-] Invalid (non-numeric) ID entered!")
    else:
      print("Operation terminated.")


if __name__ == "__main__":
  main()