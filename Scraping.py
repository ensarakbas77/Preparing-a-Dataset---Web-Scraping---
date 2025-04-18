from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import re


def temizle_metin(metin):
    return re.sub(r"\(.*?\)", "", metin).strip()


def sonuc_degerlendir(home_score, away_score, is_home):
    if home_score == away_score:
        return 0
    elif (is_home and home_score > away_score) or (not is_home and away_score > home_score):
        return 1
    else:
        return -1


def yuzde_donustur(deger):
    try:
        if "%" in deger:
            # Yüzde değerini olduğu gibi döndür, % işaretini kaldır
            return deger.replace("%", "").strip()
        return re.sub("[^0-9]", "", deger)
    except:
        return "0"


def get_stat_value(element, class_name):
    try:
        return element.find_element(By.CLASS_NAME, class_name).text.strip()
    except:
        return "0"


options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
driver.maximize_window()

team_id = 1   # Takım ID (Liv=1, City=2, Che=3, Manu=4, Arsenal=5, Tot=6)
base_url = "https://arsiv.mackolik.com"
team_url = f"{base_url}/Team/Default.aspx?id=30"
driver.get(team_url)

time.sleep(3)

match_links = driver.find_elements(By.TAG_NAME, 'a')
match_urls = [link.get_attribute('href') for link in match_links if
              link.get_attribute('href') and 'Karsilastirma' in link.get_attribute('href')]
match_urls = [url if url.startswith('http') else base_url + url for url in match_urls]

print(f"Bulunan Maç Linkleri: {len(match_urls)}")

debug_enabled = False

with open('demo.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([
        "Tarih", "Rakip Takım", "Takım ID", "Is_Home", "Sonuç", "Gol", "Rakip Gol",
        "Topla Oynama(%)", "Şut", "İsabetli Şut", "Başarılı Pas", "Pas Başarısı(%)",
        "Korner", "Orta", "Faul", "Ofsayt", "Rakip Topla Oynama(%)", "Rakip Şut",
        "Rakip İsabetli Şut", "Rakip Başarılı Pas", "Rakip Pas Başarısı(%)",
        "Rakip Korner", "Rakip Orta", "Rakip Faul", "Rakip Ofsayt", "xG"
    ])

    for match_url in match_urls:
        driver.get(match_url)

        try:
            date_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "match-info-date"))
            )
            match_date = date_element.text.replace("Tarih : ", "").strip()

            score_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "match-score"))
            )
            score_text = score_element.text.strip()

            if "-" not in score_text:
                continue

            home_score, away_score = map(int, score_text.split('-'))

            title_text = driver.title
            home_team, away_team = map(temizle_metin, title_text.split(' - ')[0:2])

            # Takımın tam adı
            team_name = "Liverpool"
            is_home = 1 if home_team == team_name else 0
            rakip_takim = away_team if is_home else home_team

            # Gol bilgilerini ayarla
            team_goals = home_score if is_home else away_score
            opponent_goals = away_score if is_home else home_score

            sonuc = sonuc_degerlendir(home_score, away_score, is_home)

            print(f"Maç: {home_team} {home_score} - {away_score} {away_team} | {match_date}")

            stats = {}

            all_stat_rows = driver.find_elements(By.CLASS_NAME, "match-statistics-rows") + \
                            driver.find_elements(By.CLASS_NAME, "match-statistics-rows-2")

            debug_stats = ["Pas Başarısı(%)", "Topla Oynama(%)"]

            for row in all_stat_rows:
                try:
                    # İstatistik başlığını al
                    stat_title_element = row.find_element(By.CLASS_NAME, "statistics-title-text")
                    stat_title = stat_title_element.text.strip()

                    # Takım 1 ve Takım 2 değerlerini al
                    team1_stat = get_stat_value(row, "team-1-statistics-text")
                    team2_stat = get_stat_value(row, "team-2-statistics-text")

                    if debug_enabled and stat_title in debug_stats:
                        print(f"DEBUG - {stat_title}: Takım 1 = {team1_stat}, Takım 2 = {team2_stat}")

                    if stat_title == "Orta":
                        team1_stat = team1_stat.split('/')[0] if '/' in team1_stat else team1_stat
                        team2_stat = team2_stat.split('/')[0] if '/' in team2_stat else team2_stat

                    stats[stat_title] = (team1_stat, team2_stat)

                except Exception as e:
                    if debug_enabled:
                        print(f"İstatistik hatası ({stat_title if 'stat_title' in locals() else 'bilinmeyen'}): {e}")

            team_data = []
            opponent_data = []

            mappings = {
                "Topla Oynama(%)": ["Topla Oynama(%)", "Topla Oynama"],
                "Şut": ["Toplam Şut", "Şut"],
                "İsabetli Şut": ["İsabetli Şut"],
                "Başarılı Pas": ["Başarılı Paslar", "Başarılı Pas"],
                "Pas Başarısı(%)": ["Pas Başarısı(%)", "Pas Başarısı"],
                "Korner": ["Korner"],
                "Orta": ["Orta"],
                "Faul": ["Faul"],
                "Ofsayt": ["Ofsayt"]
            }

            for excel_col, possible_html_stats in mappings.items():
                found = False

                for html_stat in possible_html_stats:
                    if html_stat in stats:
                        if is_home:
                            team_val = yuzde_donustur(stats[html_stat][0])
                            opp_val = yuzde_donustur(stats[html_stat][1])
                        else:
                            team_val = yuzde_donustur(stats[html_stat][1])
                            opp_val = yuzde_donustur(stats[html_stat][0])

                        team_data.append(team_val)
                        opponent_data.append(opp_val)
                        found = True

                        if debug_enabled and excel_col in ["Topla Oynama(%)", "Pas Başarısı(%)"]:
                            print(f"Excel {excel_col} için {html_stat} kullanıldı: Takım={team_val}, Rakip={opp_val}")

                        break

                if not found:
                    for stat_key in stats:
                        key_match = False
                        for html_stat in possible_html_stats:

                            clean_stat_key = stat_key.replace("(%)", "").replace("%", "").strip()
                            clean_html_stat = html_stat.replace("(%)", "").replace("%", "").strip()

                            if clean_html_stat in clean_stat_key or clean_stat_key in clean_html_stat:
                                key_match = True
                                break

                        if key_match:
                            if is_home:
                                team_val = yuzde_donustur(stats[stat_key][0])
                                opp_val = yuzde_donustur(stats[stat_key][1])
                            else:
                                team_val = yuzde_donustur(stats[stat_key][1])
                                opp_val = yuzde_donustur(stats[stat_key][0])

                            team_data.append(team_val)
                            opponent_data.append(opp_val)

                            if debug_enabled and excel_col in ["Topla Oynama(%)", "Pas Başarısı(%)"]:
                                print(f"Excel {excel_col} için alternatif olarak {stat_key} kullanıldı: Takım={team_val}, Rakip={opp_val}")

                            found = True
                            break

                    if not found:
                        team_data.append("0")
                        opponent_data.append("0")
                        if debug_enabled:
                            print(f"Excel {excel_col} için hiçbir istatistik bulunamadı")

            row_data = [
                match_date, rakip_takim, team_id, is_home, sonuc, team_goals, opponent_goals,
                *team_data, *opponent_data, ""
            ]

            writer.writerow(row_data)

        except Exception as e:
            if debug_enabled:
                print(f"Maç için hata oluştu: {e}")
                import traceback
                traceback.print_exc()

driver.quit()
